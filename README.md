# hello-rag: A Learnable RAG Implementation

A comprehensive, modular implementation of Retrieval-Augmented Generation (RAG) in Python. This project is designed as a learning tool to understand the full RAG pipeline from chunking to retrieval to generation, with a focus on clean, well-documented code.

## Project Overview

hello-rag implements the complete RAG pipeline:
1. **Chunking** - Text splitting strategies for optimal document segmentation
2. **Retrieval** - Vector embeddings, similarity search, and document retrieval
3. **Generation** - LLM integration, prompt engineering, and response generation
4. **Evaluation** - Metrics and testing for RAG system performance

## Architecture

The project follows a modular design:

```
hello-rag/
├── text_spliter/          # Text chunking strategies
│   ├── __init__.py
│   └── simple.py          # Simple and recursive text splitters
├── retrieval/             # Vector stores and embeddings
│   └── __init__.py
├── generation/           # LLM integration
│   └── __init__.py
├── evaluation/           # Metrics and testing
│   └── __init__.py
└── tests/               # Test suite
│   ├── __init__.py
│   └── test_simple.py
├── pyproject.toml        # Project configuration
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
├── AGENTS.md            # AI agent guidelines
└── LICENSE              # MIT License
```

## Current Status

Currently implemented:
- ✅ `TextSplitter` abstract base class
- ✅ `SimpleTextSplitter` - Basic character-based chunking
- ✅ `RecursiveTextSplitter` - Semantic-aware recursive splitting (with bug annotations)
- ✅ Comparison with LangChain's text splitters

Recently added:
- ✅ Project structure with modular directories
- ✅ Basic test suite for text_spliter
- ✅ Project configuration (pyproject.toml, requirements.txt)

Planned implementations:
- 🔄 Vector store integration (FAISS, Chroma) - *directory created*
- 🔄 Embedding models (OpenAI, sentence-transformers) - *directory created*
- 🔄 LLM integration (OpenAI, Anthropic, local models) - *directory created*
- 🔄 Evaluation framework (retrieval metrics, answer quality) - *directory created*

## Installation

### Prerequisites
- Python 3.10+
- UV package manager (recommended) or pip

### Setup with UV (Recommended)
```bash
# Clone the repository
git clone git@github.com:YogeLiu/hello-rag.git
cd hello-rag

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Unix/macOS
# .venv\Scripts\activate   # On Windows

# Install dependencies from pyproject.toml
uv sync
```

### Setup with pip
```bash
# Clone the repository
git clone git@github.com:YogeLiu/hello-rag.git
cd hello-rag

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Unix/macOS
# .venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Text Splitting
```python
from text_spliter.simple import SimpleTextSplitter, RecursiveTextSplitter

# Simple character-based splitting
splitter = SimpleTextSplitter(chunk_size=100, overlap_count=10)
chunks = splitter.split_text("Your long text here...")

# Recursive semantic splitting
recursive_splitter = RecursiveTextSplitter(
    separators=["\n\n", "\n", "。", "！", "？"],
    chunk_size=200,
    overlap_count=20
)
chunks = recursive_splitter.split_text("Your long text here...")
```

### Comparison with LangChain
The module includes comparison functionality with LangChain's text splitters:
```bash
python -m text_spliter.simple
```

## Development

### Installing Development Dependencies
```bash
# With UV
uv sync --group dev

# With pip
pip install -e ".[dev]"
```

### Running Tests
```bash
pytest
pytest tests/test_simple.py::test_specific_function
```

### Code Quality
```bash
black .                    # Format code
ruff check .              # Lint
ruff check --fix .        # Auto-fix lint issues
mypy text_spliter/        # Type checking
```

### Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Learning Resources

This project is designed as a learning tool. Key concepts covered:
- Text chunking strategies and their trade-offs
- Vector embeddings and similarity search
- Retrieval-augmented generation patterns
- LLM prompt engineering
- RAG evaluation metrics

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by LangChain's RAG implementation
- Built for educational purposes to understand RAG systems deeply