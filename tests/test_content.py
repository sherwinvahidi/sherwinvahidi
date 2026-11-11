import re
from pathlib import Path

import content

FORBIDDEN = [r"react", r"javascript", r"\(?\b\d{3}\)?[\s.-]?\d{3}-\d{4}\b", r"gmail", r"@\w+\.\w+"]


def test_log_now_is_ms():
    now = [row for row in content.LOG if row[2] == "NOW"]
    assert len(now) == 1
    assert "MS Data Science" in now[0][1]


def test_gsk_not_now():
    gsk = [row for row in content.LOG if "GSK" in row[1]]
    assert gsk and all(r[2] != "NOW" for r in gsk)


def test_metrics_verbatim():
    p = {x["n"]: x for x in content.PROJECTS}
    assert [b[1] for b in p["01"]["bars"]] == [0.737, 0.829]
    assert p["02"]["gauge"] == 0.72
    assert "2.3M" in p["02"]["caption_l"] and "F1 .85" in p["02"]["caption_r"]
    assert [b[1] for b in p["03"]["bars"]] == [0.857, 0.955, 0.964]
    log = " ".join(r[1] for r in content.LOG)
    for s in ["32 PRs", "40+ students", "~15% repeat-donation lift"]:
        assert s in log


def test_best_flags():
    for proj in content.PROJECTS:
        if proj["bars"]:
            best = [b for b in proj["bars"] if b[2]]
            assert len(best) == 1
            assert best[0][1] == max(b[1] for b in proj["bars"])


def test_availability_date():
    assert "DEC 2026" in content.TICKER
    assert ("Available", "DEC 2026") in content.STATUS


def test_no_forbidden_terms():
    text = Path(content.__file__).read_text().lower()
    for pat in FORBIDDEN:
        assert not re.search(pat, text), pat


def test_docsumxai_unlinked():
    d = [p for p in content.PROJECTS if p["title"] == "DocSumXAI"][0]
    assert d["url"] is None
    assert "team capstone" in d["caption_l"].lower()


def test_contact_is_linkedin_only():
    assert content.LINKEDIN == "https://www.linkedin.com/in/sherwinvahidi"
    assert content.RESUME_PATH == "resume/Sherwin_Vahidimowlavi_Resume.pdf"
