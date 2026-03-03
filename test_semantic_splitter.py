"""Test semantic text splitter with different configurations."""

from text_spliter.simple import SemanticTextSplitter

def test_basic_semantic_splitting():
    """Test basic semantic splitting with topic changes."""
    text = """
    Python is a high-level programming language. It was created by Guido van Rossum.
    Python emphasizes code readability and simplicity.
    
    Machine learning is a subset of artificial intelligence. It focuses on algorithms that learn from data.
    Deep learning uses neural networks with multiple layers.
    
    The weather today is sunny and warm. Tomorrow will be cloudy with a chance of rain.
    Weather patterns are influenced by many factors.
    """
    
    splitter = SemanticTextSplitter(
        chunk_size=500,
        buffer_size=1,
        breakpoint_type="percentile",
        breakpoint_threshold=75.0
    )
    
    chunks = splitter.split_text(text)
    
    print("=== Basic Semantic Splitting (threshold=75) ===")
    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i+1} (len={len(chunk)}):")
        print(chunk)
    print(f"\nTotal chunks: {len(chunks)}")


def test_buffer_size_comparison():
    """Compare buffer_size=1 vs buffer_size=3."""
    text = """
    The Renaissance was a cultural movement in Europe. It began in Italy during the 14th century.
    Renaissance art emphasized realism and human emotion. Leonardo da Vinci was a master of this style.
    
    The Industrial Revolution transformed manufacturing. It started in Britain in the 18th century.
    Steam engines powered new factories. This led to rapid urbanization.
    
    Climate change affects global temperatures. Rising CO2 levels are the primary cause.
    Scientists predict more extreme weather events. International cooperation is essential.
    """
    
    print("\n" + "="*80)
    print("=== Buffer Size Comparison ===")
    
    for buffer_size in [1, 3]:
        splitter = SemanticTextSplitter(
            chunk_size=500,
            buffer_size=buffer_size,
            breakpoint_type="percentile",
            breakpoint_threshold=80.0
        )
        
        chunks = splitter.split_text(text)
        print(f"\n--- Buffer Size = {buffer_size} ---")
        print(f"Chunks created: {len(chunks)}")
        for i, chunk in enumerate(chunks):
            print(f"\nChunk {i+1} ({len(chunk)} chars):")
            print(chunk[:150] + "..." if len(chunk) > 150 else chunk)


def test_threshold_comparison():
    """Compare different percentile thresholds."""
    text = """
    Artificial intelligence is transforming technology. Machine learning enables computers to learn.
    Deep learning uses neural networks. Neural networks mimic the human brain.
    
    Python is popular for AI development. It has many libraries like TensorFlow.
    PyTorch is another popular framework. Both are widely used in research.
    
    Cloud computing provides scalable resources. AWS and Azure are major providers.
    Serverless architectures reduce operational overhead. They automatically scale based on demand.
    """
    
    print("\n" + "="*80)
    print("=== Threshold Comparison ===")
    
    for threshold in [70, 80, 90, 95]:
        splitter = SemanticTextSplitter(
            chunk_size=500,
            buffer_size=1,
            breakpoint_type="percentile",
            breakpoint_threshold=threshold
        )
        
        chunks = splitter.split_text(text)
        print(f"\nThreshold = {threshold}%: {len(chunks)} chunks")
        avg_length = sum(len(c) for c in chunks) / len(chunks)
        print(f"Average chunk length: {avg_length:.0f} chars")


def test_breakpoint_types():
    """Compare different breakpoint detection methods."""
    text = """
    Quantum computing uses quantum mechanics principles. Qubits can exist in superposition states.
    Quantum entanglement enables faster computation. This technology is still experimental.
    
    Blockchain is a distributed ledger technology. It enables secure decentralized transactions.
    Bitcoin was the first cryptocurrency application. Ethereum added smart contract functionality.
    
    Virtual reality creates immersive experiences. VR headsets track head and hand movements.
    Augmented reality overlays digital content. AR is used in gaming and education.
    """
    
    print("\n" + "="*80)
    print("=== Breakpoint Type Comparison ===")
    
    for bp_type in ["percentile", "std", "interquartile"]:
        splitter = SemanticTextSplitter(
            chunk_size=500,
            buffer_size=1,
            breakpoint_type=bp_type,
            breakpoint_threshold=2.0 if bp_type == "std" else 85.0
        )
        
        chunks = splitter.split_text(text)
        print(f"\nBreakpoint type '{bp_type}': {len(chunks)} chunks")


def test_chinese_text():
    """Test semantic splitting with Chinese text."""
    text = """
    人工智能正在改变世界。机器学习让计算机能够自主学习。深度学习使用多层神经网络。
    这些技术在图像识别中表现出色。
    
    区块链是一种分布式账本技术。它可以实现去中心化的交易。比特币是第一个加密货币应用。
    以太坊增加了智能合约功能。
    
    气候变化影响全球温度。二氧化碳排放是主要原因。科学家预测会有更多极端天气事件。
    国际合作至关重要。
    """
    
    print("\n" + "="*80)
    print("=== Chinese Text Semantic Splitting ===")
    
    splitter = SemanticTextSplitter(
        chunk_size=500,
        buffer_size=1,
        breakpoint_type="percentile",
        breakpoint_threshold=80.0
    )
    
    chunks = splitter.split_text(text)
    print(f"Total chunks: {len(chunks)}")
    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i+1} ({len(chunk)} chars):")
        print(chunk)


if __name__ == "__main__":
    test_basic_semantic_splitting()
    test_buffer_size_comparison()
    test_threshold_comparison()
    test_breakpoint_types()
    test_chinese_text()
    
    print("\n" + "="*80)
    print("✅ All tests completed!")
