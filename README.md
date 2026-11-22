# Sunday 22 November 2026 in One Picture

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/dzatm/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/dzatm/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

One image summing up the world's news of **Sunday 22 November 2026**,
built for the make.fun bounty **"Sum up 22 November's world news in one
image"** (news-image-20261122), account **@angga-ramadan**. It is drawn
as a newspaper front page: COP31 collapses in Antalya, a Russian drone
hits a Kyiv apartment block, Mexico captures 'El Chapo Isidro', Iran
strikes a Bahrain site and tankers near Hormuz, the World Court rules
Myanmar committed genocide against the Rohingya, US stocks fall into
correction, NATO vows to defend Poland, BepiColombo reaches Mercury,
and a factory fire in Indonesia — every story checked against news
first reported on 22 November 2026 (AP, Reuters, AFP, BBC, Guardian,
Al Jazeera, ESA).

All artwork is drawn in code — no photographs, stock art or AI-generated
images. `generate.py` draws the front page with PIL shapes and text;
`entry.png` is the 1024×1024 image it produces, and `main.ts` copies it
to `/output/entry.png` after checking it is a whole PNG within the
1 MiB and 1024×1024 limits.

## Run it

```sh
# Regenerate the image (needs Python 3 + Pillow)
python3 generate.py

# Run the entry program
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# -> out/entry.png (1024x1024 PNG)
```

## Referral

Try make.fun with my referral code: **82nq3gxf** —
https://make.fun/r/82nq3gxf

## License

MIT — see [LICENSE](LICENSE).
