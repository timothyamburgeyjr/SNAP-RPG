"""Draws the SNAP paper-skin pieces and writes the stylesheet that uses them.

Pieces (all drawn from fixed seeds, so the output is reproducible):
  torn/deckled page edges with a hand-ruled double border (one border-image),
  a dog-eared corner, foxing spots, an ink blot and a coffee ring.
Map-fold creases are CSS gradients, faint enough that body text keeps 14:1 contrast.

Usage:
  python wiki/theme/tools/make-paper.py preview        -> wiki/theme/preview/{a,b,c}/  (gitignored)
  python wiki/theme/tools/make-paper.py final b        -> wiki/theme/snap-paper.css + wiki/theme/paper/
"""
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

THEME = Path(__file__).resolve().parent.parent
OUT_SCALE = 2          # PNGs are drawn at 2x so they stay crisp on phones and high-DPI screens
SS = 4                 # supersampling factor on top of that, for smooth lines
FRAME, BAND = 300, 30   # CSS px: the frame image is FRAME square; BAND px of it is the border on each side

GUTTER = (236, 230, 216)   # average colour of paper-gutter.png = the margin around the sheet
CREAM = (246, 242, 234)    # the sheet itself (snap-theme.css)
TEXT = (32, 33, 34)        # Vector body text
RULE_DARK = (168, 159, 140)
RULE_SOFT = (207, 198, 179)

# How worn each option is. a = quiet, b = worn, c = old map.
OPTIONS = {
    "a": dict(name="Quiet", tear=2.2, tear_var=1.4, notches=0, edge_shade=0.20, wobble=0.35,
              crease=0.018, foxing=10, fox_alpha=0.12, ink=False, ring=False, dogear=36),
    "b": dict(name="Worn", tear=3.5, tear_var=2.4, notches=2, edge_shade=0.30, wobble=0.6,
              crease=0.026, foxing=22, fox_alpha=0.17, ink=True, ring=True, dogear=44),
    "c": dict(name="Old map", tear=5.0, tear_var=3.4, notches=4, edge_shade=0.42, wobble=0.9,
              crease=0.034, foxing=40, fox_alpha=0.22, ink=True, ring=True, dogear=52),
}


# ---------- helpers ----------

def periodic_noise(rng, n, harmonics=48, roughness=1.15):
    """Smooth random wiggle that repeats exactly every n samples (so tiles join seamlessly)."""
    x = np.arange(n) / n
    y = np.zeros(n)
    for k in range(1, harmonics + 1):
        y += rng.normal() * k ** -roughness * np.sin(2 * math.pi * (k * x + rng.random()))
    return y / np.abs(y).max()


def notch_profile(rng, n, count, depth):
    """A few small tears: sharp triangular bites out of the edge."""
    out = np.zeros(n)
    x = np.arange(n)
    for _ in range(count):
        x0, w = rng.uniform(0, n), rng.uniform(5, 14)
        dist = np.minimum(np.abs(x - x0), n - np.abs(x - x0))   # periodic distance
        out += depth * rng.uniform(0.6, 1.0) * np.clip(1 - dist / w, 0, None)
    return out


def finish(img, size):
    """Downsample the supersampled drawing to the 2x output size."""
    return img.resize((size[0] * OUT_SCALE, size[1] * OUT_SCALE), Image.LANCZOS)


def rgba(color, alpha):
    return (*color, max(0, min(255, round(alpha * 255))))


def luminance(c):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(v) for v in c)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def blend(base, top, alpha):
    return tuple(round(b + (t - b) * alpha) for b, t in zip(base, top))


# ---------- pieces ----------

def grain_canvas(css_px, s):
    """A square of the margin grain, css_px wide, drawn at the working scale s (grain is 1:1 with CSS px)."""
    tile = gutter_grain().crop((0, 0, css_px, css_px))
    return tile.resize((css_px * s, css_px * s), Image.BICUBIC).convert("RGBA")


def frame(seed, opt):
    """The whole sheet edge as one border-image: torn margin (gutter colour) outside an irregular
    line, a little shadow on the torn fibres, and a hand-ruled double border turning the corners.

    The image is FRAME x FRAME; CSS slices BAND px off each side. Every side's wiggle repeats
    every (FRAME - 2*BAND) px, measured from the slice line, so the repeated edge pieces meet each
    other and the fixed corners without a seam."""
    rng = np.random.default_rng(seed)
    s = OUT_SCALE * SS
    size, period, per = FRAME * s, FRAME - 2 * BAND, 4          # `per` samples per CSS px

    def profile(base, var, fuzz, notches, harmonics=48, roughness=0.9):
        p = base + var * (periodic_noise(rng, period * per, harmonics, roughness) * 0.5 + 0.5)
        if fuzz:
            p += fuzz * periodic_noise(rng, period * per, harmonics=160, roughness=0.6)
        p += notch_profile(rng, period * per, notches, base * 1.6) if notches else 0
        return p

    def along(p, t):
        """Value of a side's profile at position t (CSS px from the start of that side)."""
        return float(p[int(round(((t - BAND) % period) * per)) % len(p)])

    ts = np.linspace(0, FRAME, FRAME * per + 1)
    tears = [np.clip(profile(opt["tear"], opt["tear_var"], 0.6, opt["notches"]), 0.8, None) for _ in range(4)]
    top, right, bottom, left = tears

    def outline(insets):
        """Closed loop just inside the edge, `insets` = per-side function of position."""
        it, ir, ib, il = insets
        pts = [(t, it(t)) for t in ts]
        pts += [(FRAME - ir(t), t) for t in ts]
        pts += [(t, FRAME - ib(t)) for t in ts[::-1]]
        pts += [(il(t), t) for t in ts[::-1]]
        return [(x * s, y * s) for x, y in pts]

    torn = outline([lambda t, p=p: along(p, t) for p in tears])
    gutter = grain_canvas(FRAME, s)            # torn-away paper shows the margin grain, not a flat band
    ImageDraw.Draw(gutter).polygon(torn, fill=(0, 0, 0, 0))     # the sheet itself stays transparent
    shade = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(shade).line(torn + [torn[0]], fill=rgba((150, 130, 95), opt["edge_shade"]),
                               width=round(2.2 * s), joint="curve")
    img = Image.alpha_composite(shade.filter(ImageFilter.GaussianBlur(0.7 * s)), gutter)

    d = ImageDraw.Draw(img)
    for inset, color, width, a in ((13, RULE_DARK, 1.15, 0.95), (18, RULE_SOFT, 1.0, 1.0)):
        wobs = [profile(0, opt["wobble"] * 2, 0, 0, harmonics=12, roughness=1.6) - opt["wobble"] for _ in range(4)]
        loop = outline([lambda t, p=p: inset + along(p, t) for p in wobs])
        # keep only the part of each side between the corners, so the rule turns the corner cleanly
        clipped = [(x, y) for x, y in loop if inset * s - s <= x <= (FRAME - inset) * s + s
                   and inset * s - s <= y <= (FRAME - inset) * s + s]
        d.line(clipped + [clipped[0]], fill=rgba(color, a), width=round(width * s), joint="curve")
    return finish(img, (FRAME, FRAME))


def foxing(seed, opt, size=(220, 26)):
    """A drift of small brown age spots, for the frame band at the top."""
    rng = np.random.default_rng(seed)
    s = OUT_SCALE * SS
    img = Image.new("RGBA", (size[0] * s, size[1] * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for _ in range(opt["foxing"]):
        x, y = rng.uniform(4, size[0] - 4) * s, rng.uniform(6, size[1] - 4) * s
        r = rng.uniform(0.6, 2.2) * s
        a = opt["fox_alpha"] * rng.uniform(0.4, 1.0)
        d.ellipse((x - r * 2.2, y - r * 2.2, x + r * 2.2, y + r * 2.2), fill=rgba((165, 120, 70), a * 0.3))
        d.ellipse((x - r, y - r, x + r, y + r), fill=rgba((140, 95, 50), a))
    img = img.filter(ImageFilter.GaussianBlur(0.5 * s))
    return finish(img, size)


def ink_blot(seed, size=34):
    """An old ink blot: irregular, darker at the rim where it dried, with two splatter dots."""
    rng = np.random.default_rng(seed)
    s = OUT_SCALE * SS
    c = size * s / 2
    img = Image.new("RGBA", (size * s, size * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    n = 240
    wig = periodic_noise(rng, n, harmonics=10, roughness=1.3)
    ang = np.linspace(0, 2 * math.pi, n, endpoint=False)
    rad = (size * 0.30) * s * (1 + 0.18 * wig)
    pts = [(c + r * math.cos(t), c + r * math.sin(t)) for r, t in zip(rad, ang)]
    d.polygon(pts, fill=rgba((58, 52, 72), 0.10))
    d.line(pts + [pts[0]], fill=rgba((52, 46, 66), 0.16), width=round(1.4 * s), joint="curve")
    for _ in range(2):
        t, r = rng.uniform(0, 2 * math.pi), rng.uniform(0.40, 0.46) * size * s
        x, y, rr = c + r * math.cos(t), c + r * math.sin(t), rng.uniform(0.7, 1.4) * s
        d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=rgba((58, 52, 72), 0.14))
    return finish(img.filter(ImageFilter.GaussianBlur(0.4 * s)), (size, size))


def coffee_ring(seed, size=84):
    """Part of a cup ring, uneven and broken, centred on the image."""
    rng = np.random.default_rng(seed)
    s = OUT_SCALE * SS
    c = size * s / 2
    img = Image.new("RGBA", (size * s, size * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    n = 360
    a = 0.07 + 0.06 * (periodic_noise(rng, n, harmonics=6) * 0.5 + 0.5)
    a[(np.arange(n) > 200) & (np.arange(n) < 245)] = 0          # a gap in the ring
    wid = 1.6 + 1.2 * (periodic_noise(rng, n, harmonics=8) * 0.5 + 0.5)
    r0 = size * 0.38 * s
    for i in range(n):
        t0, t1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1.5) / n
        d.arc((c - r0, c - r0, c + r0, c + r0), math.degrees(t0), math.degrees(t1),
              fill=rgba((140, 98, 52), a[i]), width=round(wid[i] * s))
    return finish(img.filter(ImageFilter.GaussianBlur(0.5 * s)), (size, size))


def dog_ear(size):
    """Bottom-right corner folded over: the corner itself is gone (gutter shows), the flap lies on the page."""
    s = OUT_SCALE * SS
    w = size * s
    img = grain_canvas(size, s)                                                  # missing corner: margin grain shows
    mask = Image.new("L", (w, w), 0)
    ImageDraw.Draw(mask).polygon([(w, 0), (w, w), (0, w)], fill=255)
    img.putalpha(mask)
    shadow = Image.new("RGBA", (w, w), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).polygon([(w, 0), (0, w), (-0.06 * w, 0.06 * w), (0.94 * w, -0.06 * w)],
                                   fill=rgba((120, 105, 80), 0.18))
    img = Image.alpha_composite(img, shadow.filter(ImageFilter.GaussianBlur(1.2 * s)))
    d = ImageDraw.Draw(img)
    flap = [(w, 0), (0, w), (0.10 * w, 0.10 * w)]                               # flap, slightly short of the corner
    d.polygon(flap, fill=rgba((232, 225, 209), 1))
    d.line(flap + [flap[0]], fill=rgba(RULE_DARK, 1), width=round(1.0 * s), joint="curve")
    return finish(img, (size, size))


def gutter_grain(strength=0.6):
    """The supplied paper-gutter.png with its grain softened (side-panel links sit on it)."""
    im = np.asarray(Image.open(THEME / "paper" / "paper-gutter.png").convert("RGB"), dtype=float)
    mean = im.reshape(-1, 3).mean(axis=0)
    return Image.fromarray(np.clip(mean + (im - mean) * strength, 0, 255).round().astype(np.uint8))


# ---------- stylesheet ----------

def crease_alpha_for_14(target, color=(110, 98, 80)):
    """Strongest crease darkness that still leaves body text at 14:1 or better on top of it."""
    a = target
    while a > 0 and contrast(TEXT, blend(CREAM, color, a)) < 14.0:
        a -= 0.001
    return round(a, 3), contrast(TEXT, blend(CREAM, color, a))


def stylesheet(key, opt):
    ca, cr = crease_alpha_for_14(opt["crease"])
    crease_dark, crease_light = f"rgba(110, 98, 80, {ca})", "rgba(255, 255, 255, 0.35)"

    def vline(pos):
        return (f"linear-gradient(90deg, transparent calc({pos} - 1px), {crease_dark} calc({pos} - 1px), "
                f"{crease_dark} {pos}, {crease_light} {pos}, {crease_light} calc({pos} + 1px), transparent calc({pos} + 1px))")

    def hline(pos):
        return vline(pos).replace("90deg", "180deg")

    layers = [  # first layer is drawn on top; the torn frame (border-image) is drawn over all of them
        ("url('paper/foxing.png')", "no-repeat", "right 64px top 4px", "220px 26px"),
    ]
    if opt["ink"]:
        layers.append(("url('paper/ink-blot.png')", "no-repeat", "right 6px top 4px", "34px 34px"))
    if opt["ring"]:
        layers.append(("url('paper/coffee-ring.png')", "no-repeat", "left -40px bottom -40px", "84px 84px"))
    layers += [(vline("33.33%"), "no-repeat", "0 0", "100% 100%"),
               (vline("66.67%"), "no-repeat", "0 0", "100% 100%"),
               (hline("50%"), "no-repeat", "0 0", "100% 100%")]
    phone_layers = [l for l in layers if "ink-blot" not in l[0] and "coffee-ring" not in l[0]]

    def bg(ls, indent="\t\t"):
        j = (",\n" + indent)
        return (f"background-image:\n{indent}{j.join(l[0] for l in ls)};\n"
                f"\tbackground-repeat: {', '.join(l[1] for l in ls)};\n"
                f"\tbackground-position: {', '.join(l[2] for l in ls)};\n"
                f"\tbackground-size: {', '.join(l[3] for l in ls)};\n"
                f"\tbackground-origin: border-box;")

    day = "html.skin-theme-clientpref-day"
    os_ = "html.skin-theme-clientpref-os"
    rules = f"""
/* margins around the sheet: the supplied low-contrast grain */
{{ROOT}} {{
	background-image: url('paper/gutter-grain.png');
}}

/* body, header and the pinned side panels are painted with a solid colour; let the grain show through */
{{ROOT}} body,
{{ROOT}} .mw-page-container,
{{ROOT}} .vector-header,
{{ROOT}} .vector-pinned-container {{
	background-color: transparent;
}}
{{ROOT}} .vector-sticky-pinned-container::after {{
	background: none;
}}

/* the sheet: flat cream where text sits; torn edges, ruled border, creases and stains only at the frame */
{{ROOT}} #bodyContent.vector-body {{
	position: relative;
	margin-top: 10px;
	border: {BAND}px solid transparent;
	border-image: url('paper/frame.png') {BAND * OUT_SCALE} / {BAND}px round;
	padding: 12px 16px 24px;
	background-color: {'#%02x%02x%02x' % CREAM};
	{bg(layers)}
}}

/* dog-eared corner (decorative only) */
{{ROOT}} #bodyContent.vector-body::after {{
	content: '';
	position: absolute;
	right: -{BAND}px;
	bottom: -{BAND}px;
	width: {opt['dogear']}px;
	height: {opt['dogear']}px;
	background: url('paper/dog-ear.png') 0 0 / 100% 100% no-repeat;
	pointer-events: none;
}}

/* serif headings with a thin rule, like a printed book */
{{ROOT}} .mw-body h1,
{{ROOT}} #bodyContent.vector-body h2 {{
	font-family: Georgia, 'Iowan Old Style', 'Palatino Linotype', serif;
}}

/* phones: a slimmer frame, and no ink blot or ring where they could reach the text */
@media (max-width: 639px) {{
	{{ROOT}} #bodyContent.vector-body {{
		border-width: 22px;
		border-image-width: 22px;
		padding: 8px 6px 18px;
		{bg(phone_layers, chr(9) * 3).replace(chr(10) + chr(9) + 'background-', chr(10) + chr(9) * 2 + 'background-')}
	}}
}}
"""
    css = rules.replace("{ROOT}", day)
    css_os = rules.replace("{ROOT}", os_)
    header = f"""/* SNAP wiki - paper skin, option {key.upper()} ("{opt['name']}")
 * Generated by wiki/theme/tools/make-paper.py - edit the script, not this file.
 *
 * EASY ON THE EYES, ON PURPOSE
 *  - Text sits on flat cream. Texture is only in the page margins and the frame band.
 *  - Map-fold creases cross the page but are capped so body text keeps >= 14:1 (here {cr:.2f}:1 at a crease).
 *  - No animation. Light mode only: dark mode keeps Vector's own palette.
 *  - Readers who ask their device for more contrast get a plain page.
 */
"""
    plain = f"""
/* more contrast requested: no texture, no edges, no folds */
@media (prefers-contrast: more) {{
	{day}, {os_} {{ background-image: none; }}
	{day} #bodyContent.vector-body, {os_} #bodyContent.vector-body {{ background-image: none; border-image: none; }}
	{day} #bodyContent.vector-body::after, {os_} #bodyContent.vector-body::after {{ display: none; }}
}}
"""
    return (header + "@media screen {\n" + css + "}\n\n"
            "@media screen and (prefers-color-scheme: light) {\n" + css_os + "}\n" + plain), cr


def build(key, out_dir):
    opt = OPTIONS[key]
    paper = out_dir / "paper"
    paper.mkdir(parents=True, exist_ok=True)
    base = {"a": 100, "b": 200, "c": 300}[key]
    frame(base + 1, opt).save(paper / "frame.png", optimize=True)
    foxing(base + 5, opt).save(paper / "foxing.png", optimize=True)
    if opt["ink"]:
        ink_blot(base + 6).save(paper / "ink-blot.png", optimize=True)
    if opt["ring"]:
        coffee_ring(base + 7).save(paper / "coffee-ring.png", optimize=True)
    dog_ear(opt["dogear"]).save(paper / "dog-ear.png", optimize=True)
    gutter_grain().save(paper / "gutter-grain.png", optimize=True)
    css, cr = stylesheet(key, opt)
    (out_dir / "snap-paper.css").write_text(css, encoding="utf-8", newline="\n")
    size = sum(f.stat().st_size for f in paper.glob("*.png") if f.name != "gutter-grain.png")
    print(f"option {key} ({opt['name']}): {out_dir}  drawn pieces {size // 1024} KB, text at a crease {cr:.2f}:1")


if __name__ == "__main__":
    print(f"body text on flat cream: {contrast(TEXT, CREAM):.2f}:1")
    if sys.argv[1:2] == ["preview"]:
        for k in OPTIONS:
            build(k, THEME / "preview" / k)
    elif sys.argv[1:2] == ["final"] and sys.argv[2:3] and sys.argv[2] in OPTIONS:
        build(sys.argv[2], THEME)
    else:
        sys.exit(__doc__)
