#!/usr/bin/env python3
"""make.fun news-image-20261124 entrypoint.

The digest image for Tuesday 24 November 2026 is rendered once by
render_entry.py from news25.json (deterministic, offline, bundled fonts)
and shipped here as entry.png. This entrypoint moves that image into the
output directory using the standard library only, as the competition
sandbox requires.
"""
import os
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(BASE, "entry.png")
    out_dir = "/output"
    if not os.path.isdir(out_dir):
        try:
            os.makedirs(out_dir)
        except OSError:
            out_dir = BASE
    dst = os.path.join(out_dir, "entry.png")
    if os.path.abspath(src) != os.path.abspath(dst):
        shutil.copyfile(src, dst)
    print(dst)


if __name__ == "__main__":
    main()
