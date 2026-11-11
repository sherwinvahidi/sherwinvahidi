"""Render every profile section to assets/. Usage: python build/build.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import content  # noqa: E402
from sections import cards, contact, hero, log  # noqa: E402
import readme  # noqa: E402

ASSETS = Path(__file__).resolve().parents[1] / "assets"


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    out = {
        "00-hero.svg": hero.render(),
        "01-log.svg": log.render(),
        "03-contact.svg": contact.render_band(),
        "btn-resume.svg": contact.render_button("resume"),
        "btn-linkedin.svg": contact.render_button("linkedin"),
    }
    for i, p in enumerate(content.PROJECTS, 1):
        out[f"02-card-{i}.svg"] = cards.render(p)
    for name, svg in out.items():
        (ASSETS / name).write_text(svg)
        print(f"{name:20s} {len(svg) / 1024:6.1f} KB")
    readme.main()
    print("README.md")


if __name__ == "__main__":
    main()
