import os

from knowledge_scraper import DocProcessor, KnowledgeScraper

# Create a mock sources.toml
with open("sources.toml", "w") as f:
    f.write("""
[sources.mock_lib]
url = "http://example.com"
type = "web"
""")

# Large mock HTML content
large_html = (
    "<html><main><h1>Start</h1>"
    + ("<p>Word </p>" * 1000)
    + "<h1>End</h1></main></html>"
)

scraper = KnowledgeScraper("sources.toml", ".knowledge")
scraper.process_and_save(
    "mock_lib", "test.html", DocProcessor.html_to_markdown(large_html)
)

# Verify output
mock_dir = ".knowledge/mock_lib"
if os.path.exists(mock_dir):
    files = os.listdir(mock_dir)
    print(f"Files created in {mock_dir}: {files}")
    for f in files:
        path = os.path.join(mock_dir, f)
        size = os.path.getsize(path)
        print(f"  {f}: {size} bytes")
else:
    print(f"Error: {mock_dir} not created")
