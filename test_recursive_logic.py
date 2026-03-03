"""测试 RecursiveTextSplitter 的逻辑正确性"""

from text_spliter.simple import RecursiveTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

print("=" * 80)
print("测试1：基本的递归切分")
print("=" * 80)

text1 = """Hello world!

This is a test.

Python is great."""

splitter_mine = RecursiveTextSplitter(separators=["\n\n", "\n", " ", ""], chunk_size=20, overlap_count=5)

splitter_langchain = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", " ", ""], chunk_size=20, chunk_overlap=5, keep_separator=False)

chunks_mine = splitter_mine.split_text(text1)
chunks_langchain = splitter_langchain.split_text(text1)

print("\n我的实现:")
for i, chunk in enumerate(chunks_mine, 1):
    print(f"  Chunk {i} (长度={len(chunk):2d}): [{chunk}]")

print("\nLangChain 实现:")
for i, chunk in enumerate(chunks_langchain, 1):
    print(f"  Chunk {i} (长度={len(chunk):2d}): [{chunk}]")

print("\n" + "=" * 80)
print("测试2：没有分隔符的长句子（应该按字符切分）")
print("=" * 80)

text2 = "Thisisaverylongsentencewithoutanyspaces"

chunks_mine2 = splitter_mine.split_text(text2)
chunks_langchain2 = splitter_langchain.split_text(text2)

print("\n我的实现:")
for i, chunk in enumerate(chunks_mine2, 1):
    print(f"  Chunk {i} (长度={len(chunk):2d}): [{chunk}]")

print("\nLangChain 实现:")
for i, chunk in enumerate(chunks_langchain2, 1):
    print(f"  Chunk {i} (长度={len(chunk):2d}): [{chunk}]")

print("\n" + "=" * 80)
print("测试3：包含不同层级分隔符的文本")
print("=" * 80)

text3 = "First sentence. Second sentence. Third sentence with more words here."

chunks_mine3 = splitter_mine.split_text(text3)
chunks_langchain3 = splitter_langchain.split_text(text3)

print("\n我的实现:")
for i, chunk in enumerate(chunks_mine3, 1):
    print(f"  Chunk {i} (长度={len(chunk):2d}): [{chunk}]")

print("\nLangChain 实现:")
for i, chunk in enumerate(chunks_langchain3, 1):
    print(f"  Chunk {i} (长度={len(chunk):2d}): [{chunk}]")

print("\n" + "=" * 80)
print("测试4：验证重叠功能")
print("=" * 80)

text4 = "a b c d e f g h i j k l m n o p q r s t u v w x y z"

splitter_overlap = RecursiveTextSplitter(separators=[" ", ""], chunk_size=10, overlap_count=3)

chunks_overlap = splitter_overlap.split_text(text4)

print("\n带重叠的切分 (chunk_size=10, overlap=3):")
for i, chunk in enumerate(chunks_overlap, 1):
    print(f"  Chunk {i} (长度={len(chunk):2d}): [{chunk}]")

print("\n验证重叠:")
for i in range(len(chunks_overlap) - 1):
    current = chunks_overlap[i]
    next_chunk = chunks_overlap[i + 1]
    # 找出重叠部分
    overlap_found = False
    for j in range(len(current)):
        if next_chunk.startswith(current[j:]):
            overlap_len = len(current[j:])
            print(f"  Chunk {i+1} 和 Chunk {i+2} 重叠: [{current[j:]}] (长度={overlap_len})")
            overlap_found = True
            break
    if not overlap_found:
        print(f"  ⚠️  Chunk {i+1} 和 Chunk {i+2} 没有发现重叠！")

print("\n" + "=" * 80)
print("测试5：中文文本")
print("=" * 80)

text5 = "我喜欢Python。我也喜欢AI。编程很有趣。"

splitter_chinese = RecursiveTextSplitter(separators=["。", " ", ""], chunk_size=15, overlap_count=3)

chunks_chinese = splitter_chinese.split_text(text5)

print("\n我的实现:")
for i, chunk in enumerate(chunks_chinese, 1):
    print(f"  Chunk {i} (长度={len(chunk):2d}): [{chunk}]")
