"""单独测试正则表达式切分"""

from text_spliter.simple import RecursiveTextSplitter

text = "item1,item2;item3,item4;item5"
print(f"原文本: {text}")
print(f"长度: {len(text)}")

splitter = RecursiveTextSplitter(separators=[r"[,;]", ""], chunk_size=15, overlap_count=0, is_separator_regex=True)

chunks = splitter.split_text(text)
print(f"\n结果:")
for i, chunk in enumerate(chunks, 1):
    print(f"  Chunk {i} (长度={len(chunk):2d}): [{chunk}]")

# 手动跟踪执行过程
print("\n手动跟踪:")
import re

separators = [r"[,;]", ""]
separator = r"[,;]"
separator_regex = separator  # is_separator_regex=True

print(f"separator_regex: {separator_regex}")

segments = [s for s in re.split(separator_regex, text) if s]
print(f"segments: {segments}")

for seg in segments:
    print(f"  segment: [{seg}], len={len(seg)}")
