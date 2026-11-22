#!/usr/bin/env python3
"""Draw the 22 November 2026 world-news summary as a single 1024x1024 image.

Everything is drawn in code with PIL: rectangles, rules and text only.
No photos, no stock art, no AI imagery. The stories are the ones first
reported on Sunday 22 November 2026 (COP31, Kyiv, Sinaloa, Hormuz,
the Rohingya ruling, the market sell-off, NATO, BepiColombo, Cikande).

Run:  python3 generate.py        -> writes entry.png next to this file
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = "entry.png"

PAPER = (248, 245, 238)
INK = (24, 24, 28)
NAVY = (18, 38, 66)
RED = (168, 32, 26)
GOLD = (184, 134, 11)
GREY = (96, 96, 100)
CARD = (255, 255, 255)
RULE = (210, 204, 192)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w pixels."""
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


def para(draw, x, y, text, fnt, max_w, leading, color=INK):
    """Draw wrapped text, return the y just below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def kicker(draw, x, y, label, color):
    fnt = font(SANS_B, 17)
    draw.text((x, y), label.upper(), font=fnt, fill=color)
    return y + 24


def story_card(draw, box, label, color, head, body, head_size=25):
    """One news card: coloured kicker, headline, at most two body lines."""
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=10, fill=CARD, outline=RULE, width=2)
    px, py = x0 + 18, y0 + 12
    inner = x1 - x0 - 36
    py = kicker(draw, px, py, label, color)
    py = para(draw, px, py + 2, head, font(SERIF_B, head_size),
              inner, head_size + 6)
    lines = wrap(draw, body, font(SANS, 17), inner)[:2]
    for line in lines:
        draw.text((px, py + 6), line, font=font(SANS, 17), fill=GREY)
        py += 21
    return y1


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead band -------------------------------------------------
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.text((48, 22), "THE WORLD TODAY", font=font(SERIF_B, 58), fill=(255, 255, 255))
    d.text((48, 88), "SUNDAY 22 NOVEMBER 2026  ·  ONE DAY, ONE PICTURE",
           font=font(SANS_B, 19), fill=(200, 210, 225))
    d.rectangle([0, 118, W, 124], fill=GOLD)

    # ---- Lead story ----------------------------------------------------
    lx, ly, lw = 48, 140, 928
    d.rounded_rectangle([lx, ly, lx + lw, ly + 190], radius=12,
                        fill=CARD, outline=RULE, width=2)
    kicker(d, lx + 24, ly + 16, "Climate · Antalya", RED)
    y = para(d, lx + 24, ly + 46,
             "COP31 collapses with no deal",
             font(SERIF_B, 44), lw - 48, 52)
    para(d, lx + 24, y + 8,
         "After two days of overtime, talks in Antalya ended without an "
         "agreement. The European Union rejected a draft text that made no "
         "mention of fossil fuels, and no deal was adopted.",
         font(SANS, 21), lw - 48, 28, GREY)

    # ---- Grid of eight stories ----------------------------------------
    stories = [
        ("War · Kyiv", NAVY,
         "Drone hits Kyiv flats",
         "A Russian drone struck a Kyiv apartment block. Part of it "
         "collapsed; at least 14 are missing."),
        ("Crime · Sinaloa", RED,
         "\u2018El Chapo Isidro\u2019 captured",
         "Mexico arrested cartel boss Fausto Isidro Meza Flores. Eleven "
         "died in the raid."),
        ("Gulf · Hormuz", NAVY,
         "Iran strikes near Hormuz",
         "Iran hit a site in Sitra, Bahrain, and two tankers near Hormuz. "
         "Gulf states condemned it."),
        ("Justice · The Hague", RED,
         "Myanmar guilty of genocide",
         "The World Court ruled Myanmar committed genocide against the "
         "Rohingya in 2017."),
        ("Markets", GOLD,
         "Stocks slide into correction",
         "The S&P 500 fell 3.7% into correction; Nasdaq 5.3%, Nikkei 5.1%."),
        ("Security · Warsaw", NAVY,
         "NATO: defend every inch",
         "NATO chief Mark Rutte vowed to defend every inch of Poland."),
        ("Space", GOLD,
         "BepiColombo reaches Mercury",
         "After an eight-year journey, ESA confirmed the probe is in orbit "
         "around Mercury."),
        ("Indonesia · Banten", RED,
         "Candy factory fire",
         "A fire at a candy factory in Cikande, Banten, killed 3 people. "
         "Another 36 are still missing."),
    ]
    gx, gy = 48, 346
    cw, ch, gap = 452, 122, 12
    for i, (label, color, head, body) in enumerate(stories):
        cx = gx + (i % 2) * (cw + gap)
        cy = gy + (i // 2) * (ch + gap)
        story_card(d, (cx, cy, cx + cw, cy + ch), label, color, head, body,
                   head_size=24)

    # ---- In brief strip ------------------------------------------------
    by = gy + 4 * (ch + gap) + 6
    d.rounded_rectangle([48, by, 976, by + 84], radius=10,
                        fill=NAVY, outline=NAVY)
    d.text((72, by + 10), "IN BRIEF", font=font(SANS_B, 19), fill=GOLD)
    para(d, 72, by + 36,
         "Nigeria boat capsizes, 24 dead  ·  South Korea\u2019s education "
         "minister quits over AI cheating  ·  EU and Indonesia sign a "
         "landmark trade deal  ·  Kryvyi Rih toll: 2 dead, 58 hurt.",
         font(SANS, 16), 904, 20, (225, 228, 235))

    # ---- Footer --------------------------------------------------------
    d.text((48, 972), "Sources: AP · Reuters · AFP · BBC · The Guardian · Al Jazeera",
           font=font(SANS, 15), fill=GREY)

    img.save(OUT, "PNG")
    print(f"wrote {OUT}: {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
