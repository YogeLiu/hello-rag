"""测试极端情况：没有任何分隔符的超长文本"""

from langchain_text_splitters import RecursiveCharacterTextSplitter

# 极端情况1：没有空格、换行的超长英文
text1 = "Thisisaverylongsentencewithoutanyspacesornewlinesatallanditwillbeforcedtosplitbycharacters"
print(f"文本1长度: {len(text1)}")
print(f"文本1内容: {text1}\n")

splitter1 = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", " ", ""], chunk_size=20, chunk_overlap=5, keep_separator=False)

chunks1 = splitter1.split_text(text1)
print("=" * 60)
print("结果1: 英文无分隔符文本")
print("=" * 60)
for i, chunk in enumerate(chunks1, 1):
    print(f"Chunk {i} (长度={len(chunk)}): [{chunk}]")

print("\n\n")

# 极端情况2：中文没有标点符号
text2 = "这是一个非常非常非常长的中文句子没有任何标点符号也没有空格就是这样一直写下去看看会怎么样"
print(f"文本2长度: {len(text2)}")
print(f"文本2内容: {text2}\n")

splitter2 = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", "。", "，", " ", ""], chunk_size=15, chunk_overlap=3, keep_separator=False)

chunks2 = splitter2.split_text(text2)
print("=" * 60)
print("结果2: 中文无标点符号文本")
print("=" * 60)
for i, chunk in enumerate(chunks2, 1):
    print(f"Chunk {i} (长度={len(chunk)}): [{chunk}]")

print("\n\n")

# 极端情况3：非常长的单词（如URL或base64编码）
text3 = "https://example.com/api/v1/users/12345/posts/67890?query=abcdefghijklmnopqrstuvwxyz&token=ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789"
print(f"文本3长度: {len(text3)}")
print(f"文本3内容: {text3}\n")

splitter3 = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", " ", ""], chunk_size=30, chunk_overlap=5, keep_separator=False)

chunks3 = splitter3.split_text(text3)
print("=" * 60)
print("结果3: 超长URL")
print("=" * 60)
for i, chunk in enumerate(chunks3, 1):
    print(f"Chunk {i} (长度={len(chunk)}): [{chunk}]")

print("\n\n")

# 极端情况4：如果去掉空字符串分隔符会怎样？
print("=" * 60)
print("极端测试：如果 separators 中没有空字符串会怎样？")
print("=" * 60)

try:
    splitter4 = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", " "], chunk_size=20, chunk_overlap=5, keep_separator=False)  # 注意：没有 ""

    chunks4 = splitter4.split_text(text1)
    print("结果4:")
    for i, chunk in enumerate(chunks4, 1):
        print(f"Chunk {i} (长度={len(chunk)}): [{chunk}]")
except Exception as e:
    print(f"错误: {e}")
