"""Tests for web scraping with Betamax mocking."""

from pathlib import Path

import requests
from betamax import Betamax  # pyright: ignore[reportMissingTypeStubs]

from utils.knowledge_scraper import KnowledgeScraper

with Betamax.configure() as config:
    config.cassette_library_dir = "tests/cassettes"


def test_fetch_web(tmp_path: Path) -> None:
    """Test fetching a web page using Betamax recorded cassette."""
    # Create a mock config for the test
    config_file = tmp_path / "sources.toml"
    _ = config_file.write_text("""
[sources.example]
url = "http://example.com"
type = "web"
""")

    output_dir = tmp_path / ".knowledge"
    session = requests.Session()
    recorder = Betamax(session)

    with recorder.use_cassette("example-web"):  # pyright: ignore[reportUnknownMemberType]
        scraper = KnowledgeScraper(str(config_file), str(output_dir), session=session)
        source = scraper.config["example"]
        _ = scraper.fetch_web(source)

    # Verify file was created
    expected_file = output_dir / "example" / "example.com.md"
    assert expected_file.exists()
    content = expected_file.read_text()
    assert "Example Domain" in content
