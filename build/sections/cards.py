from svgkit import ACCENT, BAR_OFF, Canvas, _metrics, panel, text_width

W, H = 600, 800
X0 = 58
INNER = W - 2 * X0
BAR_X = 170
BAR_SCALE = 360  # px for a value of 1.0
TITLE = 54
TITLE_TRK = -0.035


def wrap_title(title: str) -> list:
    words, lines, cur = title.upper().split(), [], ""
    for w in words:
        cand = (cur + " " + w).strip()
        if text_width(cand, "display", TITLE, TITLE_TRK) <= INNER:
            cur = cand
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    assert len(lines) <= 3, lines
    return lines


def render(p: dict) -> str:
    c = Canvas()
    c.raw(panel(30, 30, W - 60, H - 60, notch=26))
    sw = 1.6 * _metrics("display")[2] / 300  # stroke is in glyph units
    c.t(X0 - 10, 300, p["n"], "display", 300, -0.07,
        extra=f' style="fill:none" stroke="rgba(255,255,255,.45)" stroke-width="{sw:.1f}"')
    c.t(W - X0, 92, p["kicker"], "mono", 21, 0.08, anchor="end")

    lines = wrap_title(p["title"])
    y = 420
    for ln in lines:
        c.t(X0, y, ln, "display", TITLE, TITLE_TRK, max_w=INNER)
        y += TITLE * 0.95

    base = 650
    if p["bars"]:
        n = len(p["bars"])
        for i, (label, value, best) in enumerate(p["bars"]):
            yy = base - (n - 1 - i) * 40
            c.t(X0, yy, label.upper(), "mono", 21, 0.06)
            fill = ACCENT if best else BAR_OFF
            glow = ' filter="url(#bg)"' if best else ""
            c.raw(f'<rect data-bar="{label}" x="{BAR_X}" y="{yy - 17}" width="{value * BAR_SCALE:.1f}" height="20" fill="{fill}"{glow}/>')
            if best:
                c.raw(f'<rect x="{BAR_X}" y="{yy - 17}" width="{value * BAR_SCALE:.1f}" height="20" fill="{ACCENT}"/>')
    elif p["gauge"] is not None:
        cx, cy, r = W / 2, base + 4, 96
        arc = f"M{cx - r},{cy} A{r},{r} 0 0 1 {cx + r},{cy}"
        c.raw(f'<path d="{arc}" fill="none" stroke="{BAR_OFF}" stroke-width="12"/>')
        c.raw(f'<path d="{arc}" fill="none" stroke="{ACCENT}" stroke-width="12" pathLength="100" '
              f'stroke-dasharray="{p["gauge"] * 100:g} 100" filter="url(#gg)"/>')
        c.raw(f'<path d="{arc}" fill="none" stroke="{ACCENT}" stroke-width="12" pathLength="100" '
              f'stroke-dasharray="{p["gauge"] * 100:g} 100"/>')
        c.t(cx, cy - 8, f'{p["gauge"]:.2f}', "display", 52, -0.03, anchor="middle")
    elif p.get("status"):
        c.t(X0, base, "STATUS", "mono", 21, 0.06)
        c.raw(f'<rect x="{BAR_X}" y="{base - 17}" width="44" height="20" fill="{ACCENT}" class="pulse"/>')

    c.t(X0, 726, p["caption_l"].upper(), "mono", 19, 0.04, max_w=INNER - 100)
    c.t(W - X0, 726, p["caption_r"], "mono", 21, 0.04, anchor="end", cls="fg")
    defs = ('<defs><filter id="bg" x="-20%" y="-200%" width="140%" height="500%"><feGaussianBlur stdDeviation="7"/></filter>'
            '<filter id="gg" x="-30%" y="-60%" width="160%" height="220%"><feGaussianBlur stdDeviation="6"/></filter></defs>')
    c.parts.insert(0, defs)
    return c.doc(W, H, title=p["alt"])
