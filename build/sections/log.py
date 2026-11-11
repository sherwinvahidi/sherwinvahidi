import content
from svgkit import ACCENT, Canvas, assert_fits, panel, text

W, H = 1600, 860
PAD = 48
ROW = 22   # mono size inside panels
TRK = 0.05
HDR = 18   # panel header size


def _sep(c, x1, x2, y):
    c.raw(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="rgba(255,255,255,.08)" stroke-width="1.5"/>')


def _header(c, x, y, w, left, right):
    c.t(x + 28, y + 46, left, "mono", HDR, 0.12)
    c.t(x + w - 28, y + 46, right, "mono", HDR, 0.12, anchor="end", cls="fg")


def render() -> str:
    c = Canvas()
    c.t(PAD, 62, "01 / SYSTEM", "mono", 19, 0.1)
    h1, h2 = content.LOG_HEADING
    c.t(PAD - 3, 200, h1, "display", 96, -0.05, max_w=480)
    c.t(PAD - 3, 284, h2, "display", 96, -0.05, max_w=480)
    c.t(PAD, 352, content.LOG_SERIF, "serif", 48, max_w=480)

    # status panel, two columns of two rows
    sx, sy, sw, sh = 600, 96, W - PAD - 600, 280
    c.raw(panel(sx, sy, sw, sh))
    _header(c, sx, sy, sw, "STATUS", "01.A")
    colw = (sw - 56 - 48) / 2
    for i, (label, value) in enumerate(content.STATUS):
        col, row = i % 2, i // 2
        x0 = sx + 28 + col * (colw + 48)
        yy = sy + 136 + row * 84
        off = 0
        if i == 0:
            c.raw(f'<circle cx="{x0 + 7}" cy="{yy - 8}" r="7" fill="{ACCENT}" class="pulse"/>')
            off = 26
        lab = label.upper()
        assert_fits(lab, "mono", ROW, colw - 180 - off, TRK)
        c.use("mono", lab)
        c.raw(text(x0 + off, yy, lab, "m", ROW, TRK))
        c.t(x0 + colw, yy, value, "mono", ROW, TRK, anchor="end", cls="fg")
        _sep(c, x0, x0 + colw, yy + 28)

    # career log, full width
    lx, ly, lw, lh = PAD, 420, W - 2 * PAD, 400
    c.raw(panel(lx, ly, lw, lh))
    _header(c, lx, ly, lw, "CAREER LOG", "01.B")
    for i, (year, txt, mark) in enumerate(content.LOG):
        yy = ly + 122 + i * 60
        t = txt.upper()
        c.t(lx + 28, yy, year, "mono", ROW, TRK)
        c.t(lx + 140, yy, t, "mono", ROW, TRK, cls="fg", max_w=lw - 140 - 140)
        c.t(lx + lw - 28, yy, mark, "mono", ROW, TRK, anchor="end", cls="ac" if mark == "NOW" else "fg")
        _sep(c, lx + 28, lx + lw - 28, yy + 26)
    return c.doc(W, H, title="Status: open to full-time work, available Dec 2026, targeting data science and ML roles in the Bay Area. Career log.")
