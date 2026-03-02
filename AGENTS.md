# Agent Guidelines for hello-rag

This document provides guidelines for AI agents working on the `hello-rag` project, a learnable Python-based RAG (Retrieval-Augmented Generation) implementation.

## Project Overview

- **Project**: hello-rag - A learnable RAG implementation covering the full pipeline: chunking, retrieval, generation, and evaluation
- **Language**: Python 3.10+
- **Package manager**: UV (used for virtual environment and dependency management)
- **Architecture**: Modular components implementing the RAG pipeline:
  - **Chunking**: Text splitting strategies (currently in `text_spliter/`)
  - **Retrieval**: Vector stores, embedding models, similarity search
  - **Generation**: LLM integration, prompt engineering, response generation
  - **Evaluation**: Metrics, testing, quality assessment
- **Dependencies**: LangChain (for comparison), Pydantic (for data models), embedding models, vector databases, and LLM SDKs.
- **Current state**: The project currently has a `text_spliter/` module with bug annotations and missing implementations (see `text_spliter/simple.py`).
- **Learning approach**: This is a learnable project where the user will implement components. Agents should:
  - Help with scaffolding, project structure, and documentation
  - Fix bugs in existing code (like those annotated in `text_spliter/simple.py`)
  - Provide guidance and references, but NOT implement core RAG features
  - Use LangChain only as a reference for learning, not for implementation

## Environment Setup

1. **Virtual environment**: Already set up via UV at `.venv`. Activate with `source .venv/bin/activate` (Unix) or `.venv\Scripts\activate` (Windows).
2. **Install dependencies**: If missing, run `uv sync` (if `pyproject.toml` exists). Use `uv pip install` for individual packages.
3. **Development dependencies**: No explicit dev dependencies yet; consider adding `pytest`, `black`, `ruff`, `mypy`, `isort`.

## Build, Lint, and Test Commands

Since no explicit build system is defined, the following commands are recommended for agents to run **after making changes** to ensure code quality.

### Running Tests
- **Run all tests**: `pytest` (requires `pytest` installed)
- **Run a specific test file**: `pytest path/to/test_file.py`
- **Run a single test**: `pytest path/to/test_file.py::test_function_name`
- **Run tests with coverage**: `pytest --cov=text_spliter`

**Note**: Currently there are basic test files. When creating tests, place them in a `tests/` directory mirroring the module structure (e.g., `tests/test_simple.py`).

### Manual Testing
- **Run the module directly**: `python -m text_spliter.simple` (prints test output).
- **Compare with LangChain**: The module includes a comparison with `langchain_text_splitters.RecursiveCharacterTextSplitter` in the `__main__` block.

### Linting and Formatting
- **Format code with Black**: `black .`
- **Sort imports with isort**: `isort .`
- **Lint with Ruff**: `ruff check .`
- **Auto‑fix lint issues**: `ruff check --fix .`

### Type Checking
- **Run mypy**: `mypy text_spliter/`
- **Strict type checking**: `mypy --strict text_spliter/`

### Pre‑commit Hooks
If a `.pre-commit-config.yaml` is added, run `pre-commit run --all-files` before committing.

## Code Style Guidelines

Follow the existing patterns observed in `text_spliter/simple.py`.

### Indentation and Line Length
- **Indentation**: 4 spaces per level (no tabs).
- **Line length**: 88 characters (Black default). If Black is not used, keep lines under 100 characters.

### Imports
- **Grouping**: Standard library imports first, then third‑party imports, then local imports. Separate each group with a blank line.
- **Absolute imports**: Use absolute imports for local modules (e.g., `from text_spliter.simple import SimpleTextSplitter`).
- **Avoid wildcard imports**: Never use `from module import *`.
- **Import order**: Alphabetical within each group (isort can enforce this).

Example:
```python
from abc import ABC, abstractmethod
from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter
```

### Naming Conventions
- **Classes**: `PascalCase` (e.g., `TextSplitter`, `SimpleTextSplitter`).
- **Functions and methods**: `snake_case` (e.g., `split_text`, `__recursive_split`).
- **Variables and parameters**: `snake_case`.
- **Constants**: `UPPER_SNAKE_CASE`.
- **Private methods**: Prefix with `__` (double underscore) for truly private methods (e.g., `__recursive_split`). Use a single underscore `_` for protected methods.

### Type Annotations
- **Always use type hints** for function/method signatures and, where helpful, for local variables.
- **Return type**: Explicitly annotate return type, even if `None`.
- **Use `list[str]` over `List[str]`** (Python 3.9+ style).
- **Prefer `typing` types when needed** (`Optional`, `Union`, `Any`, etc.).

Example:
```python
def split_text(self, text: str) -> list[str]:
    ...
```

### String Quotes
- **Use double quotes** (`"`) for string literals, unless the string contains double quotes inside (then use single quotes).
- **Triple‑double‑quotes** for docstrings and multi‑line strings.

### Error Handling
- **Exceptions**: Raise built‑in exceptions where appropriate (`ValueError`, `TypeError`, `RuntimeError`).
- **Custom exceptions**: Define custom exception classes if needed, inheriting from `Exception`.
- **Avoid bare `except:`**: Always catch specific exceptions.
- **Use `try`‑`except`‑`else`‑`finally`** where it improves clarity.

### Documentation
- **Docstrings**: Use triple‑double‑quoted docstrings for all public modules, classes, and functions/methods.
- **Style**: Google‑style or NumPy‑style docstrings (choose one and be consistent).
- **Comments**: Use comments sparingly to explain “why” rather than “what”. The existing code uses comments to describe bugs and missing implementations; follow that pattern when noting TODOs.

### Class Design
- **Abstract base classes**: Inherit from `ABC` and use `@abstractmethod` for methods that must be implemented.
- **Constructor**: Keep `__init__` simple; validate parameters and assign them to instance variables.
- **Property decorators**: Use `@property` for computed attributes that are expensive or should be read‑only.

### Testing Style
- **Test framework**: `pytest`.
- **Test naming**: `test_<function_name>_<scenario>`.
- **Fixtures**: Use `pytest.fixture` for shared setup.
- **Assertions**: Use plain `assert` statements; `pytest` will provide rich failure output.
- **Mocking**: Use `unittest.mock` or `pytest‑mock`.

## Commit Conventions

- **Commit messages**: Use the conventional commits format (e.g., `feat: add recursive splitter`, `fix: preserve separators in recursive split`).
- **Scope**: Optionally include a scope in parentheses: `feat(text_spliter): ...`.
- **Body**: Explain the “why” and any breaking changes.
- **Footer**: Reference issue numbers (`Closes #123`).

## Cursor / Copilot Rules

No project‑specific Cursor or Copilot rules have been defined. If you add them, place them in `.cursor/rules/` or `.github/copilot-instructions.md` and update this section.

## Quick Reference for Agents

After making changes, run at least:

```bash
black .                   # formatting
ruff check .              # linting
mypy text_spliter/        # type checking
pytest                    # tests (when tests exist)
```

If any command fails, fix the issues before committing.

---
*This file was generated by an AI agent. Update it as the project evolves.*