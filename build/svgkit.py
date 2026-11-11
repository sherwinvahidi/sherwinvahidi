"""Small helpers for building self-contained SVG sections.

Fonts are instanced from the variable TTFs, subset to the glyphs a section uses,
and embedded as base64 WOFF2, so every viewer sees the same typography.
"""
import base64
import io
from functools import lru_cache
from pathlib import Path

from fontTools import subset
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


def text_width(s: str, font: str, size: float, tracking_em: float = 0) -> float:
    """Advance width of `s` in px (no kerning), plus letter-spacing after every glyph."""
    cmap, hmtx, upem = _metrics(font)
    units = sum(hmtx[cmap.get(ord(c), ".notdef")][0] for c in s)
    return units / upem * size + tracking_em * size * len(s)


def assert_fits(s: str, font: str, size: float, max_w: float, tracking_em: float = 0) -> None:
    w = text_width(s, font, size, tracking_em)
    assert w <= max_w, f"{s!r} is {w:.0f}px wide, limit {max_w:.0f}px"


def font_css(used: dict) -> str:
    """@font-face rules embedding each font subset to the characters in `used[key]`."""
    rules = []
    for key, chars in used.items():
        if not chars:
            continue
        f = TTFont(io.BytesIO(_font_bytes(key)))
        opts = subset.Options()
        opts.flavor = "woff2"
        opts.layout_features = ["kern", "liga"]
        opts.name_IDs = [0, 1, 2, 13, 14]  # keep copyright + OFL license records
        opts.notdef_outline = True
        sub = subset.Subsetter(opts)
        sub.populate(text="".join(sorted(set(chars))) + " ")
        sub.subset(f)
        buf = io.BytesIO()
        f.flavor = "woff2"
        f.save(buf)
        b64 = base64.b64encode(buf.getvalue()).decode()
        rules.append(f"@font-face{{font-family:{FONTS[key][2]};src:url(data:font/woff2;base64,{b64}) format('woff2')}}")
    return "".join(rules)


@lru_cache(maxsize=None)
def _font_bytes(key: str) -> bytes:
    buf = io.BytesIO()
    _font(key).save(buf)
    return buf.getvalue()


def base_css() -> str:
    d, m, s = (FONTS[k][2] for k in ("display", "mono", "serif"))
    return (
        f".d{{font-family:{d};font-weight:800;fill:{FG}}}"
        f".m{{font-family:{m};font-weight:500;fill:{MUTED}}}"
        f".s{{font-family:{s};font-style:italic;fill:{FG}}}"
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


def text(x, y, s, cls, size, tracking_em=0, anchor="start", extra="") -> str:
    ls = f' letter-spacing="{tracking_em * size:.2f}"' if tracking_em else ""
    return (f'<text x="{x:g}" y="{y:g}" class="{cls}" font-size="{size:g}"{ls} '
            f'text-anchor="{anchor}"{extra}>{esc(s)}</text>')


def svg_doc(w: int, h: int, body: str, css: str, title: str = "") -> str:
    t = f"<title>{esc(title)}</title>" if title else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img">{t}<style>{css}</style>'
            f'<rect width="{w}" height="{h}" fill="#000"/>{body}</svg>')


CLASS = {"display": "d", "mono": "m", "serif": "s"}


class Canvas:
    """Collects SVG parts and the characters each font must embed."""

    def __init__(self):
        self.parts = []
        self.used = {k: "" for k in FONTS}

    def use(self, font: str, s: str) -> None:
        self.used[font] += s

    def raw(self, s: str) -> None:
        self.parts.append(s)

    def t(self, x, y, s, font, size, tracking=0, anchor="start", cls="", extra="", max_w=None):
        if max_w is not None:
            assert_fits(s, font, size, max_w, tracking)
        self.use(font, s)
        c = (CLASS[font] + " " + cls).strip()
        self.raw(text(x, y, s, c, size, tracking, anchor, extra))

    def doc(self, w: int, h: int, css: str = "", title: str = "") -> str:
        return svg_doc(w, h, "".join(self.parts), font_css(self.used) + base_css() + css, title)
