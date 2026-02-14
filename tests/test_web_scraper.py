import pytest
import os
import requests
from betamax import Betamax
from utils.knowledge_scraper import KnowledgeScraper, ScraperSource

with Betamax.configure() as config:
    config.cassette_library_dir = 'tests/cassettes'

def test_fetch_web(tmp_path):
    # Create a mock config for the test
    config_file = tmp_path / "sources.toml"
    config_file.write_text("""
[sources.example]
url = "http://example.com"
type = "web"
""")
    
    output_dir = tmp_path / ".knowledge"
    session = requests.Session()
    recorder = Betamax(session)
    
    with recorder.use_cassette('example-web'):
        scraper = KnowledgeScraper(str(config_file), str(output_dir), session=session)
        source = scraper.config["example"]
        scraper.fetch_web(source)
        
    # Verify file was created
    expected_file = output_dir / "example" / "example.com.md"
    assert expected_file.exists()
    content = expected_file.read_text()
    assert "Example Domain" in content
