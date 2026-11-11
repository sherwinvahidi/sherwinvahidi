"""Render every profile section to assets/. Usage: python build/build.py"""
import hashlib
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
    # Content hash in the filename: a changed image gets a new URL, so GitHub's
    # image cache (which ignores query strings) can never serve a stale copy.
    files = {}
    for name, svg in out.items():
        h = hashlib.sha256(svg.encode()).hexdigest()[:10]
        files[name] = f"{name[:-4]}.{h}.svg"
        (ASSETS / files[name]).write_text(svg)
        print(f"{files[name]:32s} {len(svg) / 1024:6.1f} KB")
    for old in ASSETS.glob("*.svg"):
        if old.name not in files.values():
            old.unlink()
    readme.main(files)
    print("README.md")


if __name__ == "__main__":
    main()
