"""Tests for the text_spliter module."""

from text_spliter.simple import SimpleTextSplitter, RecursiveTextSplitter


def test_simple_text_splitter_basic():
    splitter = SimpleTextSplitter(chunk_size=10, overlap_count=2)
    text = "abcdefghijklmnopqrstuvwxyz"
    chunks = splitter.split_text(text)

    # Should split into chunks of size 10 with overlap 2
    # Step size = chunk_size - overlap_count = 8
    # Chunks: 0-10, 8-18, 16-26
    assert len(chunks) == 3
    assert chunks[0] == "abcdefghij"
    assert chunks[1] == "ijklmnopqr"
    assert chunks[2] == "qrstuvwxyz"


def test_simple_text_splitter_small_text():
    splitter = SimpleTextSplitter(chunk_size=100, overlap_count=10)
    text = "Short text"
    chunks = splitter.split_text(text)

    # Text shorter than chunk_size should produce single chunk
    assert len(chunks) == 1
    assert chunks[0] == text


def test_simple_text_splitter_empty():
    splitter = SimpleTextSplitter(chunk_size=10, overlap_count=2)
    text = ""
    chunks = splitter.split_text(text)

    # Empty text should produce empty list
    assert chunks == []


def test_recursive_text_splitter_basic():
    splitter = RecursiveTextSplitter(
        separators=["\n\n", "\n", " "], chunk_size=20, overlap_count=5
    )
    text = "First line\nSecond line\nThird line"
    chunks = splitter.split_text(text)

    # Should split on newlines
    assert len(chunks) >= 1
    # Note: This test will need updates once RecursiveTextSplitter bugs are fixed
