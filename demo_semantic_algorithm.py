"""Demonstrate the semantic splitting algorithm with mock embeddings."""

import numpy as np

def demonstrate_algorithm():
    """Show the step-by-step semantic chunking algorithm."""
    
    print("="*80)
    print("标准语义分割算法演示")
    print("="*80)
    
    # 示例文本：三个不同主题
    sentences = [
        "Python is a programming language.",           # Topic 1: Python
        "It emphasizes code readability.",             # Topic 1: Python
        "Python has many libraries.",                  # Topic 1: Python
        "Machine learning uses algorithms.",           # Topic 2: ML (主题切换)
        "Neural networks learn from data.",            # Topic 2: ML
        "Deep learning has multiple layers.",          # Topic 2: ML
        "The weather today is sunny.",                 # Topic 3: Weather (主题切换)
        "Tomorrow will be cloudy."                     # Topic 3: Weather
    ]
    
    print("\n步骤 1: 句子分割")
    print("-" * 80)
    for i, s in enumerate(sentences):
        print(f"S{i}: {s}")
    
    # 模拟 embeddings (实际中由模型生成)
    # 相同主题的句子 embedding 相似，不同主题的差异大
    print("\n步骤 2: 生成 Embeddings (模拟)")
    print("-" * 80)
    print("实际运行: embeddings = model.encode(sentences)")
    print("这里用模拟数据展示...")
    
    embeddings = np.array([
        [1.0, 0.9, 0.1, 0.1],  # S0 - Python主题向量
        [0.9, 1.0, 0.1, 0.0],  # S1 - Python主题向量
        [1.0, 0.8, 0.2, 0.1],  # S2 - Python主题向量
        [0.1, 0.2, 1.0, 0.1],  # S3 - ML主题向量 (主题切换!)
        [0.2, 0.1, 0.9, 0.2],  # S4 - ML主题向量
        [0.1, 0.1, 1.0, 0.1],  # S5 - ML主题向量
        [0.1, 0.1, 0.1, 1.0],  # S6 - Weather主题向量 (主题切换!)
        [0.0, 0.2, 0.1, 0.9],  # S7 - Weather主题向量
    ])
    
    # 计算相邻句子的余弦相似度
    print("\n步骤 3: 计算相邻句子的余弦相似度")
    print("-" * 80)
    
    def cosine_similarity(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    similarities = []
    for i in range(len(embeddings) - 1):
        sim = cosine_similarity(embeddings[i], embeddings[i + 1])
        similarities.append(sim)
        status = "📌 LOW (breakpoint!)" if sim < 0.7 else "✓ high (same topic)"
        print(f"similarity(S{i}, S{i+1}) = {sim:.3f}  {status}")
    
    # 计算阈值
    print("\n步骤 4: 计算分割阈值")
    print("-" * 80)
    
    percentile_95 = np.percentile(similarities, 95)
    percentile_80 = np.percentile(similarities, 80)
    percentile_20 = np.percentile(similarities, 20)
    
    print(f"所有相似度: {[f'{s:.3f}' for s in similarities]}")
    print(f"最小值: {min(similarities):.3f}")
    print(f"最大值: {max(similarities):.3f}")
    print(f"平均值: {np.mean(similarities):.3f}")
    print(f"\n95 percentile (你的原始想法): {percentile_95:.3f}")
    print(f"80 percentile: {percentile_80:.3f}")
    print(f"20 percentile (反向阈值): {percentile_20:.3f}")
    
    # 方法对比
    print("\n步骤 5: 不同阈值策略对比")
    print("-" * 80)
    
    # 错误方法 1: 使用 distance 的 95 percentile
    print("\n❌ 错误方法 1: 使用 cosine distance 的 95 percentile")
    distances = [1 - s for s in similarities]
    distance_threshold_95 = np.percentile(distances, 95)
    print(f"Distance 95 percentile = {distance_threshold_95:.3f}")
    print(f"这意味着: 只在 distance > {distance_threshold_95:.3f} 时分割")
    breakpoints_wrong1 = [i+1 for i, d in enumerate(distances) if d > distance_threshold_95]
    print(f"分割点: {breakpoints_wrong1}")
    print(f"问题: 分割点太少！只能找到最极端的主题变化")
    
    # 正确方法 1: 使用 similarity 的低百分位或固定阈值
    print("\n✅ 正确方法 1: 使用 similarity < 阈值")
    fixed_threshold = 0.70
    print(f"固定阈值 = {fixed_threshold}")
    breakpoints_correct1 = [i+1 for i, s in enumerate(similarities) if s < fixed_threshold]
    print(f"分割点: {breakpoints_correct1} (在 S{breakpoints_correct1[0]} 和 S{breakpoints_correct1[1]} 之前分割)")
    
    # 正确方法 2: 使用 similarity 的 20 percentile (反向)
    print("\n✅ 正确方法 2: 使用 similarity 的低百分位 (20%)")
    threshold_20 = percentile_20
    print(f"20 percentile = {threshold_20:.3f}")
    breakpoints_correct2 = [i+1 for i, s in enumerate(similarities) if s < threshold_20]
    print(f"分割点: {breakpoints_correct2}")
    
    # 展示分块结果
    print("\n步骤 6: 生成最终分块")
    print("-" * 80)
    
    def create_chunks(sentences, breakpoint_indices):
        chunks = []
        start = 0
        for bp in breakpoint_indices:
            chunks.append(" ".join(sentences[start:bp]))
            start = bp
        chunks.append(" ".join(sentences[start:]))
        return chunks
    
    chunks = create_chunks(sentences, breakpoints_correct1)
    print(f"\n使用固定阈值 0.70 的结果: {len(chunks)} 个块")
    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i+1}:")
        print(f"  {chunk}")
    
    print("\n" + "="*80)
    print("关键发现")
    print("="*80)
    print("""
1. ✅ 使用 cosine SIMILARITY (不是 distance)
2. ✅ 在相似度 **低** 的地方分割 (similarity < threshold)
3. ✅ 阈值通常是 0.65-0.85 或使用较低的百分位 (如 20-30%)
4. ❌ 你的原始代码用 distance 的 95 percentile，会导致分割点太少

标准做法:
- similarity < 0.75  (固定阈值法)
- similarity < np.percentile(similarities, 20)  (动态阈值法)

而不是:
- distance > np.percentile(distances, 95)  (你的原始方法)
    """)


def demonstrate_your_original_logic():
    """展示你原始代码的逻辑问题."""
    print("\n" + "="*80)
    print("你的原始代码逻辑问题分析")
    print("="*80)
    
    print("\n原始代码 Line 182-183:")
    print("```python")
    print("for e1, e2 in zip(distance, distance[1:]):")
    print("    distance.append(self.__consine_dis(e1, e2))")
    print("```")
    
    print("\n问题分析:")
    print("1. distance 初始化为 []，zip([], []) 永远不执行")
    print("2. 即使 distance 有值，在循环中 append 会造成无限循环")
    print("3. 对 distance 值（标量）调用 __consine_dis 没有意义")
    print("   - distance[0] = 0.3 (标量)")
    print("   - distance[1] = 0.5 (标量)")
    print("   - __consine_dis(0.3, 0.5) 要求输入是向量，不是标量!")
    
    print("\n原始代码 Line 188-189:")
    print("```python")
    print("for i, (e1, e2) in enumerate(zip(distance[:-1], distance[1:])):")
    print("    if self.__consine_dis(e1, e2) > sort_distance[index]:")
    print("```")
    
    print("\n问题分析:")
    print("1. 再次对 distance 值调用 __consine_dis，概念错误")
    print("2. distance 已经是计算好的标量值，应该直接比较")
    print("3. 应该是: if distance[i] > threshold")


if __name__ == "__main__":
    demonstrate_algorithm()
    demonstrate_your_original_logic()
