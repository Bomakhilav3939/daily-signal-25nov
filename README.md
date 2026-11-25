# The World in One Day — Tuesday, November 24, 2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Bomakhilav3939/daily-signal-25nov/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Bomakhilav3939/daily-signal-25nov/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

> [!NOTE]
> **make.fun entry** — [news-image-20261124](https://make.fun/bounty/news-image-20261124)
> "Sum up the world news of 24 November 2026 in one image."

## The entry

`entry.png` is a 1024x1024 one-page digest of world news for **Tuesday,
November 24, 2026**: 34 dated stories across 7 regions, 13 of them drawn
as original flat-vector illustrations — no photographs, everything
deterministically rendered by `render_entry.py` from `news25.json` with
the bundled fonts.

- **Masthead** — the day's date, deck, and per-region story counts
- **The day in UTC** — five dated moments, from the 07:17 Nepal quake to
  the Asian market close
- **The day in numbers** — 96 drones, 3 tankers ablaze, +9.0% Taiex,
  Kospi at 5,000, 1,283 EU-pact migrants, M5.6
- **Three leads** — Hormuz tanker mines, the Asian market roar-back,
  Russia's 96-drone night on Ukraine — each with a drawn scene
- **Stories 4–13** — ten carded briefs, each with place, status tag,
  source, and a small drawing: Korean air-raid alert, Pakistan's first
  astronaut, Australia's digital duty-of-care deal, the Bogotá car bomb,
  the Gaza police-post strike, Singapore's no-chip-backdoor vow, the
  Nepal quake, the EU migrant pact, Johannesburg's flood alert, and
  Monday Night Football
- **Twenty-one more, by region** — the rest of the day's wire in two
  columns
- **Where it happened** — a dot-matrix world map with a numbered pin on
  each drawn story
- **Date check** — every story is dated to Tuesday 24 November 2026, or
  explicitly marked as another day's event first reported that day

Status tags are defined in the legend: CONFIRMED (two or more
independent outlets), OFFICIAL (an on-the-record statement), REPORTED
(outlets report it), CLAIM (one side's account), ONGOING (still
unfolding). Every story names its source or runs to wire.

## Build

`main.py` is the graded entrypoint: standard library only, it moves the
shipped `entry.png` into `/output`. The image itself is produced by

```
python3 render_entry.py   # writes entry.png, 1024x1024, deterministic
```

Run it twice and the bytes are identical. Sources: open reporting from
AP, Reuters, Anadolu, Al Jazeera, POLITICO, The Hindu, USGS and CNSA.
