#!/usr/bin/env python3
"""Draw the 22 November 2026 world-news front page (1024x1024 PNG).

Every story below was checked against news first reported on Sunday
22 November 2026 (AP, Reuters, AFP, BBC, Guardian, Al Jazeera, One Turn,
phys.org / ESA). All artwork is drawn here in code with PIL shapes --
no photos, no stock art, no AI-generated images.
Run: python3 generate.py  ->  entry.png
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
INK = (18, 18, 18)
RED = (178, 24, 24)
BLUE = (16, 62, 120)
GREEN = (18, 110, 60)
GREY = (90, 90, 90)
LIGHT = (242, 240, 235)
PAPER = (252, 250, 244)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    out = []
    for para in text.split("\n"):
        out.extend(textwrap.wrap(para, width=width, break_long_words=False) or [""])
    return out


def text_block(draw, x, y, text, fnt, color, max_w, leading=None):
    """Draw wrapped text; returns y after the last line."""
    avg = fnt.getlength("x")
    lines = wrap(draw, text, fnt, max(8, int(max_w / max(avg, 1))))
    lh = leading or int(fnt.size * 1.25)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=color)
        y += lh
    return y


def icon(draw, kind, x, y, s, color):
    """Simple pictogram drawn from shapes, inside a square of side s."""
    if kind == "globe":
        draw.ellipse([x, y, x + s, y + s], outline=color, width=4)
        draw.ellipse([x + s * .32, y, x + s * .68, y + s], outline=color, width=3)
        draw.line([(x, y + s * .5), (x + s, y + s * .5)], fill=color, width=3)
        draw.arc([x, y + s * .2, x + s, y + s * .8], 200, 340, fill=color, width=3)
    elif kind == "crack":
        # globe with a crack: climate talks collapsing
        draw.ellipse([x, y, x + s, y + s], outline=color, width=4)
        draw.line([(x + s * .5, y + s * .05), (x + s * .4, y + s * .35),
                   (x + s * .6, y + s * .55), (x + s * .45, y + s * .95)],
                  fill=color, width=4)
    elif kind == "building":
        draw.rectangle([x + s * .1, y + s * .2, x + s * .9, y + s], outline=color, width=4)
        draw.line([(x + s * .1, y + s * .2), (x + s * .5, y), (x + s * .9, y + s * .2)],
                  fill=color, width=4)
        for r in range(2):
            for c in range(3):
                draw.rectangle([x + s * (.22 + c * .22), y + s * (.35 + r * .25),
                                x + s * (.34 + c * .22), y + s * (.47 + r * .25)],
                               fill=color)
    elif kind == "cuffs":
        draw.ellipse([x, y + s * .25, x + s * .38, y + s * .63], outline=color, width=5)
        draw.ellipse([x + s * .62, y + s * .25, x + s, y + s * .63], outline=color, width=5)
        draw.line([(x + s * .38, y + s * .44), (x + s * .62, y + s * .44)],
                  fill=color, width=5)
    elif kind == "flame":
        draw.polygon([(x + s * .5, y), (x + s * .85, y + s * .5), (x + s * .65, y + s * .75),
                      (x + s * .85, y + s), (x + s * .15, y + s), (x + s * .35, y + s * .75),
                      (x + s * .15, y + s * .5)], fill=color)
    elif kind == "scales":
        draw.line([(x + s * .5, y + s * .1), (x + s * .5, y + s * .9)], fill=color, width=4)
        draw.line([(x + s * .15, y + s * .25), (x + s * .85, y + s * .25)], fill=color, width=4)
        draw.polygon([(x + s * .05, y + s * .55), (x + s * .25, y + s * .55),
                      (x + s * .15, y + s * .35)], outline=color, width=3)
        draw.polygon([(x + s * .75, y + s * .55), (x + s * .95, y + s * .55),
                      (x + s * .85, y + s * .35)], outline=color, width=3)
        draw.line([(x, y + s * .95), (x + s, y + s * .95)], fill=color, width=4)
    elif kind == "chart":
        draw.line([(x, y + s * .8), (x + s * .3, y + s * .55), (x + s * .55, y + s * .68),
                   (x + s, y + s * .15)], fill=color, width=5)
        draw.polygon([(x + s * .8, y + s * .1), (x + s, y + s * .15), (x + s * .82, y + s * .32)],
                     fill=color)
        draw.line([(x, y + s), (x + s, y + s)], fill=color, width=3)
    elif kind == "shield":
        draw.polygon([(x + s * .5, y), (x + s * .95, y + s * .2), (x + s * .95, y + s * .55),
                      (x + s * .5, y + s), (x + s * .05, y + s * .55), (x + s * .05, y + s * .2)],
                     outline=color, width=4)
        draw.line([(x + s * .3, y + s * .5), (x + s * .45, y + s * .65),
                   (x + s * .75, y + s * .3)], fill=color, width=4)
    elif kind == "rocket":
        draw.polygon([(x + s * .5, y), (x + s * .78, y + s * .5),
                      (x + s * .22, y + s * .5)], fill=color)
        draw.rectangle([x + s * .4, y + s * .5, x + s * .6, y + s * .85], fill=color)
        draw.polygon([(x + s * .5, y + s * .85), (x + s * .65, y + s),
                      (x + s * .35, y + s)], fill=color)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([10, 10, W - 10, H - 10], outline=INK, width=4)

    # ---- masthead ----
    d.text((512, 28), "THE WORLD IN ONE PICTURE", font=font(SERIF, 54),
           fill=INK, anchor="ma")
    d.line([(40, 108), (984, 108)], fill=RED, width=5)
    d.text((512, 118), "SUNDAY 22 NOVEMBER 2026", font=font(SANS_B, 34),
           fill=RED, anchor="ma")
    d.text((512, 158), "The day's most consequential stories, from every region and every field",
           font=font(SERIF_R, 21), fill=GREY, anchor="ma")
    d.line([(40, 192), (984, 192)], fill=INK, width=2)

    # ---- lead story: COP31 collapses ----
    d.text((40, 206), "LEAD  •  CLIMATE", font=font(SANS_B, 20), fill=RED)
    d.text((40, 232), "COP31 talks collapse in Antalya",
           font=font(SERIF, 40), fill=INK)
    d.text((40, 278), "No deal adopted after the EU rejects a draft with no mention",
           font=font(SANS, 22), fill=INK)
    d.text((40, 304), "of fossil fuels — the summit ends with nothing at all.",
           font=font(SANS, 22), fill=INK)
    d.text((40, 334), "Climate talks run two days into overtime, then break down with no deal at all.",
           font=font(SANS_B, 21), fill=BLUE)
    icon(d, "crack", 905, 225, 70, RED)
    d.line([(40, 368), (984, 368)], fill=INK, width=2)

    # ---- story grid: 2 columns x 4 rows ----
    cards = [
        ("WAR  •  UKRAINE", "building", RED, "Russian drone hits Kyiv flats; 14 missing",
         "Part of a five-storey block collapses near Kyiv; two killed, four wounded."),
        ("JUSTICE  •  MEXICO", "cuffs", BLUE, "Cartel boss 'El Chapo Isidro' captured",
         "Special forces seize Fausto Isidro Meza Flores in Sinaloa; 11 killed in the raid."),
        ("MIDDLE EAST", "flame", RED, "Iran strikes Bahrain site; tankers hit",
         "Two hurt in Sitra as Gulf states condemn Iran; two tankers struck near Hormuz."),
        ("JUSTICE  •  THE HAGUE", "scales", BLUE, "Court: Myanmar committed genocide",
         "World Court rules Myanmar committed genocide against the Rohingya in 2017."),
        ("MARKETS  •  USA", "chart", RED, "S&P 500 falls 3.7% into correction",
         "AI sell-off spreads worldwide; Nasdaq down 5.3% and Nikkei down 5.1%."),
        ("SECURITY  •  EUROPE", "shield", BLUE, "NATO: 'every inch' of Poland defended",
         "Rutte vows defence after Russian missiles land in Poland; council meets Monday."),
        ("SPACE  •  MERCURY", "rocket", GREEN, "BepiColombo reaches Mercury's orbit",
         "ESA confirms capture after an eight-year journey; science starts in April 2027."),
        ("DISASTER  •  INDONESIA", "globe", BLUE, "Candy factory fire: 3 dead, 36 missing",
         "Blaze at a factory in Cikande, Banten, leaves dozens unaccounted for."),
    ]
    x0, y0 = 40, 384
    cw, ch = 462, 118
    gx, gy = 20, 8
    for i, (tag, kind, col, head, body) in enumerate(cards):
        x = x0 + (i % 2) * (cw + gx)
        y = y0 + (i // 2) * (ch + gy)
        d.rectangle([x, y, x + cw, y + ch], outline=INK, width=2)
        d.rectangle([x, y, x + cw, y + 28], fill=LIGHT)
        d.text((x + 10, y + 4), tag, font=font(SANS_B, 16), fill=col)
        icon(d, kind, x + cw - 56, y + 34, 44, col)
        text_block(d, x + 10, y + 32, head, font(SANS_B, 20), INK, cw - 76, leading=22)
        text_block(d, x + 10, y + 80, body, font(SANS, 16), INK, cw - 20, leading=19)

    # ---- in brief + sources ----
    y3 = y0 + 4 * (ch + gy) + 6
    d.line([(40, y3), (984, y3)], fill=INK, width=2)
    d.text((40, y3 + 8), "IN BRIEF", font=font(SANS_B, 18), fill=RED)
    brief = ("Boat capsizes in Nigeria, 24 dead  •  South Korea's education minister quits "
             "over AI cheating  •  EU and Indonesia sign landmark trade deal  •  "
             "Kryvyi Rih toll: 2 dead, 58 hurt")
    text_block(d, 40, y3 + 32, brief, font(SANS, 18), INK, 944, leading=22)
    d.text((512, H - 42), "Sources: AP, Reuters, AFP, BBC, Guardian, Al Jazeera, ESA — reported 22 November 2026",
           font=font(SANS, 15), fill=GREY, anchor="ma")

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
