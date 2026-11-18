#!/usr/bin/env python3
"""Draw entry.png: a one-page newspaper front page summing up the world news
of Tuesday 17 November 2026. Run: python3 draw_news.py  ->  entry.png
Only Pillow is needed at draw time; the submitted entrypoint (main.py) is
stdlib-only and just copies the finished image into the output directory."""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (20, 24, 34)
NAVY = (20, 33, 61)
RED = (178, 34, 34)
GREY = (90, 92, 98)
RULE = (180, 175, 160)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, fill=INK, max_lines=None):
    lines = wrap(draw, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def icon_bridge(d, box, c):
    x0, y0, x1, y1 = box
    d.line([(x0 + 6, y1 - 22), (x1 - 6, y1 - 22)], fill=c, width=6)
    d.arc([x0 + 8, y1 - 62, x0 + 62, y1 - 8], 180, 360, fill=c, width=5)
    d.arc([x0 + 62, y1 - 62, x1 - 8, y1 - 8], 180, 360, fill=c, width=5)
    d.line([(x0 + 14, y1 - 22), (x0 + 14, y1 - 4)], fill=c, width=5)
    d.line([(x0 + 62, y1 - 22), (x0 + 62, y1 - 4)], fill=c, width=5)
    d.line([(x1 - 14, y1 - 22), (x1 - 14, y1 - 4)], fill=c, width=5)


def icon_radar(d, box, c):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    r = (x1 - x0) // 2 - 4
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=5)
    d.ellipse([cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2],
              outline=c, width=3)
    d.line([(cx, cy), (cx + r - 6, cy - r + 10)], fill=c, width=5)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=c)
    d.ellipse([cx + r - 14, cy + 4, cx + r - 4, cy + 14], fill=c)


def icon_summit(d, box, c):
    x0, y0, x1, y1 = box
    for cx in (x0 + 22, (x0 + x1) // 2, x1 - 22):
        d.ellipse([cx - 13, y0 + 14, cx + 13, y0 + 40], fill=c)
        d.pieslice([cx - 18, y0 + 44, cx + 18, y0 + 78], 180, 360, fill=c)
    d.line([(x0 + 4, y1 - 8), (x1 - 4, y1 - 8)], fill=c, width=5)


def icon_lock(d, box, c):
    x0, y0, x1, y1 = box
    d.rounded_rectangle([x0 + 12, y0 + 34, x1 - 12, y1 - 6], 6,
                        outline=c, width=6)
    d.arc([x0 + 22, y0 + 8, x1 - 22, y0 + 44], 180, 360, fill=c, width=6)
    d.ellipse([(x0 + x1) // 2 - 6, y0 + 50, (x0 + x1) // 2 + 6, y0 + 62],
              fill=c)
    d.line([((x0 + x1) // 2, y0 + 58), ((x0 + x1) // 2, y0 + 74)],
           fill=c, width=6)


def icon_ship(d, box, c):
    x0, y0, x1, y1 = box
    d.polygon([(x0 + 6, y0 + 46), (x1 - 6, y0 + 46),
               (x1 - 18, y1 - 18), (x0 + 18, y1 - 18)], fill=c)
    d.rectangle([x0 + 20, y0 + 26, x1 - 20, y0 + 46], fill=c)
    d.line([(x0 + 34, y0 + 26), (x0 + 34, y0 + 10)], fill=c, width=4)
    for wy in (y1 - 10, y1 - 2):
        d.arc([x0 + 4, wy - 8, x0 + 34, wy + 8], 0, 180, fill=c, width=4)
        d.arc([x0 + 36, wy - 8, x0 + 66, wy + 8], 0, 180, fill=c, width=4)
        d.arc([x0 + 68, wy - 8, x1 - 4, wy + 8], 0, 180, fill=c, width=4)


def story_block(d, x, y, w, h, kicker, headline, body, icon, accent):
    """One story: icon tile left, kicker + headline + body right."""
    tile = 92
    d.rounded_rectangle([x, y, x + tile, y + tile], 10, fill=accent)
    icon(d, (x + 8, y + 8, x + tile - 8, y + tile - 8), (255, 255, 255))
    tx = x + tile + 16
    tw = w - tile - 16
    d.text((tx, y + 2), kicker, font=font(SANS_B, 19), fill=RED)
    y2 = para(d, tx, y + 30, headline, font(SANS_B, 27), tw, 33,
              max_lines=2)
    para(d, tx, y2 + 4, body, font(SANS, 21), tw, 27, max_lines=3)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.text((36, 22), "THE WORLD IN ONE DAY", font=font(SERIF, 58),
           fill=(255, 255, 255))
    d.text((36, 100), "TUESDAY  17  NOVEMBER  2026",
           font=font(SANS_B, 26), fill=(255, 214, 90))
    d.text((W - 36, 104), "WORLD NEWS", font=font(SANS_B, 24),
           fill=(200, 205, 220), anchor="ra")

    # Lead story
    y = 176
    d.text((36, y), "EUROPE  ·  RUSSIA–UKRAINE WAR", font=font(SANS_B, 20),
           fill=RED)
    y = para(d, 36, y + 30,
             "Ukraine hits the Crimea bridge again",
             font(SERIF, 44), 700, 52, max_lines=2)
    para(d, 36, y + 8,
         "Kyiv says it struck the Kerch bridge for a second straight day. "
         "Russian missiles hit two bridges in Kyiv overnight.",
         font(SANS, 24), 700, 32, max_lines=2)
    d.rounded_rectangle([780, 176, 988, 384], 12, fill=NAVY)
    icon_bridge(d, (796, 192, 972, 368), (255, 214, 90))
    d.line([(36, 420), (988, 420)], fill=RULE, width=2)

    # Four more stories in a 2x2 grid
    stories = [
        ("MIDDLE EAST", "Iran fires drones at US radar in Bahrain",
         "Tehran says its Guards hit a US radar at Sheikh Isa base; "
         "Bahrain says it intercepted the attack. Tankers hit mines "
         "near the Strait of Hormuz.",
         icon_radar, (178, 34, 34)),
        ("ASIA  ·  DIPLOMACY", "Xi, Trump and Putin to meet in Shenzhen",
         "China confirms the first three-way summit of the three leaders, "
         "on Thursday at APEC.",
         icon_summit, (20, 33, 61)),
        ("TECHNOLOGY", "Cyberattack hits 178 major websites",
         "Malicious code spread via Optimizely hit the BBC, CNN, Zoom "
         "and HSBC to steal card data.",
         icon_lock, (20, 33, 61)),
        ("MIDDLE EAST  ·  SECURITY", "Third US carrier reaches the region",
         "The USS Theodore Roosevelt arrives in the Middle East, "
         "a third US carrier group there.",
         icon_ship, (178, 34, 34)),
    ]
    gx, gy = 36, 444
    cw, ch = 466, 236
    for i, (kicker, headline, body, icon, accent) in enumerate(stories):
        x = gx + (i % 2) * (cw + 20)
        yy = gy + (i // 2) * (ch + 16)
        story_block(d, x, yy, cw, ch, kicker, headline, body, icon, accent)
        if i % 2 == 0:
            d.line([(x + cw + 10, yy + 6), (x + cw + 10, yy + ch - 6)],
                   fill=RULE, width=2)

    d.line([(36, 934), (988, 934)], fill=RULE, width=2)
    d.text((36, 950),
           "Also: EU sanctions 101 Russia-linked entities  ·  Japan scrambles "
           "jets over Russian planes",
           font=font(SANS, 19), fill=GREY)
    d.text((36, 982), "Drawn from reports published on 17 November 2026.",
           font=font(SANS, 18), fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
