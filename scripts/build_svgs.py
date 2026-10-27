#!/usr/bin/env python3
"""Generate the SVGs used by the profile README.

Run from the repo root:  python3 scripts/build_svgs.py
Every asset is written into assets/ as <name>-<theme>.svg.
Edit copy or colours here, never in the generated files.
"""
from pathlib import Path
from string import Template

OUT = Path(__file__).resolve().parent.parent / "assets"

THEMES = {
    "light": dict(bg="#F5F2EB", surface="#EBE6DA", surface2="#E0D9CA", ink="#1B1A17",
                  muted="#6E685D", line="#D9D1C1", accent="#D9472B", good="#2E7D5B", bad="#C23A22"),
}
FONTS = dict(
    serif="'Iowan Old Style','Charter','Georgia',serif",
    sans="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif",
    mono="'SF Mono','JetBrains Mono',Menlo,Consolas,monospace",
)

BASE_CSS = """
.serif{font-family:$serif}.sans{font-family:$sans}.mono{font-family:$mono}
"""


def svg(w, h, css, body, framed=True):
    frame = (f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="18" fill="$bg" stroke="$line"/>'
             if framed else "")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">'
            f"<style>{BASE_CSS}{css}</style>{frame}{body}</svg>")


# ---------------------------------------------------------------- hero

HERO = """
<text x="56" y="80" class="mono" font-size="13" fill="$muted" letter-spacing="2">HELLO, I'M</text>
<text x="52" y="154" class="serif" font-size="76" fill="$ink">Ashma Rai<tspan fill="$accent">.</tspan></text>
<text x="56" y="198" class="sans" font-size="18" fill="$muted">I design and build interfaces, AI agents and small machines.</text>
<line x1="56" y1="284" x2="612" y2="284" stroke="$line"/>
<text x="56" y="312" class="mono" font-size="11" fill="$muted" letter-spacing="1.6">AI AGENTS  ·  HARDWARE  ·  INTERACTION DESIGN  ·  COMPUTER VISION</text>
"""

# ---------------------------------------------------------------- build

ASSETS = {
    "hero": svg(1000, 340, "", HERO),
}


def main():
    OUT.mkdir(exist_ok=True)
    for name, tmpl in ASSETS.items():
        for theme, colours in THEMES.items():
            out = Template(tmpl).substitute(colours, **FONTS)
            (OUT / f"{name}-{theme}.svg").write_text(out, encoding="utf-8")
    print(f"wrote {len(ASSETS) * len(THEMES)} files to {OUT}")


if __name__ == "__main__":
    main()
