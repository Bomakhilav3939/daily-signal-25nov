#!/usr/bin/env python3
"""One day of world news - Tuesday 24 November 2026.
Local build of entry.png: 1024x1024 digest from news25.json, drawn with bundled fonts.
Deterministic: no network, no time, no randomness. Re-run to regenerate entry.png byte for byte.
The graded entrypoint is main.py, which ships entry.png into /output in the standard library only."""
import json
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 16
INK = (28, 26, 24)
PAPER = (251, 249, 243)
CREAM = (241, 237, 227)
RED = (172, 30, 30)
GRAY = (112, 108, 100)
LINE = (208, 203, 192)
SEA = (214, 224, 228)

TAG_STYLE = {
    "CONFIRMED": ((24, 108, 54), (222, 240, 229)),
    "OFFICIAL": ((138, 90, 0), (250, 239, 210)),
    "REPORTED": ((21, 82, 150), (222, 236, 250)),
    "CLAIM": ((176, 60, 12), (252, 234, 222)),
    "ONGOING": ((148, 28, 28), (247, 226, 226)),
}
REGION_COLOR = {
    "EUROPE": (30, 90, 180),
    "MIDDLE EAST": (198, 90, 20),
    "ASIA": (188, 42, 42),
    "AFRICA": (24, 122, 60),
    "OCEANIA": (14, 128, 118),
    "AMERICAS": (110, 55, 168),
    "WORLD": (84, 84, 90),
}

BASE = os.path.dirname(os.path.abspath(__file__))
_fc = {}


def F(size, bold=False, serif=False):
    key = (serif, bold, size)
    if key not in _fc:
        if serif and bold:
            p = "DejaVuSerif-Bold.ttf"
        elif bold:
            p = "DejaVuSans-Bold.ttf"
        else:
            p = "DejaVuSans.ttf"
        _fc[key] = ImageFont.truetype(os.path.join(BASE, "fonts", p), size)
    return _fc[key]


def tw(d, text, font):
    return d.textlength(text, font=font)


def fit(d, text, font, maxw):
    if tw(d, text, font) <= maxw:
        return text
    while text and tw(d, text + "\u2026", font) > maxw:
        text = text[:-1]
    return text.rstrip() + "\u2026"


def wrap(d, text, font, maxw, n):
    words = text.split()
    lines = []
    cur = ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if tw(d, t, font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = wd
            if len(lines) == n:
                break
    if len(lines) < n and cur and (not lines or cur != lines[-1]):
        lines.append(cur)
    while len(lines) < n:
        lines.append("")
    if lines:
        lines[-1] = fit(d, lines[-1], font, maxw)
    return lines


def ls(d, xy, text, font, fill, sp=1.0):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += tw(d, ch, font) + sp
    return x


def pill(d, x, y, text, fg, bg, font, pad=4):
    wpx = tw(d, text, font) + pad * 2
    h = font.size + 4
    d.rounded_rectangle([x, y, x + wpx, y + h], radius=h // 2, fill=bg)
    d.text((x + pad, y + 2), text, font=font, fill=fg)
    return wpx


def num(d, cx, cy, n, color, r=9, fs=9):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    f = F(fs, bold=True)
    s = str(n)
    d.text((cx - tw(d, s, f) / 2, cy - fs * 0.78), s, font=f, fill=(255, 255, 255))


def label(d, x, y, text):
    ls(d, (x, y), text, F(8, bold=True), GRAY, sp=1.4)


def rule(d, x0, x1, y, wdt=2):
    d.line([x0, y, x1, y], fill=INK, width=wdt)


# ---------- world map: land spans (row, col0, col1) on a 60x30 equirect grid ----------
# col = (lon+180)/6, row = (84-lat)/5.6
MASK = [
    (0, 18, 20), (0, 32, 34), (0, 52, 58),
    (1, 10, 28), (1, 31, 34), (1, 40, 59),
    (2, 10, 28), (2, 27, 27), (2, 31, 59),
    (3, 10, 18), (3, 26, 27), (3, 30, 59),
    (4, 10, 17), (4, 27, 58),
    (5, 9, 17), (5, 27, 58),
    (6, 7, 17), (6, 27, 55),
    (7, 7, 17), (7, 30, 49), (7, 50, 50), (7, 52, 54),
    (8, 9, 15), (8, 28, 47), (8, 52, 54),
    (9, 10, 13), (9, 28, 48),
    (10, 10, 13), (10, 28, 47), (10, 52, 54),
    (11, 13, 15), (11, 29, 32), (11, 34, 36), (11, 41, 41), (11, 45, 45), (11, 49, 50),
    (12, 14, 17), (12, 29, 33), (12, 34, 36), (12, 44, 48), (12, 49, 50),
    (13, 14, 18), (13, 29, 33), (13, 34, 36), (13, 45, 46), (13, 50, 52),
    (14, 17, 19), (14, 29, 35), (14, 45, 48), (14, 49, 52),
    (15, 30, 36), (15, 46, 48), (15, 49, 52), (15, 52, 58),
    (16, 31, 34), (16, 37, 38), (16, 49, 58),
    (17, 32, 34), (17, 37, 38), (17, 49, 58),
    (18, 16, 24), (18, 33, 34), (18, 49, 58),
    (19, 16, 23), (19, 33, 35), (19, 51, 56),
    (20, 16, 21), (20, 51, 56),
    (21, 17, 19), (21, 53, 54),
    (22, 17, 19),
    (23, 15, 17),
    (24, 0, 11), (24, 18, 59),
    (25, 0, 9), (25, 19, 59),
    (26, 0, 59), (27, 0, 59), (28, 0, 59), (29, 0, 59),
]


def draw_map(d, x, y, cell=4.8):
    for c in range(60):
        for r in range(30):
            px, py = x + c * cell, y + r * cell
            d.ellipse([px + 0.5, py + 0.5, px + cell - 1.3, py + cell - 1.3], fill=SEA)
    for (r, c0, c1) in MASK:
        for c in range(c0, c1 + 1):
            px, py = x + c * cell, y + r * cell
            d.ellipse([px + 0.4, py + 0.4, px + cell - 1.1, py + cell - 1.1], fill=(160, 152, 134))


ILL = {}

def _tanker(d, x, y, w, h, acc):
    sea = y + h - 14
    d.line([x, sea, x + w, sea], fill=(46, 66, 96), width=3)
    d.polygon([(x + w*0.08, sea), (x + w*0.92, sea), (x + w*0.86, sea - 16), (x + w*0.14, sea - 16)], fill=(52, 52, 58))
    d.rectangle([x + w*0.62, sea - 30, x + w*0.78, sea - 16], fill=(62, 62, 68))
    d.rectangle([x + w*0.66, sea - 38, x + w*0.70, sea - 30], fill=(72, 72, 78))
    for i, fx in enumerate((0.18, 0.42, 0.88)):
        fx = x + w * fx
        d.polygon([(fx - 12, sea - 10), (fx - 3, sea - 30), (fx + 1, sea - 46 - 8 * (i % 2)), (fx + 6, sea - 30), (fx + 12, sea - 10)], fill=(228, 118, 20))
        d.polygon([(fx - 6, sea - 10), (fx + 1, sea - 34 - 6 * (i % 2)), (fx + 7, sea - 10)], fill=(250, 200, 60))


def _market(d, x, y, w, h, acc):
    base = y + h - 8
    d.line([x + 4, base, x + w - 4, base], fill=LINE, width=1)
    for cx_, tp in zip((0.14, 0.30, 0.46, 0.62, 0.78), (0.72, 0.55, 0.62, 0.38, 0.16)):
        cx_ = x + w * cx_
        d.rectangle([cx_ - 4, y + h * tp, cx_ + 4, base], fill=(30, 130, 60))
    d.line([x + w*0.10, y + h*0.78, x + w*0.84, y + h*0.20], fill=(200, 60, 40), width=2)
    d.polygon([(x + w*0.88, y + h*0.18), (x + w*0.78, y + h*0.20), (x + w*0.85, y + h*0.28)], fill=(200, 60, 40))


def _drone(d, x, y, w, h, acc):
    bx = x + w * 0.60
    d.rectangle([bx, y + h*0.35, bx + w*0.34, y + h - 6], fill=(122, 118, 110))
    d.line([bx + w*0.10, y + h*0.35, bx + w*0.18, y + h*0.55, bx + w*0.08, y + h*0.75, bx + w*0.16, y + h - 6], fill=(58, 56, 52), width=2)
    for (dx, dy) in ((0.12, 0.25), (0.30, 0.12), (0.46, 0.34)):
        cx_, cy_ = x + w * dx, y + h * dy
        d.line([cx_-10, cy_, cx_+10, cy_], fill=acc, width=2)
        d.polygon([(cx_-7, cy_+1), (cx_, cy_-4), (cx_+7, cy_+1), (cx_, cy_+4)], fill=acc)
    d.arc([x + w*0.02, y + h*0.02, x + w*0.55, y + h*0.72], start=200, end=290, fill=GRAY, width=1)


def _radar(d, x, y, w, h, acc):
    cx_, cy_ = x + w*0.42, y + h*0.58
    for r in (10, 20, 30):
        d.arc([cx_-r, cy_-r, cx_+r, cy_+r], start=200, end=340, fill=acc, width=1)
    d.line([cx_, cy_, cx_+30, cy_-8], fill=(200, 60, 40), width=2)
    d.polygon([(cx_, cy_), (cx_+30, cy_-8), (cx_+26, cy_+4)], fill=(200, 60, 40))
    d.polygon([(x+w*0.76, y+h*0.26), (x+w*0.94, y+h*0.18), (x+w*0.86, y+h*0.36)], fill=INK)
    d.ellipse([x+w*0.80, y+h*0.62, x+w*0.90, y+h*0.72], outline=RED, width=2)
    d.text((x+w*0.835, y+h*0.635), "!", font=F(8, bold=True), fill=RED)


def _rocket(d, x, y, w, h, acc):
    cx_ = x + w*0.30
    d.polygon([(cx_, y+4), (cx_-8, y+h*0.45), (cx_+8, y+h*0.45)], fill=INK)
    d.rectangle([cx_-8, y+h*0.45, cx_+8, y+h*0.82], fill=INK)
    d.ellipse([cx_-3, y+h*0.55, cx_+3, y+h*0.65], fill=(120, 180, 220))
    d.polygon([(cx_-8, y+h*0.68), (cx_-14, y+h*0.94), (cx_-8, y+h*0.84)], fill=RED)
    d.polygon([(cx_+8, y+h*0.68), (cx_+14, y+h*0.94), (cx_+8, y+h*0.84)], fill=RED)
    d.polygon([(cx_-5, y+h*0.82), (cx_, y+h-2), (cx_+5, y+h*0.82)], fill=(240, 160, 40))
    d.ellipse([x+w*0.55, y+h*0.08, x+w*0.95, y+h*0.78], outline=GRAY, width=1)
    d.ellipse([x+w*0.78, y+h*0.14, x+w*0.90, y+h*0.30], fill=(204, 200, 190))
    d.ellipse([x+w*0.80, y+h*0.17, x+w*0.86, y+h*0.26], fill=(172, 168, 158))
    for (sx, sy) in ((0.60, 0.55), (0.68, 0.82), (0.92, 0.62)):
        d.rectangle([x+w*sx, y+h*sy, x+w*sx+2, y+h*sy+2], fill=GRAY)


def _scales(d, x, y, w, h, acc):
    cx_ = x + w*0.5
    d.line([cx_, y+6, cx_, y+h-14], fill=INK, width=3)
    d.rectangle([cx_-16, y+h-14, cx_+16, y+h-8], fill=INK)
    d.line([x+w*0.18, y+14, x+w*0.82, y+14], fill=INK, width=3)
    for px_ in (x + w*0.18, x + w*0.82):
        d.line([px_, y+14, px_-8, y+h*0.52], fill=INK, width=1)
        d.line([px_, y+14, px_+8, y+h*0.52], fill=INK, width=1)
        d.arc([px_-10, y+h*0.42, px_+10, y+h*0.66], start=0, end=180, fill=acc, width=3)
    d.ellipse([cx_-4, y+10, cx_+4, y+18], fill=RED)


def _blast(d, x, y, w, h, acc):
    bx = x + w * 0.55
    d.rectangle([bx, y + h*0.30, bx + w*0.38, y + h - 6], fill=(122, 118, 110))
    cx_, cy_ = x + w*0.38, y + h*0.42
    pts = []
    for i in range(16):
        import math
        ang = i * 22.5 * 3.14159 / 180
        r = 22 if i % 2 == 0 else 11
        pts.append((cx_ + r * math.cos(ang), cy_ + r * math.sin(ang)))
    d.polygon(pts, fill=(228, 118, 20))
    d.polygon([(cx_-8, cy_), (cx_+5, cy_-6), (cx_+8, cy_+6)], fill=(250, 200, 60))
    for (sx, sy, sr) in ((0.20, 0.12, 5), (0.30, 0.06, 4), (0.52, 0.10, 5)):
        d.ellipse([x+w*sx-sr, y+h*sy-sr, x+w*sx+sr, y+h*sy+sr], fill=(160, 156, 148))


def _gaza(d, x, y, w, h, acc):
    d.rectangle([x + w*0.30, y + h*0.25, x + w*0.70, y + h - 8], fill=(200, 196, 184))
    d.rectangle([x + w*0.42, y + 6, x + w*0.58, y + h*0.25], fill=(188, 184, 172))
    d.rectangle([x + w*0.47, y + h*0.42, x + w*0.53, y + h*0.62], fill=RED)
    d.rectangle([x + w*0.42, y + h*0.49, x + w*0.58, y + h*0.55], fill=RED)
    d.line([x + w*0.20, y + h - 8, x + w*0.80, y + h - 8], fill=INK, width=2)
    cx_, cy_ = x + w*0.14, y + h*0.30
    d.line([cx_-8, cy_, cx_+8, cy_], fill=INK, width=2)
    d.polygon([(cx_-5, cy_+1), (cx_, cy_-3), (cx_+5, cy_+1), (cx_, cy_+3)], fill=INK)


def _chip(d, x, y, w, h, acc):
    cx_, cy_ = x + w*0.42, y + h*0.5
    d.rectangle([cx_-20, cy_-16, cx_+20, cy_+16], fill=INK)
    d.rectangle([cx_-12, cy_-9, cx_+12, cy_+9], fill=(70, 70, 76))
    for i in range(4):
        d.rectangle([cx_-16 + i*9, cy_-22, cx_-13 + i*9, cy_-16], fill=GRAY)
        d.rectangle([cx_-16 + i*9, cy_+16, cx_-13 + i*9, cy_+22], fill=GRAY)
    d.line([x+w*0.72, y+h*0.18, x+w*0.94, y+h*0.18], fill=RED, width=2)
    d.line([x+w*0.72, y+h*0.24, x+w*0.94, y+h*0.24], fill=RED, width=2)
    d.line([x+w*0.83, y+h*0.16, x+w*0.83, y+h*0.26], fill=RED, width=2)
    d.text((x+w*0.72, y+h*0.30), "NO BACKDOOR", font=F(6, bold=True), fill=INK)


def _quake(d, x, y, w, h, acc):
    gy = y + h*0.62
    d.line([x, gy, x + w*0.30, gy], fill=INK, width=2)
    d.line([x + w*0.30, gy, x + w*0.38, gy-6, x + w*0.44, gy+4, x + w*0.52, gy-8, x + w*0.60, gy, x + w, gy], fill=INK, width=2)
    d.polygon([(x + w*0.66, gy), (x + w*0.80, y + h*0.28), (x + w*0.94, gy)], fill=(122, 118, 110))
    for r in (8, 16, 24):
        d.arc([x + w*0.38 - r, gy - r, x + w*0.38 + r, gy + r], start=180, end=360, fill=acc, width=2)


def _migrants(d, x, y, w, h, acc):
    for i in range(5):
        fx = x + w*(0.10 + i*0.13)
        d.ellipse([fx-4, y+h*0.30, fx+4, y+h*0.38], fill=INK)
        d.line([fx, y+h*0.38, fx, y+h*0.62], fill=INK, width=2)
        d.line([fx, y+h*0.62, fx-4, y+h*0.80], fill=INK, width=2)
        d.line([fx, y+h*0.62, fx+4, y+h*0.80], fill=INK, width=2)
    d.line([x + w*0.82, y+h*0.55, x + w*0.94, y+h*0.55], fill=acc, width=2)
    d.polygon([(x + w*0.96, y+h*0.55), (x + w*0.92, y+h*0.50), (x + w*0.92, y+h*0.60)], fill=acc)
    d.text((x + w*0.78, y+h*0.20), "1,283", font=F(10, bold=True), fill=INK)


def _flood(d, x, y, w, h, acc):
    d.rectangle([x + w*0.35, y + h*0.20, x + w*0.65, y + h - 10], fill=(160, 156, 148))
    d.rectangle([x + w*0.40, y + h*0.28, x + w*0.45, y + h*0.38], fill=PAPER)
    d.rectangle([x + w*0.55, y + h*0.28, x + w*0.60, y + h*0.38], fill=PAPER)
    for j in range(3):
        yy = y + h*(0.62 + j*0.10)
        for i in range(8):
            d.arc([x + i*w/8, yy, x + i*w/8 + w/4, yy + 8], start=0, end=180, fill=(70, 110, 160), width=2)
    d.polygon([(x + w*0.14, y + h*0.42), (x + w*0.20, y + h*0.22), (x + w*0.26, y + h*0.42)], fill=(228, 170, 20))
    d.text((x + w*0.18, y + h*0.28), "!", font=F(8, bold=True), fill=INK)


def _ball(d, x, y, w, h, acc):
    cx_, cy_ = x + w*0.45, y + h*0.5
    d.ellipse([cx_-22, cy_-22, cx_+22, cy_+22], fill=(252, 250, 244), outline=INK, width=2)
    import math
    for i in range(5):
        ang = -90 + i * 72
        px_ = cx_ + 11 * math.cos(math.radians(ang))
        py_ = cy_ + 11 * math.sin(math.radians(ang))
        d.ellipse([px_-4, py_-4, px_+4, py_+4], fill=INK)
    for i in range(5):
        ang = -90 + i * 72 + 36
        d.line([cx_ + 11 * math.cos(math.radians(ang)), cy_ + 11 * math.sin(math.radians(ang)),
                cx_ + 21 * math.cos(math.radians(ang)), cy_ + 21 * math.sin(math.radians(ang))], fill=INK, width=1)
    d.line([x + w*0.74, y + h - 6, x + w*0.74, y + h*0.18], fill=acc, width=3)
    d.line([x + w*0.94, y + h - 6, x + w*0.94, y + h*0.18], fill=acc, width=3)
    d.line([x + w*0.74, y + h*0.18, x + w*0.94, y + h*0.18], fill=acc, width=3)


ILL = {
    "tanker": _tanker, "market": _market, "drone": _drone, "radar": _radar,
    "rocket": _rocket, "scales": _scales, "blast": _blast, "gaza": _gaza,
    "chip": _chip, "quake": _quake, "migrants": _migrants, "flood": _flood,
    "ball": _ball, "drones": _drone, "explosion": _blast, "football": _ball, "radar": _radar, "chip": _chip,
}


def render(path):
    with open(os.path.join(BASE, "news25.json"), encoding="utf-8") as f:
        data = json.load(f)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # top + bottom bars
    d.rectangle([0, 0, W, 5], fill=RED)
    d.rectangle([0, H - 5, W, H], fill=INK)

    # masthead
    ls(d, (M, 14), data["kicker"], F(11, bold=True), INK, sp=2.0)
    meta = data["meta"]
    fm = F(9, bold=True)
    d.text((W - M - tw(d, meta, fm), 16), meta, font=fm, fill=GRAY)
    d.text((M, 30), data["date"], font=F(42, bold=True, serif=True), fill=INK)
    d.text((M, 86), data["deck"], font=F(11, serif=True), fill=(70, 66, 60))
    rule(d, M, W - M, 102, 2)
    d.line([M, 105, W - M, 105], fill=INK, width=1)

    # region tabs
    counts = {}
    for s in data["leads"] + data["cards"]:
        counts[s["region"]] = counts.get(s["region"], 0) + 1
    for s in data["briefs"]:
        counts[s[2]] = counts.get(s[2], 0) + 1
    tx = M
    for reg in ("EUROPE", "MIDDLE EAST", "ASIA", "AFRICA", "OCEANIA", "AMERICAS", "WORLD"):
        cc = counts.get(reg, 0)
        t = "%s  %d" % (reg, cc)
        wpx = tw(d, t, F(8.5, bold=True)) + 12
        c = REGION_COLOR[reg]
        d.rounded_rectangle([tx, 110, tx + wpx, 131], radius=10, outline=c, width=1)
        d.ellipse([tx + 6, 117, tx + 11, 122], fill=c)
        d.text((tx + 15, 115), t, font=F(8.5, bold=True), fill=INK)
        tx += wpx + 6

    # THE DAY IN UTC
    label(d, M, 138, "THE DAY IN UTC")
    slot_w = (W - 2 * M) / 5
    for i, ev in enumerate(data["utc"]):
        ex = M + i * slot_w
        d.line([ex, 146, ex, 172], fill=LINE, width=1)
        d.text((ex + 5, 146), ev[0], font=F(10, bold=True), fill=RED)
        d.text((ex + 5, 158), ev[1], font=F(7.5, bold=True), fill=GRAY)
        d.text((ex + 5, 166), fit(d, ev[2], F(8), slot_w - 10), font=F(8), fill=INK)

    # THE DAY IN NUMBERS
    label(d, M, 178, "THE DAY IN NUMBERS")
    cw = (W - 2 * M) / 6
    for i, st in enumerate(data["numbers"]):
        sx = M + i * cw
        d.rectangle([sx, 188, sx + cw - 8, 240], fill=CREAM)
        d.rectangle([sx, 188, sx + cw - 8, 191], fill=RED)
        d.text((sx + 8, 193), st[0], font=F(20, bold=True, serif=True), fill=INK)
        for j, ln in enumerate(wrap(d, st[1], F(7.5), cw - 20, 2)):
            d.text((sx + 8, 219 + j * 9.5), ln, font=F(7.5), fill=GRAY)

    rule(d, M, W - M, 246, 1)

    # LEADS 1-3
    ly = 252
    for i, s in enumerate(data["leads"]):
        acc = REGION_COLOR[s["region"]]
        tagfg, tagbg = TAG_STYLE[s["tag"]]
        num(d, M + 9, ly + 12, i + 1, INK, r=9, fs=9)
        d.rectangle([M + 24, ly + 3, M + 24 + tw(d, s["place"], F(9, bold=True)) + 10, ly + 19], fill=INK)
        d.text((M + 29, ly + 5), s["place"], font=F(9, bold=True), fill=PAPER)
        pill(d, M + 36 + tw(d, s["place"], F(9, bold=True)), ly + 3, s["tag"], tagfg, tagbg, F(7.5, bold=True))
        hx, hy = M + 24, ly + 24
        for j, ln in enumerate(wrap(d, s["headline"], F(18, bold=True, serif=True), 640, 2)):
            d.text((hx, hy + j * 22), ln, font=F(18, bold=True, serif=True), fill=INK)
        for j, ln in enumerate(wrap(d, s["deck"], F(10), 640, 2)):
            d.text((hx, ly + 68 + j * 12.5), ln, font=F(10), fill=(60, 56, 50))
        ls(d, (hx, ly + 95), s["source"], F(7.5, bold=True), acc, sp=1.0)
        # illustration panel
        ix, iy, iw, ih = 688, ly, 320, 104
        d.rectangle([ix, iy, ix + iw, iy + ih], fill=CREAM)
        d.rectangle([ix, iy, ix + iw, iy + 5], fill=acc)
        ILL[s["art"]](d, ix + 10, iy + 10, iw - 20, ih - 20, acc)
        ly += 108

    # CARDS 4-13
    label(d, M, 588, "STORIES 4\u201313 \u00b7 PLACE \u00b7 STATUS \u00b7 SOURCE")
    row_h = 82
    for r in range(2):
        cy = 598 + r * (row_h + 4)
        for c in range(5):
            s = data["cards"][r * 5 + c]
            cw_ = (W - 2 * M - 4 * 8) / 5
            cx = M + c * (cw_ + 8)
            acc = REGION_COLOR[s["region"]]
            tagfg, tagbg = TAG_STYLE[s["tag"]]
            d.rectangle([cx, cy, cx + cw_, cy + row_h], fill=(253, 252, 248), outline=LINE, width=1)
            d.rectangle([cx, cy, cx + cw_, cy + 3], fill=acc)
            n = s["n"]
            num(d, cx + 11, cy + 15, n, INK, r=8, fs=8)
            d.text((cx + 24, cy + 8), s["place"], font=F(8, bold=True), fill=acc)
            pill(d, cx + cw_ - tw(d, s["tag"], F(7, bold=True)) - 10, cy + 7, s["tag"], tagfg, tagbg, F(7, bold=True))
            ILL[s["art"]](d, cx + cw_ - 54, cy + 15, 44, 28, acc)
            for j, ln in enumerate(wrap(d, s["headline"], F(9.5, bold=True), cw_ - 60, 2)):
                d.text((cx + 8, cy + 24 + j * 11.5), ln, font=F(9.5, bold=True), fill=INK)
            for j, ln in enumerate(wrap(d, s["deck"], F(7.5), cw_ - 16, 2)):
                d.text((cx + 8, cy + 49 + j * 9.5), ln, font=F(7.5), fill=(70, 66, 60))
            ls(d, (cx + 8, cy + row_h - 11), s["source"], F(6.5, bold=True), acc, sp=0.8)

    # ALSO ON TUESDAY: 21 briefs + map
    label(d, M, 772, "ALSO ON TUESDAY 24 NOVEMBER \u00b7 21 MORE, BY REGION")
    bw = (W - 2 * M - 300) / 2 - 4
    by = 782
    for i, s in enumerate(data["briefs"]):
        col = i // 11
        row = i % 11
        bx = M + col * (bw + 8)
        yy = by + row * 15
        acc = REGION_COLOR[s[2]]
        d.text((bx, yy), "%d" % (14 + i), font=F(7, bold=True), fill=GRAY)
        pw = tw(d, s[1], F(7.5, bold=True)) + 4
        d.text((bx + 14, yy), s[1], font=F(7.5, bold=True), fill=acc)
        d.text((bx + 18 + pw, yy), fit(d, s[0], F(7.5), bw - pw - 18), font=F(7.5), fill=INK)

    # map panel
    mx, my, mw = 712, 782, 296
    d.rectangle([mx, my, mx + mw, my + 165], fill=CREAM, outline=LINE, width=1)
    label(d, mx + 8, my + 6, "WHERE IT HAPPENED \u00b7 PIN = DRAWN STORY")
    draw_map(d, mx + 4, my + 20)
    pins = []
    for i, s in enumerate(data["leads"]):
        pins.append((i + 1, s["pin"], REGION_COLOR[s["region"]]))
    for i, s in enumerate(data["cards"]):
        pins.append((s["n"], s["pin"], REGION_COLOR[s["region"]]))
    for n, (pc, pr), colr in pins:
        px, py = mx + 4 + pc * 4.8 + 2.4, my + 20 + pr * 4.8 + 2.4
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=colr, outline=PAPER, width=1)
        fs_ = F(6.5, bold=True)
        d.text((px - tw(d, str(n), fs_) / 2, py - 4.5), str(n), font=fs_, fill=(255, 255, 255))

    # DATE CHECK
    d.rectangle([M, 954, W - M, 990], outline=RED, width=2)
    d.text((M + 8, 958), "DATE CHECK", font=F(8, bold=True), fill=RED)
    for j, ln in enumerate(wrap(d, data["date_check"], F(7.5), W - 2 * M - 90, 2)):
        d.text((M + 86, 958 + j * 10), ln, font=F(7.5), fill=(90, 40, 40))

    # legend + footer
    lx = M
    for t in ("CONFIRMED", "OFFICIAL", "REPORTED", "CLAIM", "ONGOING"):
        fg, bg = TAG_STYLE[t]
        lx += pill(d, lx, 996, t, fg, bg, F(6.5, bold=True), pad=3) + 5
    d.text((W - M - tw(d, "DRAWN, NOT PHOTOGRAPHED \u00b7 1:1 VECTOR", F(6.5, bold=True)), 998),
           "DRAWN, NOT PHOTOGRAPHED \u00b7 1:1 VECTOR", font=F(6.5, bold=True), fill=GRAY)
    d.text((M, 1010), data["footer"], font=F(7), fill=GRAY)

    out_dir = "/output"
    if not os.path.isdir(out_dir):
        try:
            os.makedirs(out_dir)
        except OSError:
            out_dir = BASE
    target = os.path.join(out_dir, "entry.png")
    img.save(target, "PNG")
    return target


if __name__ == "__main__":
    print(render(None))
