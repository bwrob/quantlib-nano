import os
import requests
import toml
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from typing import Dict, List, Optional
import subprocess

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

class DocProcessor:
    @staticmethod
    def html_to_markdown(html_content: str, base_url: Optional[str] = None) -> str:
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Remove noisy elements
        for element in soup(["nav", "footer", "header", "script", "style", "aside"]):
            element.decompose()
            
        # Extract main content if possible (heuristic)
        content = soup.find("main") or soup.find("article") or soup.find("div", class_="content") or soup
        
        # Convert to markdown
        markdown = md(str(content), heading_style="ATX", base_url=base_url)
        return markdown.strip()

    @staticmethod
    def process_file(file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        if file_path.endswith(".html"):
            return DocProcessor.html_to_markdown(content)
        return content # Assume it's already markdown or text

class KnowledgeScraper:
    def __init__(self, config_path: str, output_dir: str):
        self.config = ScraperConfig.from_toml(config_path)
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def fetch_git(self, source: ScraperSource):
        repo_dir = os.path.join("/tmp", source.name)
        if os.path.exists(repo_dir):
            subprocess.run(["git", "-C", repo_dir, "pull"], check=True)
        else:
            subprocess.run(["git", "clone", "--depth", "1", source.url, repo_dir], check=True)
        return repo_dir

    def fetch_web(self, source: ScraperSource):
        # Implementation for simple web fetching (one page or simple crawl)
        # For now, just a placeholder for the logic
        pass

if __name__ == "__main__":
    # Example usage placeholder
    pass
