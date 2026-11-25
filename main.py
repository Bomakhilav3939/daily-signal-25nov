#!/usr/bin/env python3
"""Entry program for the make.fun news-image-20261124 bounty.

Copies the committed, agent-rendered front page (entry.png) into the
output directory. The image is produced once by render_entry.py from
news25.json with the bundled fonts (deterministic, offline: two runs
give byte-identical output). This entrypoint is stdlib only, no network.
"""
import os
import shutil

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    shutil.copyfile(SRC, os.path.join(OUT, "entry.png"))


if __name__ == "__main__":
    main()
