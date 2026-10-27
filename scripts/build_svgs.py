#!/usr/bin/env python3
"""Generate the SVGs used by the profile README.

Run from the repo root:  python3 scripts/build_svgs.py
Every asset is written into assets/ twice, as <name>-light.svg and <name>-dark.svg,
so the README can swap them with <picture> to match the viewer's GitHub theme.
Edit copy or colours here, never in the generated files.
"""
from pathlib import Path
from string import Template

OUT = Path(__file__).resolve().parent.parent / "assets"

THEMES = {
    "light": dict(bg="#F5F2EB", surface="#EBE6DA", surface2="#E0D9CA", ink="#1B1A17",
                  muted="#6E685D", line="#D9D1C1", accent="#D9472B", good="#2E7D5B", bad="#C23A22"),
    "dark": dict(bg="#121211", surface="#1D1C1A", surface2="#272522", ink="#EFEBE2",
                 muted="#9C968A", line="#33302B", accent="#FF6B47", good="#5CC79A", bad="#FF6B47"),
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
.c{transform-box:fill-box;transform-origin:center}
"""


def svg(w, h, css, body, framed=True):
    frame = (f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="18" fill="$bg" stroke="$line"/>'
             if framed else "")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">'
            f"<style>{BASE_CSS}{css}</style>{frame}{body}</svg>")


# ---------------------------------------------------------------- hero

HERO_CSS = """
.blink{animation:blinkon 1s steps(1) infinite}
@keyframes blinkon{50%{opacity:0}}
.eye{animation:eye 5s infinite}
@keyframes eye{0%,90%,100%{transform:scaleY(1)}94%{transform:scaleY(.1)}}
.look{animation:look 10s ease-in-out infinite}
@keyframes look{0%,35%{transform:translateX(0)}40%,55%{transform:translateX(-12px)}60%,78%{transform:translateX(12px)}83%,100%{transform:translateX(0)}}
"""

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
<text x="56" y="104" class="mono" font-size="13" fill="$muted" letter-spacing="2">HELLO, I'M</text>
<text x="52" y="178" class="serif" font-size="76" fill="$ink">Ashma Rai<tspan fill="$accent">.</tspan></text>
<text x="56" y="222" class="sans" font-size="18" fill="$muted">I design and build interfaces, AI agents and small machines.</text>
<line x1="56" y1="252" x2="612" y2="252" stroke="$line"/>
<text x="56" y="280" class="mono" font-size="11" fill="$muted" letter-spacing="1.6">AI AGENTS  ·  HARDWARE  ·  INTERACTION DESIGN  ·  COMPUTER VISION</text>

<rect x="664" y="56" width="288" height="228" rx="16" fill="{OLED_FRAME}"/>
<rect x="680" y="72" width="256" height="136" rx="6" fill="{OLED_SCREEN}"/>
<g filter="url(#glow)">
  <g class="look c">
    <rect class="eye c" x="742" y="100" width="36" height="52" rx="10" fill="{OLED_PX}"/>
    <rect class="eye c" x="838" y="100" width="36" height="52" rx="10" fill="{OLED_PX}"/>
  </g>
  <path d="M796 174 q12 10 24 0" fill="none" stroke="{OLED_PX}" stroke-width="4" stroke-linecap="square"/>
</g>
<rect x="680" y="72" width="256" height="136" fill="url(#grid)" opacity=".85"/>
<text x="682" y="238" class="mono" font-size="11" fill="#8A8F96">bobby-pinout</text>
<text x="682" y="256" class="mono" font-size="10" fill="#5E636A">ESP32 · SSD1306 · 128×64</text>
<circle class="blink" cx="926" cy="234" r="5" fill="$accent"/>
{''.join(f'<rect x="{690 + i * 18}" y="268" width="8" height="6" rx="1" fill="#C9A85A"/>' for i in range(14))}
"""

# ---------------------------------------------------------------- build

ASSETS = {
    "hero": svg(1000, 340, HERO_CSS, HERO),
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
