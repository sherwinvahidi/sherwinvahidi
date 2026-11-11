import re
import subprocess
from pathlib import Path

import content
import svgkit
from sections import cards

ROOT = Path(__file__).resolve().parents[1]
PHONE = re.compile(r"\(?\b\d{3}\)?[\s.-]?\d{3}-\d{4}\b")
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.(com|edu|org|net)")


def tracked_text_files():
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout.split()
    return [ROOT / f for f in out if not f.endswith((".pdf", ".ttf"))]


def test_no_phone_or_email_in_tracked_files():
    files = tracked_text_files() + [Path(__file__)]
    assert files
    for f in files:
        s = f.read_text(errors="ignore")
        assert not PHONE.search(s), f
        assert not EMAIL.search(s), f
        for chunk in ("728" + "-2753", "(" + "408)"):
            assert chunk not in s, f


def test_commit_email_is_noreply():
    email = subprocess.run(["git", "config", "user.email"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    assert email.endswith("@users.noreply.github.com"), email
    log = subprocess.run(["git", "log", "--format=%ae %ce"], cwd=ROOT, capture_output=True, text=True).stdout
    assert "gmail" not in log


def test_kicker_clears_numeral():
    for p in content.PROJECTS:
        num_right = cards.X0 - 10 + svgkit.text_width(p["n"], "display", 300, -0.07)
        kick_left = cards.W - cards.X0 - svgkit.text_width(p["kicker"], "mono", 21, 0.08)
        assert kick_left > num_right + 12, p["kicker"]
        assert not p["kicker"].startswith("02 /")


def test_fewshot_marked_team():
    assert "team project" in content.PROJECTS[0]["alt"].lower()


def test_donor_wording():
    log = " ".join(r[1] for r in content.LOG)
    assert "~15% repeat-donation lift" in log
    assert "experiment" not in (ROOT / "README.md").read_text().lower()


def test_font_notice():
    s = (ROOT / "FONTS.md").read_text()
    for name in ["Inter Tight", "JetBrains Mono", "Instrument Serif", "Carlito", "SIL Open Font License"]:
        assert name in s


def test_resume_links_download_raw():
    s = (ROOT / "README.md").read_text()
    raw = "https://github.com/sherwinvahidi/sherwinvahidi/raw/main/" + content.RESUME_PATH
    assert f'href="{raw}"' in s


def test_readme_projects_as_text():
    about = (ROOT / "README.md").read_text().split("## About", 1)[1]
    for need in ["0.829", "0.72", "0.964", "DocSumXAI"]:
        assert need in about, need
