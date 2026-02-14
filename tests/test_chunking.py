"""Tests for DocProcessor chunking logic."""

from utils.knowledge_scraper import DocProcessor


def test_chunk_markdown_small() -> None:
    """Test that small content is not split."""
    content = "# Title\nSome text."
    max_chars = 100
    chunks = DocProcessor.chunk_markdown(content, max_chars=max_chars)
    num_chunks = 1
    assert len(chunks) == num_chunks
    assert chunks[0] == content


def test_chunk_markdown_split_by_header() -> None:
    """Test splitting content by headers."""
    content = "# Section 1\nContent 1\n\n# Section 2\nContent 2"
    # Max chars 30 should force a split between Section 1 and Section 2
    max_chars = 30
    chunks = DocProcessor.chunk_markdown(content, max_chars=max_chars)
    num_chunks = 2
    assert len(chunks) == num_chunks
    assert "# Section 1" in chunks[0]
    assert "# Section 2" in chunks[1]


def test_chunk_markdown_fallback_split() -> None:
    """Test fallback splitting when no headers are present."""
    # Content with no headers but exceeds limit
    max_chars = 40
    content = "A" * 100
    chunks = DocProcessor.chunk_markdown(content, max_chars=max_chars)
    num_chunks = 3
    assert len(chunks) == num_chunks
    assert len(chunks[0]) <= max_chars
    assert len(chunks[1]) <= max_chars
    assert len(chunks[2]) <= max_chars
