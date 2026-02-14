import pytest
import os
import toml
from knowledge_scraper import ScraperConfig, ScraperSource, DocProcessor

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

def test_load_config(tmp_path):
    config_file = tmp_path / "sources.toml"
    config_file.write_text(MOCK_CONFIG)
    
    sources = ScraperConfig.from_toml(str(config_file))
    
    assert len(sources) == 3
    assert sources["nanobind"].url == "https://github.com/wjakob/nanobind"
    assert sources["nanobind"].type == "git"
    assert sources["quantlib_html"].type == "web"

def test_config_file_not_found():
    with pytest.raises(FileNotFoundError):
        ScraperConfig.from_toml("non_existent.toml")

def test_html_to_markdown():
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
