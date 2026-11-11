import content
from svgkit import ACCENT, FG, Canvas, text_width

W, H = 1600, 230
PAD = 48


def render_band() -> str:
    c = Canvas()
    c.t(PAD, 58, "03 / CONTACT", "mono", 19, 0.1)
    c.t(PAD - 3, 178, content.CONTACT_HEADING, "display", 84, -0.05)
    x = PAD + text_width(content.CONTACT_HEADING, "display", 84, -0.05) + 28
    c.t(x, 178, content.CONTACT_SERIF, "serif", 44)
    c.raw(f'<circle cx="{W - PAD - 8}" cy="52" r="7" fill="{ACCENT}" class="pulse"/>')
    c.t(W - PAD - 28, 59, "REPLIES VIA LINKEDIN", "mono", 19, 0.1, anchor="end")
    return c.doc(W, H, title="Let's talk. I'm graduating in December.")


def render_button(kind: str) -> str:
    label = {"resume": "↓ RESUME.PDF", "linkedin": "LINKEDIN ↗"}[kind]
    w, h = 380, 76
    c = Canvas()
    if kind == "resume":
        c.raw(f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" fill="{FG}"/>')
        cls = 'style="fill:#000"'
    else:
        c.raw(f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" fill="none" stroke="rgba(255,255,255,.55)" stroke-width="2"/>')
        cls = ""
    c.t(w / 2, h / 2 + 7, label, "mono", 20, 0.12, anchor="middle", cls="fg", extra=" " + cls if cls else "", max_w=w - 40)
    return c.doc(w, h, title="Download resume (PDF)" if kind == "resume" else "LinkedIn profile")
