"""调试正则表达式分隔符问题"""

import re

text = "item1,item2;item3"
separator_regex = r"[,;]"

print("测试 re.split 的行为:")
print(f"text: {text}")
print(f"separator: {separator_regex}")

result1 = re.split(separator_regex, text)
print(f"\nre.split('{separator_regex}', text):")
print(f"  结果: {result1}")

result2 = [s for s in re.split(separator_regex, text) if s]
print(f"\n过滤空字符串后:")
print(f"  结果: {result2}")

# 测试带括号的情况（捕获分隔符）
result3 = re.split(f"({separator_regex})", text)
print(f"\nre.split('({separator_regex})', text) - 捕获分隔符:")
print(f"  结果: {result3}")

# 测试空字符串分隔符
text2 = "Hello"
result4 = re.split("", text2)
print(f"\nre.split('', 'Hello'):")
print(f"  结果: {result4}")

result5 = list(text2)
print(f"\nlist('Hello'):")
print(f"  结果: {result5}")
