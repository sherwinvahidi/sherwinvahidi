import content
from svgkit import ACCENT, FG, LINE, Canvas, _metrics, assert_fits, text_width

W, H = 1600, 800
PAD = 48
NAME_SIZE = 178
NAME_TRACK = -0.05


def render() -> str:
    c = Canvas()
    # faint grid, faded toward the edges
    c.raw(
        '<defs>'
        '<pattern id="g" width="100" height="100" patternUnits="userSpaceOnUse">'
        f'<path d="M100 0H0V100" fill="none" stroke="{LINE}" stroke-width="1"/></pattern>'
        '<radialGradient id="fade" cx=".6" cy=".45" r=".6"><stop offset="0" stop-color="#fff" stop-opacity=".9"/>'
        '<stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
        '<mask id="gm"><rect width="1600" height="800" fill="url(#fade)"/></mask>'
        f'<linearGradient id="scan" x1="0" x2="1"><stop offset="0" stop-color="{ACCENT}" stop-opacity="0"/>'
        f'<stop offset=".3" stop-color="{ACCENT}"/><stop offset=".55" stop-color="#fff"/>'
        f'<stop offset=".75" stop-color="{ACCENT}"/><stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/></linearGradient>'
        '<filter id="glow" x="-5%" y="-2000%" width="110%" height="4000%"><feGaussianBlur stdDeviation="6"/></filter>'
        '<clipPath id="tk"><rect x="514" y="33" width="572" height="38" rx="19"/></clipPath>'
        '</defs>'
        '<rect width="1600" height="800" fill="url(#g)" mask="url(#gm)" opacity=".35"/>'
    )
    # nav row
    c.t(PAD, 60, content.NAV_LEFT, "mono", 19, 0.1, cls="fg")
    c.t(W - PAD, 60, content.NAV_RIGHT, "mono", 19, 0.1, anchor="end", cls="fg")
    c.raw('<rect x="510" y="30" width="580" height="44" rx="22" fill="none" stroke="rgba(255,255,255,.5)" stroke-width="1.5"/>')
    unit = content.TICKER + "      "
    uw = text_width(unit, "mono", 19, 0.1)
    dot, rest = unit[0], unit[1:]
    dw = text_width(dot, "mono", 19, 0.1)
    runs = "".join(
        c.run(536 + i * uw, 59, dot, "mono", 19, 0.1, cls="ac pulse")
        + c.run(536 + i * uw + dw, 59, rest, "mono", 19, 0.1, cls="fg") for i in range(4))
    c.raw(f'<g clip-path="url(#tk)"><g class="tick">{runs}</g></g>')
    c.raw(f'<line x1="0" y1="104" x2="1600" y2="104" stroke="{LINE}" stroke-width="1.5"/>')

    # name
    l1, l2 = content.NAME_LINES
    pre, post = content.OUTLINED_PREFIX, l2[len(content.OUTLINED_PREFIX):]
    max_name = W - PAD - 150  # keep clear of the vertical text
    c.t(PAD - 6, 310, l1, "display", NAME_SIZE, NAME_TRACK, max_w=max_name)
    assert_fits(l2, "display", NAME_SIZE, max_name, NAME_TRACK)
    sw = 2.5 * _metrics("display")[2] / NAME_SIZE  # stroke is in glyph units
    c.t(PAD - 6, 460, pre, "display", NAME_SIZE, NAME_TRACK,
        extra=f' style="fill:none" stroke="{FG}" stroke-width="{sw:.1f}"')
    c.t(PAD - 6 + text_width(pre, "display", NAME_SIZE, NAME_TRACK), 460, post, "display", NAME_SIZE, NAME_TRACK)

    # scan line
    c.raw('<rect x="0" y="548" width="1600" height="3" fill="url(#scan)" filter="url(#glow)" opacity=".9"/>'
          '<rect x="0" y="549" width="1600" height="1.2" fill="url(#scan)"/>')

    # role + tagline
    c.t(PAD, 626, content.ROLE, "mono", 20, 0.12)
    c.t(PAD + text_width(content.ROLE, "mono", 20, 0.12) + 24, 628, content.TAGLINE, "serif", 44,
        max_w=W - PAD - 170 - text_width(content.ROLE, "mono", 20, 0.12))

    # vertical labels
    c.t(0, 0, content.VERT_BIG, "display", 54, -0.04, extra=f' transform="translate({W - PAD - 40},150) rotate(90)"',
        max_w=560)
    c.t(0, 0, content.VERT_SMALL, "mono", 17, 0.1, extra=f' transform="translate({W - PAD - 96},152) rotate(90)"')

    # footer
    a, b, z = content.HERO_FOOT
    c.t(PAD, 752, a, "mono", 18, 0.08)
    c.t(W / 2, 752, b, "mono", 18, 0.08, anchor="middle")
    c.t(W - PAD, 752, z, "mono", 18, 0.08, anchor="end")

    css = (f"@keyframes ticker{{to{{transform:translateX(-{uw:.1f}px)}}}}"
           ".tick{animation:ticker 12s linear infinite}")
    return c.doc(W, H, css, title="Sherwin Vahidimowlavi, Data Scientist. Available for full-time, Dec 2026.")
