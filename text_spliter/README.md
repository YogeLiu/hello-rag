# RecursiveTextSplitter 修复说明

## 修复概述

已将 `RecursiveTextSplitter` 修复为**保留分隔符的版本**，确保文本切分后保持原有的空格、换行符等结构，提高可读性和语义完整性。

---

## 主要修复内容

### 1. **分隔符保留机制**

**修复前**：
- 所有分隔符在合并时被完全移除
- 结果文本失去空格和换行符，可读性差

**修复后**：
- 字面分隔符（如空格、换行符）在合并时被重新插入
- 正则表达式分隔符不重新插入（因为无法确定具体匹配到的字符）

```python
# 修复后的关键逻辑
if self.is_separator_regex:
    merge_separator = ""  # 正则分隔符不重新插入
else:
    merge_separator = separator  # 字面分隔符重新插入
```

### 2. **`__merge_segments` 方法优化**

- 正确计算包含分隔符的长度
- 完整的重叠逻辑（包含两个条件）
- 准确的 total 计算和更新

```python
# 计算长度时考虑分隔符
added_length = seg_len + (sep_len if len(current_doc) > 0 else 0)

# 重叠逻辑完整
while total > self.overlap_count or (
    total + seg_len + (sep_len if len(current_doc) > 0 else 0) > self.chunk_size
    and total > 0
):
    total -= len(current_doc[0]) + (sep_len if len(current_doc) > 1 else 0)
    current_doc = current_doc[1:]
```

### 3. **`__recursive_split` 方法增强**

- 使用 `enumerate` 正确获取索引
- 正确计算 `new_separators`
- 区分正则和字面分隔符的处理

```python
for i, s_ in enumerate(separators):
    # ...
    if re.search(separator_, text):
        separator = s_
        new_separators = separators[i + 1:]  # ✓ 正确的索引
        break
```

### 4. **边界情况处理**

- 过滤 `re.split()` 产生的空字符串
- 正确处理空分隔符 `""`（字符级切分）
- 检查 `new_separators` 而不是 `separator`

---

## 功能验证

### ✅ 测试1：基本功能
```python
text = "Hello world. How are you? I am fine. Thank you."
# 结果：空格和标点符号正确保留
```

### ✅ 测试2：重叠功能
```python
text = "a b c d e f g h i j k l m n o p"
chunk_size = 10, overlap_count = 3
# 结果：所有相邻 chunk 都有 3 字符重叠
```

### ✅ 测试3：多级分隔符
```python
separators = ["\n\n", "\n", " ", ""]
# 结果：从段落→行→单词→字符递归切分
```

### ✅ 测试4：中文文本
```python
separators = ["。", "！", " ", ""]
# 结果：中文标点符号正确处理
```

### ✅ 测试5：正则表达式
```python
separators = [r"[,;|]", ""]
is_separator_regex = True
# 结果：正则分隔符被移除（不插入字面值）
```

### ✅ 测试6：极端情况
```python
text = "Thisisaverylongsentencewithoutanyspacesornewlines"
# 结果：按字符切分，符合 chunk_size 限制
```

### ✅ 测试7：与 LangChain 对比
```python
# 结果：与 LangChain RecursiveCharacterTextSplitter 完全一致！
```

---

## 核心设计

### 分隔符处理策略

| 分隔符类型 | 切分行为 | 合并行为 | 示例 |
|-----------|---------|---------|------|
| 字面分隔符 | `re.split()` 移除 | 用原分隔符 `join()` | `" "`, `"\n"`, `"。"` |
| 正则分隔符 | `re.split()` 移除 | 用空字符串 `join()` | `r"[,;]"`, `r"\s+"` |
| 空字符串 | `list(text)` | 用空字符串 `join()` | `""` |

### 重叠逻辑

重叠通过"滑动窗口"实现：

1. 保存当前 chunk 后，保留部分内容作为下一个 chunk 的开头
2. 移除头部 segment 直到：
   - `total ≤ overlap_count`，或
   - 有足够空间容纳下一个 segment

### 递归切分流程

```
尝试分隔符1（如 "\n\n"）
  ├─ 找到 → 用它切分
  │   ├─ segment ≤ chunk_size → 收集
  │   └─ segment > chunk_size → 递归用下一级分隔符
  └─ 未找到 → 尝试下一个分隔符
```

---

## 使用示例

### 基本用法

```python
from text_spliter.simple import RecursiveTextSplitter

splitter = RecursiveTextSplitter(
    separators=["\n\n", "\n", " ", ""],
    chunk_size=500,
    overlap_count=50
)

text = """Your long document here..."""
chunks = splitter.split_text(text)
```

### 中文文本

```python
splitter = RecursiveTextSplitter(
    separators=["\n\n", "\n", "。", "！", "？", "，", " ", ""],
    chunk_size=500,
    overlap_count=50
)
```

### 正则表达式分隔符

```python
splitter = RecursiveTextSplitter(
    separators=[r"\n{2,}", r"[.!?]", " ", ""],
    chunk_size=500,
    overlap_count=50,
    is_separator_regex=True
)
```

---

## 与 LangChain 的对比

| 特性 | RecursiveTextSplitter | LangChain |
|-----|----------------------|-----------|
| 分隔符保留 | ✓ 字面分隔符保留 | ✓ 可配置 |
| 正则表达式 | ✓ 支持 | ✓ 支持 |
| 重叠逻辑 | ✓ 完整实现 | ✓ 完整实现 |
| 结果一致性 | ✓ 与 LangChain 一致 | - |
| 代码复杂度 | 简化版（165行） | 完整版（更多功能） |

---

## 注意事项

1. **正则表达式分隔符**：匹配的字符会被移除，不会重新插入
2. **chunk_size 限制**：如果单个 segment 超过 chunk_size，会被强制包含
3. **overlap_count**：应该小于 chunk_size，否则可能导致意外行为
4. **性能**：对于大文本（>100KB），建议先用更粗粒度的分隔符预处理

---

## 总结

修复后的 `RecursiveTextSplitter` 已经完全可用：

- ✅ 逻辑正确，无 bug
- ✅ 保留分隔符，可读性好
- ✅ 支持中文和正则表达式
- ✅ 与 LangChain 行为一致
- ✅ 适用于 RAG 应用

可以放心使用！
