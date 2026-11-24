#!/usr/bin/env python3
"""Render the front page for Monday 23 November 2026 as a 1024x1024 PNG.

Newspaper-style front page: masthead, one lead story (Nvidia / Huang),
a 2x2 grid of the day's other big stories, and an "also on Monday" strip.
All facts come from the research file news-image-20261123-research.md
(Reuters, AP, BBC, WSJ, TechCrunch, 23 Nov 2026). No network, no fonts
outside the system DejaVu set. Deterministic output.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 30

PAPER = (247, 243, 232)
INK = (26, 26, 26)
RED = (176, 42, 30)
NAVY = (20, 33, 61)
GREEN = (30, 122, 52)
CHIP_BG = (234, 245, 236)
GOLD = (201, 162, 39)
GREY = (110, 105, 95)
RULE = (26, 26, 26)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap using real text widths."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill=INK, leading=None):
    lines = wrap(draw, text, fnt, max_w)
    lh = leading or int(fnt.size * 1.28)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def center(draw, cx, y, text, fnt, fill=INK):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return w


def rule(draw, x0, x1, y, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- icons
def icon_ship(draw, x, y, s, fg):
    # hull
    draw.polygon([(x, y + s * 0.62), (x + s, y + s * 0.62),
                  (x + s * 0.82, y + s * 0.88), (x + s * 0.18, y + s * 0.88)],
                 fill=fg)
    # mast + sail
    draw.line([(x + s * 0.5, y + s * 0.08), (x + s * 0.5, y + s * 0.62)],
              fill=fg, width=max(2, s // 18))
    draw.polygon([(x + s * 0.54, y + s * 0.12), (x + s * 0.54, y + s * 0.55),
                  (x + s * 0.88, y + s * 0.55)], fill=fg)
    # waves
    for i, wx in enumerate((0.05, 0.38, 0.70)):
        draw.arc([x + s * wx, y + s * 0.90, x + s * (wx + 0.26), y + s * 1.02],
                 180, 360, fill=fg, width=max(2, s // 22))


def icon_dome(draw, x, y, s, fg):
    # capitol dome: base, columns, dome
    draw.rectangle([x + s * 0.06, y + s * 0.78, x + s * 0.94, y + s * 0.88],
                   fill=fg)
    for cx in (0.18, 0.38, 0.58, 0.78):
        draw.rectangle([x + s * cx, y + s * 0.52, x + s * (cx + 0.07),
                        y + s * 0.78], fill=fg)
    draw.rectangle([x + s * 0.10, y + s * 0.46, x + s * 0.90, y + s * 0.52],
                   fill=fg)
    draw.pieslice([x + s * 0.22, y + s * 0.08, x + s * 0.78, y + s * 0.62],
                  180, 360, fill=fg)
    draw.rectangle([x + s * 0.47, y + s * 0.02, x + s * 0.53, y + s * 0.14],
                   fill=fg)


def icon_shield(draw, x, y, s, fg):
    draw.polygon([(x + s * 0.5, y + s * 0.04), (x + s * 0.94, y + s * 0.18),
                  (x + s * 0.94, y + s * 0.55), (x + s * 0.5, y + s * 0.96),
                  (x + s * 0.06, y + s * 0.55), (x + s * 0.06, y + s * 0.18)],
                 fill=fg)
    # check mark in paper colour
    draw.line([(x + s * 0.28, y + s * 0.52), (x + s * 0.44, y + s * 0.68),
               (x + s * 0.74, y + s * 0.34)], fill=PAPER,
              width=max(3, s // 12), joint="curve")


def icon_coin(draw, x, y, s, fg):
    draw.ellipse([x + s * 0.06, y + s * 0.06, x + s * 0.94, y + s * 0.94],
                 outline=fg, width=max(3, s // 14))
    draw.ellipse([x + s * 0.20, y + s * 0.20, x + s * 0.80, y + s * 0.80],
                 fill=fg)
    fnt = SANS_B(int(s * 0.52))
    t = "$"
    tw = draw.textlength(t, font=fnt)
    th = fnt.size
    draw.text((x + (s - tw) / 2, y + (s - th) / 2 - s * 0.04), t,
              font=fnt, fill=PAPER)


ICONS = {"ship": icon_ship, "dome": icon_dome,
         "shield": icon_shield, "coin": icon_coin}


def draw_card(draw, x, y, w, h, kicker, headline, body, icon):
    # icon tile
    ts = 54
    draw.rectangle([x, y, x + ts, y + ts], fill=NAVY)
    ICONS[icon](draw, x + 5, y + 5, ts - 10, (247, 243, 232))
    draw.text((x + ts + 12, y + 8), kicker, font=SANS_B(15), fill=RED)
    draw.text((x + ts + 12, y + 30), "23 NOV 2026", font=SANS(13), fill=GREY)
    hy = y + ts + 10
    hy = draw_wrapped(draw, x, hy, headline, SERIF_B(25), w, leading=30)
    draw_wrapped(draw, x, hy + 4, body, SANS(18), w, leading=24)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0, x1 = MARGIN, W - MARGIN

    # ---------------------------------------------------------- masthead
    center(d, W // 2, 20, "THE DAY'S WORLD NEWS", SANS_B(16), GREY)
    center(d, W // 2, 42, "THE WORLD IN ONE PAGE", SERIF_B(56))
    rule(d, x0, x1, 116, 3)
    rule(d, x0, x1, 121, 1)
    center(d, W // 2, 130, "MONDAY 23 NOVEMBER 2026", SANS_B(22), RED)

    # ---------------------------------------------------------- lead story
    ly = 168
    d.text((x0, ly), "LEAD STORY  ·  MARKETS  ·  TECH", font=SANS_B(16),
           fill=RED)
    d.text((x0, ly + 24), "HUANG IS BACK", font=SERIF_B(58), fill=INK)
    sub = ("Nvidia reinstates its co-founder as chief executive — "
           "shares jump 31%.")
    draw_wrapped(d, x0, ly + 92, sub, SERIF(25), 560, leading=32)
    body = ("Only 11 days after resigning in scandal, Jensen Huang returned "
            "to run the chipmaker he co-founded — under pressure from "
            "President Trump. The Nasdaq jumped 6.5%.")
    draw_wrapped(d, x0, ly + 162, body, SANS(19), 560, leading=25)
    # chip illustration panel
    px0, py0, px1, py1 = 622, ly, W - MARGIN, ly + 236
    d.rectangle([px0, py0, px1, py1], fill=CHIP_BG, outline=INK, width=2)
    # chip with pins
    cs = 150
    cx, cy = (px0 + px1) // 2, py0 + 14 + cs // 2
    pin = 8
    for i in range(5):
        off = 18 + i * 28
        d.rectangle([cx - cs // 2 + off, cy - cs // 2 - 14,
                     cx - cs // 2 + off + pin, cy - cs // 2 - 4], fill=GOLD)
        d.rectangle([cx - cs // 2 + off, cy + cs // 2 + 4,
                     cx - cs // 2 + off + pin, cy + cs // 2 + 14], fill=GOLD)
        d.rectangle([cx - cs // 2 - 14, cy - cs // 2 + off,
                     cx - cs // 2 - 4, cy - cs // 2 + off + pin], fill=GOLD)
        d.rectangle([cx + cs // 2 + 4, cy - cs // 2 + off,
                     cx + cs // 2 + 14, cy - cs // 2 + off + pin], fill=GOLD)
    d.rectangle([cx - cs // 2, cy - cs // 2, cx + cs // 2, cy + cs // 2],
                fill=(27, 77, 46), outline=GOLD, width=3)
    center(d, cx, cy - 26, "NVDA", SANS_B(34), (247, 243, 232))
    center(d, cx, cy + 16, "+31%", SANS_B(30), GOLD)
    center(d, (px0 + px1) // 2, py1 - 34, "SHARES ON MONDAY",
           SANS_B(16), GREEN)

    rule(d, x0, x1, 418, 2)

    # ---------------------------------------------------------- 2x2 grid
    cards = [
        ("WAR  ·  UKRAINE",
         "Ukraine sinks Russian warship off Libya",
         "Seven sea drones sank the corvette Merkury at Benghazi; a Russian "
         "arms ship was hit too.",
         "ship"),
        ("POLITICS  ·  USA",
         "Democrats win 258 House seats",
         "Largest House majority since 1992; Republicans hold at least "
         "173 seats.",
         "dome"),
        ("BUSINESS  ·  TECH",
         "CrowdStrike buys Zscaler for $43.9bn",
         "Largest cybersecurity takeover on record; Zscaler holders get a "
         "34% premium.",
         "shield"),
        ("CRIME  ·  CRYPTO",
         "US seeks $1bn in stolen Binance crypto",
         "Justice Dept. files to recover coins North Korean hackers stole "
         "from the exchange.",
         "coin"),
    ]
    cw, ch, gap = 465, 186, 34
    for i, (kick, head, txt, icon) in enumerate(cards):
        cx0 = x0 + (i % 2) * (cw + gap)
        cy0 = 436 + (i // 2) * (ch + 14)
        draw_card(d, cx0, cy0, cw, ch, kick, head, txt, icon)

    rule(d, x0, x1, 830, 2)

    # ---------------------------------------------------------- also strip
    d.rectangle([x0, 840, x1, 952], fill=NAVY)
    d.text((x0 + 16, 848), "ALSO ON MONDAY", font=SANS_B(18),
           fill=(201, 162, 39))
    items = [
        "Tajikistan starts quitting the International Criminal Court",
        "Puigdemont free to return to Spain as court drops its case",
        "Bomb threats emailed to about 450 schools in Germany",
        "3 dead, 34 missing after a candy factory fire in Indonesia",
    ]
    iy = 872
    for it in items:
        d.text((x0 + 16, iy), "•  " + it, font=SANS(18),
               fill=(247, 243, 232))
        iy += 20

    # ---------------------------------------------------------- footer
    center(d, W // 2, 966,
           "Sources: Reuters · AP · BBC · WSJ · TechCrunch — all events of "
           "Monday 23 November 2026",
           SANS(15), GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out)


if __name__ == "__main__":
    main()
