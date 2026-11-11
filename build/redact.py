"""Make the public resume: remove phone + email, keep the layout.

Usage: python build/redact.py [source.pdf]
"""
import re
import sys
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / "Downloads/Sherwin_Vahidimowlavi_Resume.pdf"
OUT = ROOT / "resume/Sherwin_Vahidimowlavi_Resume.pdf"
FONT = Path(__file__).resolve().parent / "fonts/Carlito-Regular.ttf"

LINE2 = "San Jose, CA"
LINKS = [("linkedin.com/in/sherwinvahidi", "https://www.linkedin.com/in/sherwinvahidi"),
         ("github.com/sherwinvahidi", "https://github.com/sherwinvahidi")]
SEP = " • "
PHONE = re.compile(r"\(?\b\d{3}\)?[\s.-]?\d{3}-\d{4}\b")


def contact_spans(page):
    spans = [s for b in page.get_text("dict")["blocks"] for l in b.get("lines", []) for s in l["spans"]]
    phone = next(s for s in spans if PHONE.search(s["text"]))
    email = next(s for s in spans if "@" in s["text"])
    return phone, email


def main():
    doc = pymupdf.open(SRC)
    page = doc[0]
    phone, email = contact_spans(page)
    size = phone["size"]
    W = page.rect.width
    for s in (phone, email):
        r = pymupdf.Rect(s["bbox"])
        page.add_redact_annot(pymupdf.Rect(30, r.y0 - 0.5, W - 30, r.y1 + 1.5))
    for l in page.get_links():
        if l.get("uri", "").startswith("mailto"):
            page.delete_link(l)
    page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,
                          graphics=pymupdf.PDF_REDACT_LINE_ART_REMOVE_IF_TOUCHED)

    font = pymupdf.Font(fontfile=str(FONT))
    page.insert_font(fontname="carlito", fontfile=str(FONT))

    def centered(text, baseline):
        x = (W - font.text_length(text, fontsize=size)) / 2
        page.insert_text((x, baseline), text, fontname="carlito", fontsize=size)
        return x

    centered(LINE2, phone["origin"][1])
    line3 = SEP.join(t for t, _ in LINKS)
    x = centered(line3, email["origin"][1])
    y = email["origin"][1]
    for t, uri in LINKS:
        w = font.text_length(t, fontsize=size)
        page.draw_line((x, y + 1.2), (x + w, y + 1.2), color=(0, 0, 0), width=0.5)
        page.insert_link({"kind": pymupdf.LINK_URI, "from": pymupdf.Rect(x, y - size * 0.8, x + w, y + 2), "uri": uri})
        x += w + font.text_length(SEP, fontsize=size)

    doc.set_metadata({k: "" for k in doc.metadata if k not in ("format", "encryption")} | {"title": "Sherwin Vahidimowlavi Resume", "author": "Sherwin Vahidimowlavi"})
    OUT.parent.mkdir(exist_ok=True)
    doc.save(OUT, garbage=4, deflate=True, clean=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
