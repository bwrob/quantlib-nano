"""Tests for scraper configuration and HTML processing."""

from pathlib import Path

import pytest

from utils.knowledge_scraper import DocProcessor, ScraperConfig

MOCK_CONFIG = """
[sources.nanobind]
url = "https://github.com/wjakob/nanobind"
type = "git"

[sources.litgen]
url = "https://github.com/pthom/litgen"
type = "git"

[sources.quantlib_html]
url = "https://www.quantlib.org/reference/"
type = "web"
"""


def test_load_config(tmp_path: Path) -> None:
    """Test loading configuration from TOML."""
    config_file = tmp_path / "sources.toml"
    _ = config_file.write_text(MOCK_CONFIG)

    sources = ScraperConfig.from_toml(str(config_file))

    num_sources = 3
    assert len(sources) == num_sources
    assert sources["nanobind"].url == "https://github.com/wjakob/nanobind"
    assert sources["nanobind"].source_type == "git"
    assert sources["quantlib_html"].source_type == "web"


def test_config_file_not_found() -> None:
    """Test handling of missing configuration file."""
    with pytest.raises(FileNotFoundError):
        _ = ScraperConfig.from_toml("non_existent.toml")


def test_html_to_markdown() -> None:
    """Test HTML to Markdown conversion."""
    html = """
    <html>
        <nav>Navigation</nav>
        <main>
            <h1>Title</h1>
            <p>Hello World</p>
        </main>
        <footer>Footer</footer>
    </html>
    """
    markdown = DocProcessor.html_to_markdown(html)
    assert "# Title" in markdown
    assert "Hello World" in markdown
    assert "Navigation" not in markdown
    assert "Footer" not in markdown
