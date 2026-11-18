# news-image-20261117

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/leopad12121/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/leopad12121/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

One image summing up the world's news of Tuesday 17 November 2026: Ukraine
strikes the Crimea bridge again, Iran fires drones at a US radar base in
Bahrain, Xi, Trump and Putin are set to meet in Shenzhen, a cyberattack hits
178 major websites, and a third US carrier reaches the Middle East.

`draw_news.py` draws the front page (`entry.png`, 1024×1024) from the day's
reported stories; `main.py` is the entrypoint the grader runs — it copies
`entry.png` to the output directory. Standard library only, no network,
deterministic.

## Run it

```sh
python3 draw_news.py        # regenerate entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/bounty/news-image-20261117)</sub>
