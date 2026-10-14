"""Fail the Pages build on broken local links, missing assets or stale domain references."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1] / "docs"


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
        self.h1_count = 0

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if "id" in attributes:
            assert attributes["id"] not in self.ids, f"Duplicate ID: {attributes['id']}"
            self.ids.add(attributes["id"])
        if tag == "h1":
            self.h1_count += 1
        for key in ("href", "src"):
            if attributes.get(key):
                self.links.append(attributes[key])


page = Page()
page.feed((ROOT / "index.html").read_text())
assert page.h1_count == 1, f"Expected one h1, found {page.h1_count}"

checked = 0
for raw in page.links:
    url = urlsplit(raw)
    if url.scheme or url.netloc:
        continue
    if not url.path:
        assert url.fragment in page.ids, f"Missing anchor: {raw}"
    else:
        path = unquote(url.path).removeprefix("/eswar-test-repository/")
        assert (ROOT / path).is_file(), f"Missing local file: {raw}"
    checked += 1

for path in ROOT.rglob("*"):
    if path.is_file() and path.suffix in {".html", ".css", ".js", ".xml", ".txt", ".md", ".webmanifest"}:
        assert "eswar-singamsetty-qa-portfolio.com" not in path.read_text(), f"Stale domain: {path}"

assert not (ROOT / "CNAME").exists(), "Unexpected custom-domain configuration"
resume_files = {
    "pdf": ROOT / "assets" / "Eswar_Sai_Kiran_Singamsetty_ATS_Resume_Updated.pdf",
    "docx": ROOT / "assets" / "Eswar_Sai_Kiran_Singamsetty_ATS_Resume.docx",
}
for suffix, path in resume_files.items():
    assert path.is_file() and path.stat().st_size > 10_000, f"Missing or empty {suffix.upper()} resume: {path.name}"
    if suffix == "pdf":
        assert path.read_bytes().startswith(b"%PDF-"), "Resume PDF signature is invalid"
    else:
        with zipfile.ZipFile(path) as archive:
            assert archive.testzip() is None, "Resume DOCX archive is corrupt"
            assert b"eswar-singamsetty-qa-portfolio.com" not in archive.read("word/_rels/document.xml.rels")

json.loads((ROOT / "manifest.webmanifest").read_text())
print(f"PASS: {checked} internal links/assets, {len(page.ids)} unique IDs, valid resume files, no custom domain")
