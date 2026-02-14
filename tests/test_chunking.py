import pytest
from knowledge_scraper import DocProcessor

def test_chunk_markdown_small():
    content = "# Title\nSome text."
    chunks = DocProcessor.chunk_markdown(content, max_chars=100)
    assert len(chunks) == 1
    assert chunks[0] == content

def test_chunk_markdown_split_by_header():
    content = "# Section 1\nContent 1\n\n# Section 2\nContent 2"
    # Max chars 30 should force a split between Section 1 and Section 2
    chunks = DocProcessor.chunk_markdown(content, max_chars=30)
    assert len(chunks) == 2
    assert "# Section 1" in chunks[0]
    assert "# Section 2" in chunks[1]

def test_chunk_markdown_fallback_split():
    # Content with no headers but exceeds limit
    content = "A" * 100
    chunks = DocProcessor.chunk_markdown(content, max_chars=40)
    assert len(chunks) == 3
    assert len(chunks[0]) <= 40
    assert len(chunks[1]) <= 40
    assert len(chunks[2]) <= 40
