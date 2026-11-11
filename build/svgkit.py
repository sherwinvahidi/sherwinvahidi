"""Small helpers for building self-contained SVG sections.

Fonts are instanced from the variable TTFs and every letter is drawn as a vector
outline, so the SVGs need no fonts and render identically in every browser.
"""
from functools import lru_cache
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.ttLib.removeOverlaps import removeOverlaps

FONT_DIR = Path(__file__).resolve().parent / "fonts"

# key -> (file, variable-axis location, CSS family name)
FONTS = {
    "display": ("InterTight.ttf", {"wght": 800}, "SVDisplay"),
    "mono": ("JetBrainsMono.ttf", {"wght": 500}, "SVMono"),
    "serif": ("InstrumentSerif-Italic.ttf", None, "SVSerif"),
}

FG = "#f2f2f2"
MUTED = "#8a8f98"
LINE = "rgba(255,255,255,.16)"
ACCENT = "#5ab4ff"
BAR_OFF = "#3a3d42"


@lru_cache(maxsize=None)
def _font(key: str) -> TTFont:
    file, loc, _ = FONTS[key]
    f = TTFont(FONT_DIR / file)
    if loc:
        f = instancer.instantiateVariableFont(f, loc)
        removeOverlaps(f)  # outlined glyphs must not show internal contour seams
    return f


@lru_cache(maxsize=None)
def _metrics(key: str):
    f = _font(key)
    return f.getBestCmap(), f["hmtx"].metrics, f["head"].unitsPerEm


FALLBACK = "display"


def _glyph(font: str, ch: str):
    """(font actually used, glyph name, advance in px-per-size-1). Falls back to the
    display face for symbols the font lacks; raises KeyError if no font has it."""
    for f in (font, FALLBACK):
        cmap, hmtx, upem = _metrics(f)
        name = cmap.get(ord(ch))
        if name:
            return f, name, hmtx[name][0] / upem
    raise KeyError(f"no font has {ch!r} (U+{ord(ch):04X})")


def text_width(s: str, font: str, size: float, tracking_em: float = 0) -> float:
    """Advance width of `s` in px (no kerning), plus letter-spacing after every glyph."""
    return sum(_glyph(font, c)[2] for c in s) * size + tracking_em * size * len(s)


def assert_fits(s: str, font: str, size: float, max_w: float, tracking_em: float = 0) -> None:
    w = text_width(s, font, size, tracking_em)
    assert w <= max_w, f"{s!r} is {w:.0f}px wide, limit {max_w:.0f}px"


def base_css() -> str:
    return (
        f".d{{fill:{FG}}}.m{{fill:{MUTED}}}.s{{fill:{FG}}}"
        f".fg{{fill:{FG}}}.ac{{fill:{ACCENT}}}"
        "@keyframes pulse{50%{opacity:.3}}"
        ".pulse{animation:pulse 2s ease-in-out infinite}"
        "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
    )


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def panel(x: float, y: float, w: float, h: float, notch: float = 18) -> str:
    """Hairline frame with the top-right corner clipped."""
    d = f"M{x:g},{y:g} H{x + w - notch:g} L{x + w:g},{y + notch:g} V{y + h:g} H{x:g} Z"
    return f'<path d="{d}" fill="none" stroke="{LINE}" stroke-width="1.5"/>'


def svg_doc(w: int, h: int, body: str, css: str, title: str = "") -> str:
    t = f"<title>{esc(title)}</title>" if title else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img">{t}<style>{css}</style>'
            f'<rect width="{w}" height="{h}" fill="#000"/>{body}</svg>')


CLASS = {"display": "d", "mono": "m", "serif": "s"}


@lru_cache(maxsize=None)
def _outline(font: str, glyph: str) -> str:
    f = _font(font)
    pen = SVGPathPen(f.getGlyphSet())
    f.getGlyphSet()[glyph].draw(pen)
    return pen.getCommands()


class Canvas:
    """Collects SVG parts. Lettering is drawn as shared glyph outlines (<use>),
    so the SVG needs no fonts: GitHub's CSP blocks embedded fonts in Safari."""

    def __init__(self):
        self.parts = []
        self.glyphs = {}  # (font, glyph name) -> element id

    def raw(self, s: str) -> None:
        self.parts.append(s)

    def run(self, x, y, s, font, size, tracking=0, anchor="start", cls="", attrs="") -> str:
        """A <g> drawing `s` with its baseline at y. Returns the markup (not appended)."""
        w = text_width(s, font, size, tracking) - tracking * size
        x0 = {"start": x, "middle": x - w / 2, "end": x - w}[anchor]
        uses, cx = [], x0
        for ch in s:
            f, name, adv = _glyph(font, ch)
            if _outline(f, name):
                scale = size / _metrics(f)[2]
                gid = self.glyphs.setdefault((f, name), f"{CLASS[f]}{len(self.glyphs)}")
                uses.append(f'<use href="#{gid}" transform="matrix({scale:.5f} 0 0 {-scale:.5f} {cx:.2f} {y:.2f})"/>')
            cx += adv * size + tracking * size
        c = (CLASS[font] + " " + cls).strip()
        return f'<g class="{c}" data-text="{esc(s)}"{attrs}>{"".join(uses)}</g>'

    def t(self, x, y, s, font, size, tracking=0, anchor="start", cls="", extra="", max_w=None):
        if max_w is not None:
            assert_fits(s, font, size, max_w, tracking)
        self.raw(self.run(x, y, s, font, size, tracking, anchor, cls, extra))

    def doc(self, w: int, h: int, css: str = "", title: str = "") -> str:
        defs = "".join(f'<path id="{gid}" d="{_outline(f, g)}"/>' for (f, g), gid in self.glyphs.items())
        body = (f"<defs>{defs}</defs>" if defs else "") + "".join(self.parts)
        return svg_doc(w, h, body, base_css() + css, title)
