import re
from pathlib import Path

import pytest

import svgkit

ASSETS = sorted((Path(__file__).resolve().parents[1] / "assets").glob("*.svg"))


def test_text_width_monotonic():
    a = svgkit.text_width("DATA", "display", 100)
    b = svgkit.text_width("DATA SCIENTIST", "display", 100)
    assert 0 < a < b
    assert svgkit.text_width("DATA", "display", 200) == pytest.approx(2 * a)
    assert svgkit.text_width("AB", "mono", 10, tracking_em=0.1) == pytest.approx(
        svgkit.text_width("AB", "mono", 10) + 2 * 0.1 * 10)


def test_assert_fits():
    svgkit.assert_fits("HI", "display", 10, 1000)
    with pytest.raises(AssertionError):
        svgkit.assert_fits("VAHIDIMOWLAVI", "display", 200, 300)


def test_panel_has_notch():
    p = svgkit.panel(10, 20, 100, 50, notch=8)
    assert "M10,20 H102 L110,28 V70 H10 Z" in p


def test_font_css_embeds_woff2():
    css = svgkit.font_css({"display": "AB", "mono": "1", "serif": "x"})
    assert css.count("@font-face") == 3
    assert "data:font/woff2;base64," in css


def test_esc():
    assert svgkit.esc("S&P <x>") == "S&amp;P &lt;x&gt;"


def test_svg_doc_has_bg():
    d = svgkit.svg_doc(100, 50, "<g/>", "")
    assert '<rect width="100" height="50" fill="#000"' in d
    assert d.startswith("<svg")


@pytest.mark.parametrize("path", ASSETS, ids=lambda p: p.name)
def test_svg_safe(path):
    s = path.read_text()
    for bad in ["<script", "<foreignObject", 'href="http', "url(http", "onload", "onclick"]:
        assert bad not in s, bad


@pytest.mark.parametrize("path", ASSETS, ids=lambda p: p.name)
def test_svg_has_bg(path):
    assert re.search(r'<rect width="\d+" height="\d+" fill="#000"', path.read_text())


@pytest.mark.parametrize("path", ASSETS, ids=lambda p: p.name)
def test_svg_size(path):
    assert path.stat().st_size < 250_000
