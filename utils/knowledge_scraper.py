"""Knowledge scraper utility for fetching and processing documentation."""

import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Final

import requests
import toml
from bs4 import BeautifulSoup
from markdownify import markdownify as md


class ScraperSource:
    """Represents a documentation source to be scraped."""

    name: Final[str]
    url: Final[str]
    source_type: Final[str]

    def __init__(self, name: str, url: str, source_type: str) -> None:
        """Initialize a ScraperSource."""
        self.name = name
        self.url = url
        self.source_type = source_type


class ScraperConfig:
    """Configuration loader for the scraper."""

    @staticmethod
    def from_toml(file_path: str) -> dict[str, ScraperSource]:
        """Load scraper sources from a TOML file."""
        path = Path(file_path)
        if not path.exists():
            msg = f"Config file not found: {file_path}"
            raise FileNotFoundError(msg)

        with path.open("r", encoding="utf-8") as f:
            data = toml.load(f)

        sources: dict[str, ScraperSource] = {}
        # type ignore for Any from toml.load
        sources_data = data.get("sources", {})  # pyright: ignore[reportAny]
        for name, info in sources_data.items():  # pyright: ignore[reportAny]
            sources[name] = ScraperSource(name, info["url"], info["type"])  # pyright: ignore[reportAny]
        return sources


class DocProcessor:
    """Processor for converting and chunking documentation."""

    @staticmethod
    def html_to_markdown(html_content: str) -> str:
        """Convert HTML content to clean Markdown."""
        soup = BeautifulSoup(html_content, "html.parser")

        # Remove noisy elements
        for element in soup(["nav", "footer", "header", "script", "style", "aside"]):
            element.decompose()

        # Extract main content if possible (heuristic)
        content = (
            soup.find("main")
            or soup.find("article")
            or soup.find("div", class_="content")
            or soup
        )

        # Convert to markdown
        markdown = md(str(content), heading_style="ATX")
        return str(markdown).strip()

    @staticmethod
    def chunk_markdown(content: str, max_chars: int = 4000) -> list[str]:
        """Split Markdown content into smaller chunks based on headers and length."""
        if len(content) <= max_chars:
            return [content]

        # Split by headers (ATX style: #, ##, etc.)
        sections = re.split(r"(?=\n#+ )", "\n" + content)
        sections = [s.strip() for s in sections if s.strip()]

        chunks: list[str] = []
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
                    chunks.extend(
                        [
                            section[i : i + max_chars]
                            for i in range(0, len(section), max_chars)
                        ]
                    )
                    current_chunk = ""
                else:
                    current_chunk = section

        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    @staticmethod
    def process_file(file_path: str) -> str:
        """Read and process a file (HTML to MD if needed)."""
        path = Path(file_path)
        with path.open("r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        if path.suffix == ".html":
            return DocProcessor.html_to_markdown(content)
        return content


class KnowledgeScraper:
    """Orchestrator for fetching and processing documentation sources."""

    config: Final[dict[str, ScraperSource]]
    output_dir: Final[Path]
    session: Final[requests.Session]

    def __init__(
        self,
        config_path: str,
        output_dir: str,
        session: requests.Session | None = None,
    ) -> None:
        """Initialize the KnowledgeScraper."""
        self.config = ScraperConfig.from_toml(config_path)
        self.output_dir = Path(output_dir)
        self.session = session or requests.Session()
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def fetch_git(self, source: ScraperSource) -> Path:
        """Clone or pull a git repository."""
        git_executable = shutil.which("git")
        if not git_executable:
            msg = "git executable not found in PATH"
            raise RuntimeError(msg)

        # Revision: use project local .tmp for repos
        project_tmp = Path(__file__).parent.parent / ".tmp" / "repos"
        repo_dir = project_tmp / source.name
        repo_dir.parent.mkdir(parents=True, exist_ok=True)

        if repo_dir.exists():
            print(f"Updating {source.name}...")
            _ = subprocess.run(
                [git_executable, "-C", str(repo_dir), "pull"],
                check=True,
                capture_output=True,
            )
        else:
            print(f"Cloning {source.name}...")
            _ = subprocess.run(
                [git_executable, "clone", "--depth", "1", source.url, str(repo_dir)],
                check=True,
                capture_output=True,
            )
        return repo_dir

    def fetch_web(self, source: ScraperSource) -> None:
        """Fetch a single web page and save as Markdown."""
        print(f"Fetching {source.url}...")
        response = self.session.get(source.url)
        response.raise_for_status()
        markdown = DocProcessor.html_to_markdown(response.text)
        self.process_and_save(source.name, source.url + ".html", markdown)

    def run(self) -> None:
        """Execute the scraping for all configured sources."""
        for name, source in self.config.items():
            if source.source_type == "git":
                repo_dir = self.fetch_git(source)
                self.crawl_git(name, repo_dir)
            elif source.source_type == "web":
                self.fetch_web(source)

    def crawl_git(self, source_name: str, repo_dir: Path) -> None:
        """Walk a git repository and process relevant documentation files."""
        for root, _dirs, files in os.walk(repo_dir):
            for file in files:
                if file.endswith((".md", ".hpp", ".h")):
                    file_path = Path(root) / file
                    if not file_path.exists():
                        continue
                    with file_path.open("r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    # Only process files with meaningful content
                    min_content_length = 100
                    if len(content.strip()) > min_content_length:
                        self.process_and_save(source_name, str(file_path), content)

    def process_and_save(self, source_name: str, file_path: str, content: str) -> None:
        """Chunk and save documentation content to the output directory."""
        source_dir = self.output_dir / source_name
        source_dir.mkdir(parents=True, exist_ok=True)

        chunks = DocProcessor.chunk_markdown(content)
        base_name = Path(file_path).stem

        for i, chunk in enumerate(chunks):
            suffix = f"_{i}" if len(chunks) > 1 else ""
            output_file = source_dir / f"{base_name}{suffix}.md"
            with output_file.open("w", encoding="utf-8") as f:
                f.write(chunk)


if __name__ == "__main__":
    # Look for sources.toml in the same directory as the script
    _script_dir = Path(__file__).parent.resolve()
    _config_path = str(_script_dir / "sources.toml")
    _output_dir = ".knowledge"

    _scraper = KnowledgeScraper(_config_path, _output_dir)
    _ = _scraper.run()
