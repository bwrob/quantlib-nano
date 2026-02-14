import pytest
import os
import toml
from typing import List, Dict

# Implementation will go here, but for now we write the test
# We'll need a mock toml for testing

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

class ScraperSource:
    def __init__(self, name: str, url: str, type: str):
        self.name = name
        self.url = url
        self.type = type

class ScraperConfig:
    @staticmethod
    def from_toml(file_path: str) -> Dict[str, ScraperSource]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Config file not found: {file_path}")
        
        with open(file_path, "r") as f:
            data = toml.load(f)
            
        sources = {}
        for name, info in data.get("sources", {}).items():
            sources[name] = ScraperSource(name, info["url"], info["type"])
        return sources

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
