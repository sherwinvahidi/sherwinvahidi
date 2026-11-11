"""Generate README.md from content.py."""
import hashlib
import re
from pathlib import Path

import content as C

ROOT = Path(__file__).resolve().parents[1]
RAW = "https://github.com/sherwinvahidi/sherwinvahidi/raw/main/"


def render() -> str:
    cards = []
    for i, p in enumerate(C.PROJECTS, 1):
        img = f'<img src="assets/02-card-{i}.svg" width="49%" alt="{p["alt"]}">'
        cards.append(f'<a href="{p["url"]}">{img}</a>' if p["url"] else img)
    log_alt = ("Status: open to full-time work, available Dec 2026, targeting DS and ML roles in the Bay Area. Career log: "
               + "; ".join(f"{y} {t.replace(' · ', ', ')}" + (" (now)" if m == "NOW" else "") for y, t, m in C.LOG) + ".")
    return f'''<a href="{C.LINKEDIN}"><img src="assets/00-hero.svg" width="100%" alt="Sherwin Vahidimowlavi, Data Scientist. MS Data Science, Northeastern University. Available for full-time roles, Dec 2026."></a>

<img src="assets/01-log.svg" width="100%" alt="{log_alt}">

<p>
{cards[0]}
{cards[1]}
</p>
<p>
{cards[2]}
{cards[3]}
</p>

<img src="assets/03-contact.svg" width="100%" alt="Let's talk. I'm graduating in December.">

<p>
<a href="{RAW}{C.RESUME_PATH}"><img src="assets/btn-resume.svg" width="260" alt="Download resume (PDF)"></a>
<a href="{C.LINKEDIN}"><img src="assets/btn-linkedin.svg" width="260" alt="LinkedIn profile"></a>
</p>

## About

I'm a **Data Scientist** finishing an MS in Data Science at Northeastern University (Khoury College), graduating **Dec 2026**, and open to full-time data science and ML roles in the Bay Area.

Before grad school I spent four and a half years at Stanford Health Care's Blood Center, where I ran a self-initiated donor-retention project that lifted the repeat-donation rate by about 15%. Before that, I analyzed app engagement with SQL and Tableau at Foursquare. In 2026 I interned on GSK's Omics Workbench (via Atrium), building pipeline automation for Nextflow workflows on Google Cloud Batch.

**Selected projects**
- [Few-shot brain tumor segmentation]({C.PROJECTS[0]["url"]}) (team project): prototypical network reaches 0.829 Dice at k=20, above the 0.737 fully supervised baseline
- [Decoding healthcare costs]({C.PROJECTS[1]["url"]}): 2.3M NYC hospital records; length-of-stay R² 0.72, mortality F1 0.85
- [Seoul bike demand]({C.PROJECTS[2]["url"]}) (team project): XGBoost F1 0.964 with temporal cross-validation
- DocSumXAI (team capstone, in progress): explainable long-document summarization

**Skills:** {C.SKILLS}

**Resume:** [PDF]({RAW}{C.RESUME_PATH}) &nbsp;·&nbsp; **LinkedIn:** [linkedin.com/in/sherwinvahidi]({C.LINKEDIN})
'''


def _versioned(md: str) -> str:
    """Append ?v=<content hash> to every asset URL so GitHub's image cache
    (raw.githubusercontent.com, max-age 300 but often longer) can't serve stale art."""
    def add(m):
        path = m.group(1)
        h = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()[:10]
        return f'src="{path}?v={h}"'
    return re.sub(r'src="(assets/[^"?]+)"', add, md)


def main() -> None:
    (ROOT / "README.md").write_text(_versioned(render()))
