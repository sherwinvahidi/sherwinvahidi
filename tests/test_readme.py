import hashlib
import re
from pathlib import Path

import content

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
PDF = ROOT / content.RESUME_PATH


def test_resume_redacted():
    import pymupdf
    doc = pymupdf.open(PDF)
    text = "".join(p.get_text() for p in doc)
    links = [l.get("uri", "") for p in doc for l in p.get_links()]
    assert not re.search(r"\(?\b\d{3}\)?[\s.-]?\d{3}-\d{4}\b", text)
    assert "gmail" not in text and not re.search(r"[\w.]+@[\w-]+\.com", text)
    assert not any("mailto" in u for u in links)
    assert "Sherwin Vahidimowlavi" in text
    assert "linkedin.com/in/sherwinvahidi" in text
    assert len(doc) == len(pymupdf.open(Path.home() / "Downloads/Sherwin_Vahidimowlavi_Resume.pdf"))


def test_readme_text_essentials():
    s = README.read_text()
    about = s.split("## About", 1)[1]
    for need in ["Data Scientist", "Dec 2026", content.SKILLS, content.LINKEDIN, content.RESUME_PATH]:
        assert need in about, need


def test_readme_assets_exist_and_have_alt():
    s = README.read_text()
    imgs = re.findall(r"<img [^>]*>", s)
    assert len(imgs) == 9
    for tag in imgs:
        src = re.search(r'src="([^"]+)"', tag).group(1)
        path, _, ver = src.partition("?v=")
        assert (ROOT / path).exists(), src
        # a content hash in the URL makes GitHub's image cache fetch new versions
        assert ver == hashlib.sha256((ROOT / path).read_bytes()).hexdigest()[:10], src
        assert re.search(r'alt="[^"]{8,}"', tag), tag


def test_readme_links():
    s = README.read_text()
    for p in content.PROJECTS:
        if p["url"]:
            assert f'href="{p["url"]}"' in s
    assert "DocSumXAI" not in re.findall(r'href="([^"]+)"', s).__str__()
    assert "mailto" not in s.lower() and "gmail" not in s.lower()
