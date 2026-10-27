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

# OLED hardware looks the same in every theme
OLED_FRAME, OLED_SCREEN, OLED_PX = "#17181A", "#050607", "#A6ECFF"

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

HERO = f"""
<defs>
  <pattern id="grid" width="4" height="4" patternUnits="userSpaceOnUse">
    <path d="M4 0V4H0" fill="none" stroke="{OLED_SCREEN}" stroke-width="1"/>
  </pattern>
  <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur stdDeviation="3" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>
<text x="56" y="80" class="mono" font-size="13" fill="$muted" letter-spacing="2">HELLO, I'M</text>
<text x="52" y="154" class="serif" font-size="76" fill="$ink">Ashma Rai<tspan fill="$accent">.</tspan></text>
<text x="56" y="198" class="sans" font-size="18" fill="$muted">I design and build interfaces, AI agents and small machines.</text>
<line x1="56" y1="284" x2="612" y2="284" stroke="$line"/>
<text x="56" y="312" class="mono" font-size="11" fill="$muted" letter-spacing="1.6">AI AGENTS  ·  HARDWARE  ·  INTERACTION DESIGN  ·  COMPUTER VISION</text>

<rect x="664" y="56" width="288" height="228" rx="16" fill="{OLED_FRAME}"/>
<rect x="680" y="72" width="256" height="136" rx="6" fill="{OLED_SCREEN}"/>
<g filter="url(#glow)">
  <rect x="742" y="100" width="36" height="52" rx="10" fill="{OLED_PX}"/>
  <rect x="838" y="100" width="36" height="52" rx="10" fill="{OLED_PX}"/>
  <path d="M796 174 q12 10 24 0" fill="none" stroke="{OLED_PX}" stroke-width="4" stroke-linecap="square"/>
</g>
<rect x="680" y="72" width="256" height="136" fill="url(#grid)" opacity=".85"/>
<text x="682" y="238" class="mono" font-size="11" fill="#8A8F96">bobby-pinout</text>
<text x="682" y="256" class="mono" font-size="10" fill="#5E636A">ESP32 · SSD1306 · 128×64</text>
<circle cx="926" cy="234" r="5" fill="$accent"/>
{''.join(f'<rect x="{690 + i * 18}" y="268" width="8" height="6" rx="1" fill="#C9A85A"/>' for i in range(14))}
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
