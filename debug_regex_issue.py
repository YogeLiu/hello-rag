"""调试正则表达式分隔符问题"""

import re

text = "item1,item2;item3"
separator = r"[,;]"

print("测试 re.split 行为:")
print(f"text: {text}")
print(f"separator: {separator}\n")

segments = re.split(separator, text)
print(f"re.split('{separator}', text):")
print(f"  结果: {segments}\n")

# 测试 join
joined = separator.join(segments)
print(f"'{separator}'.join({segments}):")
print(f"  结果: {joined}\n")

# 这就是问题所在！join 会把字面的 '[,;]' 插入

print("=" * 60)
print("关键发现：")
print("=" * 60)
print("问题：re.split() 移除了分隔符，但我们又用 separator.join() 插入回去")
print("但正则表达式的分隔符不是单一字符，而是模式！")
print("\n解决方案：")
print("1. 对于正则表达式分隔符，不应该重新插入")
print("2. 或者需要知道实际匹配到的分隔符是什么（需要捕获组）")
