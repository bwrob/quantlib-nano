import os
import requests
import toml
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from typing import Dict, List, Optional
import subprocess
import re

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
    def chunk_markdown(content: str, max_chars: int = 4000) -> List[str]:
        if len(content) <= max_chars:
            return [content]
            
        # Split by headers (ATX style: #, ##, etc.)
        # We use a lookahead to keep the delimiter with the following text
        sections = re.split(r'(?=\n#+ )', "\n" + content)
        sections = [s.strip() for s in sections if s.strip()]
        
        chunks = []
        current_chunk = ""
        
        for section in sections:
            if len(current_chunk) + len(section) + 2 <= max_chars:
                if current_chunk:
                    current_chunk += "\n\n" + section
                else:
                    current_chunk = section
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                
                # If a single section is larger than max_chars, split it by length
                if len(section) > max_chars:
                    for i in range(0, len(section), max_chars):
                        chunks.append(section[i:i+max_chars])
                    current_chunk = ""
                else:
                    current_chunk = section
                    
        if current_chunk:
            chunks.append(current_chunk)
            
        return chunks

    @staticmethod
    def process_file(file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        if file_path.endswith(".html"):
            return DocProcessor.html_to_markdown(content)
        return content

class KnowledgeScraper:
    def __init__(self, config_path: str, output_dir: str):
        self.config = ScraperConfig.from_toml(config_path)
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def fetch_git(self, source: ScraperSource):
        repo_dir = os.path.join("/tmp/knowledge_repos", source.name)
        os.makedirs(os.path.dirname(repo_dir), exist_ok=True)
        if os.path.exists(repo_dir):
            print(f"Updating {source.name}...")
            subprocess.run(["git", "-C", repo_dir, "pull"], check=True)
        else:
            print(f"Cloning {source.name}...")
            subprocess.run(["git", "clone", "--depth", "1", source.url, repo_dir], check=True)
        return repo_dir

    def run(self):
        for name, source in self.config.items():
            if source.type == "git":
                repo_dir = self.fetch_git(source)
                self.crawl_git(name, repo_dir)

    def crawl_git(self, source_name: str, repo_dir: str):
        # We look for .md files and .hpp/.h files (for API context)
        for root, dirs, files in os.walk(repo_dir):
            for file in files:
                if file.endswith(".md") or file.endswith(".hpp") or file.endswith(".h"):
                    file_path = os.path.join(root, file)
                    if not os.path.exists(file_path):
                        continue
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    
                    # Only process files with meaningful content
                    if len(content.strip()) > 100:
                        self.process_and_save(source_name, file_path, content)

    def process_and_save(self, source_name: str, file_path: str, content: str):
        source_dir = os.path.join(self.output_dir, source_name)
        os.makedirs(source_dir, exist_ok=True)
        
        chunks = DocProcessor.chunk_markdown(content)
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        
        for i, chunk in enumerate(chunks):
            suffix = f"_{i}" if len(chunks) > 1 else ""
            output_file = os.path.join(source_dir, f"{base_name}{suffix}.md")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(chunk)

if __name__ == "__main__":
    import sys
    # Look for sources.toml in the same directory as the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "sources.toml")
    output_dir = ".knowledge"
    
    scraper = KnowledgeScraper(config_path, output_dir)
    scraper.run()
