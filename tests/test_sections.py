import re

import content
from sections import cards, contact, hero, log

ACCENT = "#5ab4ff"


def accent_uses(svg):
    return svg.count(ACCENT) + svg.count('class="ac')


def test_hero():
    s = hero.render()
    assert "AVAILABLE FOR FULL-TIME" in s and "DEC 2026" in s
    assert "@keyframes ticker" in s
    assert "VAHIDI" in s and "MOWLAVI" in s and "DATA SCIENTIST" in s
    assert content.TAGLINE in s


def test_log():
    s = log.render()
    for label, value in content.STATUS:
        assert label.upper() in s and value in s
    for year, text, mark in content.LOG:
        assert year in s
    assert "pulse" in s
    # NOW is the only accented log mark
    assert re.search(r'class="[^"]*\bac\b[^"]*"[^>]*>NOW<', s)


def test_cards_bars_proportional():
    for proj in content.PROJECTS:
        s = cards.render(proj)
        for label, value, best in proj["bars"] or []:
            m = re.search(rf'<rect data-bar="{label}" x="[\d.]+" y="[\d.]+" width="([\d.]+)"', s)
            assert m, label
            assert abs(float(m.group(1)) - value * cards.BAR_SCALE) < 0.5
        if proj["gauge"] is not None:
            assert f'stroke-dasharray="{proj["gauge"] * 100:g} 100"' in s


def test_cards_accent_only_on_best():
    for proj in content.PROJECTS:
        s = cards.render(proj)
        for label, value, best in proj["bars"] or []:
            tag = re.search(rf'<rect data-bar="{label}"[^>]*>', s).group(0)
            assert (ACCENT in tag) == best, label


def test_cards_title_wraps_max_three_lines():
    for proj in content.PROJECTS:
        assert 1 <= len(cards.wrap_title(proj["title"])) <= 3


def test_contact():
    band = contact.render_band()
    assert "LET&apos;S TALK" in band or "LET'S TALK" in band
    assert "mail" not in band.lower()
    assert "RESUME" in contact.render_button("resume")
    assert "LINKEDIN" in contact.render_button("linkedin")
