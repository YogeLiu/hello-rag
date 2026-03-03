"""测试保留分隔符的版本"""

from text_spliter.simple import RecursiveTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

print("=" * 80)
print("测试1：基本文本切分（验证空格是否保留）")
print("=" * 80)

text1 = "Hello world. How are you? I am fine."

splitter_mine = RecursiveTextSplitter(separators=["\n\n", "\n", " ", ""], chunk_size=20, overlap_count=5)

splitter_langchain = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", " ", ""], chunk_size=20, chunk_overlap=5, keep_separator=False)

chunks_mine = splitter_mine.split_text(text1)
chunks_langchain = splitter_langchain.split_text(text1)

print(f"\n原文本: {text1}")
print(f"长度: {len(text1)}\n")

print("我的实现:")
for i, chunk in enumerate(chunks_mine, 1):
    print(f"  Chunk {i} (长度={len(chunk):2d}): [{chunk}]")

print("\nLangChain 实现:")
for i, chunk in enumerate(chunks_langchain, 1):
    print(f"  Chunk {i} (长度={len(chunk):2d}): [{chunk}]")

print("\n" + "=" * 80)
print("测试2：多段落文本")
print("=" * 80)

text2 = """Hello world!

This is a test.

Python is great."""

chunks_mine2 = splitter_mine.split_text(text2)
chunks_langchain2 = splitter_langchain.split_text(text2)

print("\n我的实现:")
for i, chunk in enumerate(chunks_mine2, 1):
    print(f"  Chunk {i} (长度={len(chunk):2d}): [{chunk}]")

print("\nLangChain 实现:")
for i, chunk in enumerate(chunks_langchain2, 1):
    print(f"  Chunk {i} (长度={len(chunk):2d}): [{chunk}]")

print("\n" + "=" * 80)
print("测试3：验证重叠（空格是否保留）")
print("=" * 80)

text3 = "a b c d e f g h i j k l"

splitter_overlap = RecursiveTextSplitter(separators=[" ", ""], chunk_size=10, overlap_count=3)

chunks_overlap = splitter_overlap.split_text(text3)

print(f"\n原文本: {text3}")
print(f"Chunk size: 10, Overlap: 3\n")

print("我的实现:")
for i, chunk in enumerate(chunks_overlap, 1):
    print(f"  Chunk {i} (长度={len(chunk):2d}): [{chunk}]")

print("\n验证相邻块的重叠:")
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
print("测试4：长句子（空格保留测试）")
print("=" * 80)

text4 = "First sentence. Second sentence. Third sentence with more words here."

chunks_mine4 = splitter_mine.split_text(text4)
chunks_langchain4 = splitter_langchain.split_text(text4)

print("\n我的实现:")
for i, chunk in enumerate(chunks_mine4, 1):
    print(f"  Chunk {i} (长度={len(chunk):2d}): [{chunk}]")

print("\nLangChain 实现:")
for i, chunk in enumerate(chunks_langchain4, 1):
    print(f"  Chunk {i} (长度={len(chunk):2d}): [{chunk}]")

print("\n" + "=" * 80)
print("测试5：中文标点符号")
print("=" * 80)

text5 = "我喜欢Python。我也喜欢AI。编程很有趣。"

splitter_chinese = RecursiveTextSplitter(separators=["。", " ", ""], chunk_size=15, overlap_count=3)

chunks_chinese = splitter_chinese.split_text(text5)

print(f"\n原文本: {text5}\n")

print("我的实现:")
for i, chunk in enumerate(chunks_chinese, 1):
    print(f"  Chunk {i} (长度={len(chunk):2d}): [{chunk}]")

print("\n" + "=" * 80)
print("测试6：正则表达式分隔符")
print("=" * 80)

text6 = "item1,item2;item3,item4;item5"

splitter_regex = RecursiveTextSplitter(separators=[r"[,;]", ""], chunk_size=15, overlap_count=0, is_separator_regex=True)

chunks_regex = splitter_regex.split_text(text6)

print(f"\n原文本: {text6}\n")

print("我的实现:")
for i, chunk in enumerate(chunks_regex, 1):
    print(f"  Chunk {i} (长度={len(chunk):2d}): [{chunk}]")

print("\n✅ 注意：正则表达式分隔符被移除是正常的")

print("\n" + "=" * 80)
print("测试7：无分隔符的长文本（字符级切分）")
print("=" * 80)

text7 = "Thisisaverylongsentencewithoutanyspaces"

chunks_mine7 = splitter_mine.split_text(text7)
chunks_langchain7 = splitter_langchain.split_text(text7)

print(f"\n原文本: {text7}\n")

print("我的实现:")
for i, chunk in enumerate(chunks_mine7, 1):
    print(f"  Chunk {i} (长度={len(chunk):2d}): [{chunk}]")

print("\nLangChain 实现:")
for i, chunk in enumerate(chunks_langchain7, 1):
    print(f"  Chunk {i} (长度={len(chunk):2d}): [{chunk}]")

print("\n" + "=" * 80)
print("✅ 所有测试完成！")
print("=" * 80)
