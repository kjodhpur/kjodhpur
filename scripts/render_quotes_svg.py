#!/usr/bin/env python3
"""
Terminal-window inspirational quotes SVG (AVI-style chrome).

Bakes a shuffled subset of quotes with SMIL fade rotation so the panel
cycles while viewed. Re-run on each Action / push to reshuffle — combined
with a no-cache dynamic fallback in the README for true per-refresh variety.

    python scripts/render_quotes_svg.py [quotes.json] [output.svg]
"""
import html
import json
import os
import random
import sys
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "data", "quotes.json")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "quotes.svg")

BG, BG2, FRAME, MUTED, INK, GREEN, ACCENT = (
    "#0d1117", "#111722", "#30363d", "#7d8590", "#e6edf3", "#39d353", "#58a6ff"
)
W, H = 860, 220
PAD, TITLEBAR_H = 24, 30
HOLD, FADE = 5.0, 0.7  # seconds per quote, crossfade
N_SHOW = 8

quotes = json.load(open(SRC))
random.shuffle(quotes)
quotes = quotes[:N_SHOW]
cycle = len(quotes) * (HOLD + FADE)

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#bg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]
for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{c}"/>')
parts.append(
    f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" text-anchor="middle">'
    f'kanha@github: ~$ fortune</text>'
)

# prompt line
parts.append(
    f'<text x="{PAD}" y="{TITLEBAR_H + 36}" fill="{MUTED}" font-size="14">'
    f'$ echo <tspan fill="{GREEN}">$QUOTE</tspan></text>'
)

# rotating quote blocks
body_y = TITLEBAR_H + 78
for i, q in enumerate(quotes):
    wrapped = textwrap.wrap(q["text"], width=72) or [""]
    author = q.get("author") or "Unknown"
    delay = i * (HOLD + FADE)
    # opacity keyframes: fade in, hold, fade out, stay hidden for rest of cycle
    # Using SMIL set/animate for GitHub <img> compatibility
    g_id = f"q{i}"
    parts.append(f'<g id="{g_id}" opacity="0">')
    parts.append(
        f'<animate attributeName="opacity" values="0;1;1;0;0" '
        f'keyTimes="0;{FADE/cycle:.4f};{(FADE+HOLD)/cycle:.4f};{(2*FADE+HOLD)/cycle:.4f};1" '
        f'dur="{cycle:.2f}s" begin="{delay:.2f}s" repeatCount="indefinite"/>'
    )
    for li, line in enumerate(wrapped[:3]):
        parts.append(
            f'<text x="{PAD}" y="{body_y + li*28}" fill="{INK}" font-size="18" font-weight="600">'
            f'{html.escape(line)}</text>'
        )
    parts.append(
        f'<text x="{PAD}" y="{body_y + len(wrapped[:3])*28 + 18}" fill="{ACCENT}" font-size="14">'
        f'— {html.escape(author)}</text>'
    )
    parts.append("</g>")

parts.append(
    f'<text x="{PAD}" y="{H - 18}" fill="{MUTED}" font-size="11">'
    f'// rotates on view · reshuffled when profile art refreshes</text>'
)
parts.append("</svg>")
open(OUT, "w").write("".join(parts))
print(f"wrote {OUT}: {len(quotes)} quotes, cycle {cycle:.1f}s")
