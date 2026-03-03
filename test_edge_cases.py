"""测试边界情况和异常场景"""

from text_spliter.simple import RecursiveTextSplitter

print("=" * 80)
print("边界测试1：空文本")
print("=" * 80)

splitter = RecursiveTextSplitter(separators=["\n\n", "\n", " ", ""], chunk_size=20, overlap_count=5)

text_empty = ""
chunks_empty = splitter.split_text(text_empty)
print(f"结果: {chunks_empty}")
print(f"长度: {len(chunks_empty)}")

print("\n" + "=" * 80)
print("边界测试2：单个字符")
print("=" * 80)

text_single = "A"
chunks_single = splitter.split_text(text_single)
print(f"结果: {chunks_single}")

print("\n" + "=" * 80)
print("边界测试3：超大单个 segment（大于 chunk_size）")
print("=" * 80)

text_huge_word = "A" * 50  # 50个字符，大于 chunk_size=20
chunks_huge = splitter.split_text(text_huge_word)
print(f"文本长度: {len(text_huge_word)}")
print(f"生成的 chunks 数量: {len(chunks_huge)}")
for i, chunk in enumerate(chunks_huge, 1):
    print(f"  Chunk {i} (长度={len(chunk):2d}): [{chunk[:20]}...]")

print("\n" + "=" * 80)
print("边界测试4：overlap 等于 chunk_size（极端情况）")
print("=" * 80)

try:
    splitter_extreme = RecursiveTextSplitter(separators=[" ", ""], chunk_size=10, overlap_count=10)
    text_extreme = "a b c d e f g h i j k"
    chunks_extreme = splitter_extreme.split_text(text_extreme)
    print(f"结果: {chunks_extreme}")
    print(f"数量: {len(chunks_extreme)}")
except Exception as e:
    print(f"错误: {e}")

print("\n" + "=" * 80)
print("边界测试5：overlap 大于 chunk_size（不合理配置）")
print("=" * 80)

try:
    splitter_invalid = RecursiveTextSplitter(separators=[" ", ""], chunk_size=10, overlap_count=15)
    text_invalid = "a b c d e f g h i j k"
    chunks_invalid = splitter_invalid.split_text(text_invalid)
    print(f"结果: {chunks_invalid}")
    print(f"数量: {len(chunks_invalid)}")
    print("⚠️  注意：这种配置可能导致无限循环或异常行为")
except Exception as e:
    print(f"错误: {e}")

print("\n" + "=" * 80)
print("边界测试6：只有分隔符的文本")
print("=" * 80)

text_only_sep = "\n\n\n\n"
chunks_only_sep = splitter.split_text(text_only_sep)
print(f"结果: {chunks_only_sep}")
print(f"长度: {len(chunks_only_sep)}")

print("\n" + "=" * 80)
print("边界测试7：多个连续空格")
print("=" * 80)

text_spaces = "a     b     c"
splitter_space = RecursiveTextSplitter(separators=[" ", ""], chunk_size=10, overlap_count=0)
chunks_spaces = splitter_space.split_text(text_spaces)
print(f"结果: {chunks_spaces}")

print("\n" + "=" * 80)
print("边界测试8：正则表达式分隔符")
print("=" * 80)

text_regex = "item1,item2;item3,item4;item5"
splitter_regex = RecursiveTextSplitter(separators=[r"[,;]", ""], chunk_size=15, overlap_count=0, is_separator_regex=True)
chunks_regex = splitter_regex.split_text(text_regex)
print(f"结果: {chunks_regex}")

print("\n" + "=" * 80)
print("性能测试：大文本")
print("=" * 80)

import time

text_large = "Hello world! " * 1000  # ~13000 字符
start = time.time()
chunks_large = splitter.split_text(text_large)
elapsed = time.time() - start

print(f"文本长度: {len(text_large)} 字符")
print(f"生成的 chunks 数量: {len(chunks_large)}")
print(f"耗时: {elapsed:.4f} 秒")
print(f"前3个 chunks: {chunks_large[:3]}")
print(f"最后3个 chunks: {chunks_large[-3:]}")
