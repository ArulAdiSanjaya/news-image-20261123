# The World in One Page — Monday 23 November 2026

[![make.fun](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/ArulAdiSanjaya/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/ArulAdiSanjaya/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123)

Entry for the [make.fun bounty **news-image-20261123**](https://make.fun/bounty/news-image-20261123):
sum up the world's news of Monday 23 November 2026 in one image.

## The image

A newspaper front page — **"The World in One Page"** — drawn with Python
(Pillow) in `render.py` and shipped as `entry.png` (1024×1024, under 1 MiB).

- **Lead story — Huang is back.** Nvidia's board reinstated Jensen Huang as
  chief executive, 11 days after he resigned; shares jumped 31% and the
  Nasdaq rose 6.5% in one of Wall Street's most extraordinary days.
- **Ukraine sinks Russian warship off Libya.** Seven Ukrainian sea drones sank
  the corvette *Merkury* at Benghazi port; a Russian arms ship was hit too.
- **Democrats win 258 House seats.** The largest US House majority since 1992.
- **CrowdStrike buys Zscaler for $43.9bn.** The largest cybersecurity
  takeover on record.
- **US seeks $1bn in stolen Binance crypto.** The Justice Department moved to
  recover coins North Korean hackers stole from the exchange.
- **Also on Monday:** Tajikistan starts quitting the ICC, Puigdemont is free
  to return to Spain, bomb threats hit about 450 German schools, and 3 people
  died with 34 missing after a candy factory fire in Indonesia.

Every fact is as reported on 23 November 2026 by Reuters, AP, BBC, WSJ and
TechCrunch — no invented headlines, no speculation shown as fact. The image
names the day it sums up in the masthead and the footer.

## How it runs

`main.ts` (Node 22, standard library only) copies the bundled `entry.png`
byte-for-byte to the output directory, so two runs produce identical bytes:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`render.py` regenerates `entry.png` from scratch (Pillow, system DejaVu
fonts, no network) — it is the build script, not part of the run path.

## License

MIT — see [LICENSE](LICENSE).
