"""Single source of truth for every fact shown on the profile.

Every value here must match the resume. Edit this file, then run `python build/build.py`.
"""

NAME_LINES = ("SHERWIN", "VAHIDIMOWLAVI")
OUTLINED_PREFIX = "VAHIDI"  # drawn as an outline at the start of line 2
ROLE = "DATA SCIENTIST"
TAGLINE = "turning messy, real-world data into models people act on."
TICKER = "● AVAILABLE FOR FULL-TIME · DEC 2026"
NAV_LEFT = "SV / 00"
NAV_RIGHT = "PROJECTS   RESUME   CONTACT"
VERT_BIG = "Data Science //"
VERT_SMALL = "MS · NORTHEASTERN · 2026"
HERO_FOOT = (
    "SAN JOSE, CA · 37.33°N 121.89°W",
    "PYTHON · PYTORCH · SCIKIT-LEARN · GCP",
    "SCROLL ↓",
)

STATUS = [
    ("Open to work", "FULL-TIME"),  # first row gets the pulsing dot
    ("Available", "DEC 2026"),
    ("Target", "DS / ML"),
    ("Base", "BAY AREA"),
]

# (year, text, mark); exactly one row is "NOW"
LOG = [
    ("2026", "MS Data Science · Northeastern · capstone", "NOW"),
    ("2026", "Data Platform Eng. Intern · GSK via Atrium · 32 PRs", "✓"),
    ("2026", "TA · Unsupervised ML · 40+ students", "✓"),
    ("2020", "Stanford Health Care · ~15% repeat-donation lift", "✓"),
    ("2015", "Foursquare · SQL & Tableau analytics", "✓"),
]

GH = "https://github.com/sherwinvahidi/"

PROJECTS = [
    {
        "n": "01", "kicker": "DL", "title": "Few-shot tumor segmentation",
        "bars": [("Base", 0.737, False), ("Proto", 0.829, True)], "gauge": None,
        "caption_l": "Dice @k=20", "caption_r": "0.829",
        "url": GH + "UNet-FewShot",
        "alt": "Few-shot brain tumor segmentation (team project): prototypical network reaches 0.829 Dice at k=20 vs a 0.737 fully supervised baseline",
    },
    {
        "n": "02", "kicker": "HEALTH", "title": "Decoding healthcare costs",
        "bars": None, "gauge": 0.72,
        "caption_l": "LOS R² · 2.3M rows", "caption_r": "F1 .85",
        "url": GH + "Decoding-Healthcare-Costs",
        "alt": "Decoding healthcare costs: 2.3M NYC records, length-of-stay R squared 0.72, mortality F1 0.85",
    },
    {
        "n": "03", "kicker": "ML", "title": "Seoul bike demand",
        "bars": [("LR", 0.857, False), ("RF", 0.955, False), ("XGB", 0.964, True)], "gauge": None,
        "caption_l": "Best F1", "caption_r": "0.964",
        "url": GH + "DS-5110-Final-Project-Seoul-Bike-Sharing",
        "alt": "Seoul bike demand (team project): F1 0.857 logistic regression, 0.955 random forest, 0.964 XGBoost",
    },
    {
        "n": "04", "kicker": "NLP", "title": "DocSumXAI",
        "bars": None, "gauge": None, "status": True,
        "caption_l": "Team capstone · summarization", "caption_r": "ACTIVE",
        "url": None,
        "alt": "DocSumXAI: explainable long-document summarization, team capstone in progress",
    },
]

LOG_HEADING = ("STATUS", "& LOG")
LOG_SERIF = "where I've been."
CONTACT_HEADING = "LET'S TALK"
CONTACT_SERIF = "I'm graduating in December."

LINKEDIN = "https://www.linkedin.com/in/sherwinvahidi"
RESUME_PATH = "resume/Sherwin_Vahidimowlavi_Resume.pdf"

SKILLS = "Python · SQL · PyTorch · pandas · NumPy · scikit-learn · GCP (Batch) · Nextflow · Tableau · Jupyter"
