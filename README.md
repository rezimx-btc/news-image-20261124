# The World Today — Tuesday 24 November 2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/rezimx-btc/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/rezimx-btc/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A newspaper front page summing up the world's news of Tuesday 24 November 2026 in a single 1024×1024 image, for the make.fun bounty [news-image-20261124](https://make.fun/bounty/news-image-20261124).

## What it covers

The lead story is NATO sending an AWACS early-warning aircraft to Poland after three Russian Kh-101 missiles landed there on Friday. The page then covers, each with its source named on the image:

- **War in Europe** — Ukraine sank a Russian missile corvette in Benghazi, Libya, with maritime drones; a drone strike hit the cargo ship Sparta II in the Gulf of Finland.
- **Climate** — COP31 talks in Turkey collapsed without a deal, the first climate-summit failure since 2009.
- **Middle East** — an Iranian singer and four members of her production team each received 74 lashes; Iran vows to use "all its tools" against the US naval blockade; Israeli strikes killed three in Gaza and settler arson hit five West Bank villages.
- **Americas** — Trump ordered the US Army to pause detonation of a deteriorating toxic lead azide stockpile in Iowa, and said he secured a deal to reinstate Jensen Huang as Nvidia CEO; Waymo suspended its driverless taxis from all US freeways.
- **Asia** — an Indonesia candy factory fire killed at least 24; the International Court of Justice ruled Myanmar committed genocide against the Rohingya.
- **Sport** — Carlos Alcaraz won his maiden ATP Finals title; India vs New Zealand's first Test ended in a draw; D Gukesh began his World Chess Championship title defence.

Sources: Reuters, BBC, France 24, Naval News, Times of India.

## How it works

`main.py` is a self-contained Python 3.13 program using only the standard library (`os`, `struct`, `zlib`). It draws the front page with a hand-authored 5×7 bitmap font defined in the code — no font files, no images, no network — and encodes the PNG itself. The output is fully deterministic: no clock, no randomness, so repeated runs produce byte-identical files.

## How to run

```sh
python3 main.py
```

This writes `entry.png` to the current directory, or to `$MAKEFUN_OUTPUT_DIR/entry.png` when that environment variable is set.

## License

MIT — see [LICENSE](LICENSE).
