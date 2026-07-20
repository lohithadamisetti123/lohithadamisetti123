"""
gen_terminal.py
===============
Generates TWO SVG files, side-by-side in the README:

  terminal-card.svg  (840 × 875)
    • GitHub avatar converted to ASCII art
    • Each row sweeps left→right with white cursor block
    • macOS chrome:  lohithadamisetti123@github: ~$ ./portrait.sh
    • Footer:  lohithadamisetti123@github:~$ whoami  Lohitha Damisetti

  info-card.svg  (480 × 420)
    • neofetch-style info card, matching Avi's reference exactly
    • Staggered slide-up + fade-in per row
    • macOS chrome:  lohithadamisetti123@github: ~$ neofetch
    • Sections: identity header, About, Stack, Highlights

Run:
    pip install Pillow
    python gen_terminal.py
"""

import sys, os, html as _html
from urllib.request import urlopen, Request
from io import BytesIO

# ─── CONFIG ──────────────────────────────────────────────────────────────────
USERNAME     = "lohithadamisetti123"
DISPLAY_NAME = "Lohitha Damisetti"
ROLE         = "Full Stack Developer · AI Enthusiast"

# ─── HELPERS ─────────────────────────────────────────────────────────────────
def xe(s): return _html.escape(str(s), quote=True)

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ═══════════════════════════════════════════════════════════════════════════════
# PART 1 — terminal-card.svg  (ASCII art portrait)
# ═══════════════════════════════════════════════════════════════════════════════

print("[..] Fetching GitHub avatar …")
try:
    req = Request(
        f"https://avatars.githubusercontent.com/{USERNAME}?size=400",
        headers={"User-Agent": "Mozilla/5.0"},
    )
    img_bytes = urlopen(req, timeout=20).read()
    print(f"[OK] Avatar fetched  ({len(img_bytes):,} bytes)")
except Exception as e:
    sys.exit(f"[ERR] Fetch failed: {e}")

try:
    from PIL import Image
except ImportError:
    sys.exit("[ERR] Pillow not installed.  Run: pip install Pillow")

# Density ramp: space = bright pixel, @ = dark pixel
ASCII_CHARS = "  `.-':=+*csS%#@"
ART_W, ART_H = 100, 53

img = Image.open(BytesIO(img_bytes)).convert("L")
img = img.resize((ART_W, ART_H), Image.LANCZOS)
pixels = list(img.getdata())

rows = []
for r in range(ART_H):
    row = ""
    for c in range(ART_W):
        px  = pixels[r * ART_W + c]
        idx = int((255 - px) / 255 * (len(ASCII_CHARS) - 1))
        row += ASCII_CHARS[idx]
    rows.append(row)

print(f"[OK] ASCII art generated ({ART_W}×{ART_H})")

# Layout constants — identical to reference avi-ascii.svg
W1      = 840
ROW_H   = 15
ROW_Y0  = 37
FONT_SZ = 12.9
ROW_DUR = 0.11
TEXT_W  = 800
TEXT_X  = 20

FOOTER_LINE_Y = ROW_Y0 + ART_H * ROW_H   # 832
FOOTER_TEXT_Y = FOOTER_LINE_Y + 19        # 851
H1            = FOOTER_LINE_Y + 43        # 875

WHOAMI_TEXT = f"{USERNAME}@github:~$ whoami "
CURSOR_X    = TEXT_X + len(WHOAMI_TEXT) * 7.73

# Build rows SVG
rows_svg = ""
for i, row in enumerate(rows):
    begin  = i * ROW_DUR
    y_top  = ROW_Y0 + i * ROW_H
    y_text = y_top + 11.1
    safe   = xe(row)

    rows_svg += (
        f'<clipPath id="r{i}">'
        f'<rect x="{TEXT_X}" y="{y_top:.1f}" height="{ROW_H}" width="0">'
        f'<animate attributeName="width" from="0" to="{TEXT_W}" '
        f'begin="{begin:.3f}s" dur="{ROW_DUR}s" fill="freeze"/>'
        f'</rect></clipPath>\n'
        f'<g clip-path="url(#r{i})">'
        f'<text xml:space="preserve" x="{TEXT_X}" y="{y_text:.1f}" '
        f'fill="#c9d1d9" font-size="{FONT_SZ}" '
        f'textLength="{TEXT_W}" lengthAdjust="spacing">{safe}</text>'
        f'</g>\n'
        f'<rect y="{y_top+1:.1f}" width="8" height="13" fill="#c9d1d9" opacity="0">'
        f'<animate attributeName="x" from="{TEXT_X}" to="{TEXT_X+TEXT_W}" '
        f'begin="{begin:.3f}s" dur="{ROW_DUR}s" fill="freeze"/>'
        f'<set attributeName="opacity" to="0.85" begin="{begin:.3f}s"/>'
        f'<set attributeName="opacity" to="0" begin="{begin+ROW_DUR:.3f}s"/>'
        f'</rect>\n'
    )

svg1 = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W1}" height="{H1}" viewBox="0 0 {W1} {H1}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#111722"/>
    <stop offset="1" stop-color="#0d1117"/>
  </linearGradient>
</defs>
<rect width="{W1}" height="{H1}" rx="12" fill="url(#bg)"/>
<rect x="0.5" y="0.5" width="{W1-1}" height="{H1-1}" rx="12" fill="none" stroke="#30363d" stroke-width="1"/>
<line x1="0" y1="30" x2="{W1}" y2="30" stroke="#30363d"/>
<circle cx="20" cy="15.0" r="5" fill="#ff5f56"/>
<circle cx="36" cy="15.0" r="5" fill="#ffbd2e"/>
<circle cx="52" cy="15.0" r="5" fill="#27c93f"/>
<text x="{W1/2:.1f}" y="19.0" fill="#7d8590" font-size="12" text-anchor="middle">{USERNAME}@github: ~$ ./portrait.sh</text>
{rows_svg}
<line x1="0" y1="{FOOTER_LINE_Y:.1f}" x2="{W1}" y2="{FOOTER_LINE_Y:.1f}" stroke="#30363d"/>
<text x="20" y="{FOOTER_TEXT_Y:.1f}" fill="#7d8590" font-size="13">{USERNAME}@github:~$ whoami <tspan fill="#c9d1d9">{DISPLAY_NAME}</tspan></text>
<rect x="{CURSOR_X:.0f}" y="{FOOTER_TEXT_Y-13:.1f}" width="8" height="14" fill="#c9d1d9">
  <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" dur="1s" repeatCount="indefinite"/>
</rect>
</svg>"""

out1 = os.path.join(OUT_DIR, "terminal-card.svg")
with open(out1, "w", encoding="utf-8") as f:
    f.write(svg1)
print(f"[OK] terminal-card.svg written  ({W1}×{H1}px, {os.path.getsize(out1)//1024} KB)")


# ═══════════════════════════════════════════════════════════════════════════════
# PART 2 — info-card.svg  (neofetch-style, matching Avi's info-card.svg)
# ═══════════════════════════════════════════════════════════════════════════════

W2, H2 = 480, 420

# Info rows: (label_color, label, value)
# Colors matching reference exactly
C_ORANGE = "#ffa657"
C_BLUE   = "#58a6ff"
C_GREEN  = "#3fb950"
C_CYAN   = "#22d3ee"
C_WHITE  = "#c9d1d9"
C_DIM    = "#30363d"
C_GRAY   = "#7d8590"

# Build rows: each is a dict describing what to render
# type: "header" | "section" | "field" | "bullet"
INFO_ROWS = [
    # identity header
    {"type": "header"},
    # About section
    {"type": "section",  "label": "— About"},
    {"type": "field",    "label": "Role",     "value": "Full Stack Developer"},
    {"type": "field",    "label": "Focus",    "value": "AI-powered web applications"},
    {"type": "field",    "label": "College",  "value": "B.Tech, Pragati Engg. College"},
    {"type": "field",    "label": "LeetCode", "value": "400+ problems solved"},
    # Stack section
    {"type": "section",  "label": "— Stack"},
    {"type": "field",    "label": "Frontend", "value": "React, Next.js, TypeScript"},
    {"type": "field",    "label": "Backend",  "value": "Node.js, Python, FastAPI"},
    {"type": "field",    "label": "Database", "value": "PostgreSQL, MongoDB, Redis"},
    {"type": "field",    "label": "Cloud",    "value": "AWS, Docker, GitHub Actions"},
    # Highlights section
    {"type": "section",  "label": "— Highlights"},
    {"type": "bullet",   "value": "120 public repositories"},
    {"type": "bullet",   "value": "450+ GitHub stars earned"},
    {"type": "bullet",   "value": "Open source contributor"},
]

# Animation timing (matches reference: each row starts 0.06s after previous)
SLIDE_DUR  = 0.4    # s — duration of each row's animation
STEP       = 0.06   # s — stagger between rows

# Y positions
TOP_Y    = 60.0    # first row (identity header) text y
LINE_H   = 20.5   # between rows

parts = []
cur_t = 0.15
cur_y = TOP_Y

for row in INFO_ROWS:
    t     = cur_t
    ks    = "0.2 0.8 0.2 1"    # easing

    if row["type"] == "header":
        # "lohithadamisetti123@github" bold header + horizontal rule
        ulen = len(USERNAME)
        rule_x1 = 20 + (ulen + 1 + 6) * 8.2   # rough char width
        parts.append(
            f'<g opacity="0" transform="translate(0,5)">'
            f'<text x="20" y="{cur_y}" font-size="14" font-weight="700">'
            f'<tspan fill="{C_GREEN}">{xe(USERNAME)}</tspan>'
            f'<tspan fill="{C_GRAY}">@</tspan>'
            f'<tspan fill="{C_CYAN}">github</tspan>'
            f'</text>'
            f'<line x1="{rule_x1:.0f}" y1="{cur_y-4:.1f}" x2="460" y2="{cur_y-4:.1f}" stroke="{C_DIM}" stroke-opacity="0.8"/>'
            f'<animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur="{SLIDE_DUR}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" begin="{t:.2f}s" dur="{SLIDE_DUR}s" fill="freeze" calcMode="spline" keySplines="{ks}"/>'
            f'</g>'
        )
        cur_y += LINE_H * 1.1
        cur_t += STEP

    elif row["type"] == "section":
        # blue section header + horizontal rule
        label   = row["label"]
        rule_x1 = 20 + len(label) * 7.5
        parts.append(
            f'<g opacity="0" transform="translate(0,5)">'
            f'<text x="20" y="{cur_y}" fill="{C_BLUE}" font-size="12.5" font-weight="700">{xe(label)}</text>'
            f'<line x1="{rule_x1:.0f}" y1="{cur_y-4:.1f}" x2="460" y2="{cur_y-4:.1f}" stroke="{C_DIM}" stroke-opacity="0.8"/>'
            f'<animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur="{SLIDE_DUR}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" begin="{t:.2f}s" dur="{SLIDE_DUR}s" fill="freeze" calcMode="spline" keySplines="{ks}"/>'
            f'</g>'
        )
        cur_y += LINE_H * 1.5
        cur_t += STEP * 2

    elif row["type"] == "field":
        # orange label + white value, label column at x=20, value at x=112
        parts.append(
            f'<g opacity="0" transform="translate(0,5)">'
            f'<text x="20" y="{cur_y}" fill="{C_ORANGE}" font-size="12.5" font-weight="700">{xe(row["label"])}</text>'
            f'<text x="112" y="{cur_y}" fill="{C_WHITE}" font-size="12.5">{xe(row["value"])}</text>'
            f'<animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur="{SLIDE_DUR}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" begin="{t:.2f}s" dur="{SLIDE_DUR}s" fill="freeze" calcMode="spline" keySplines="{ks}"/>'
            f'</g>'
        )
        cur_y += LINE_H
        cur_t += STEP

    elif row["type"] == "bullet":
        # green dot + white text
        dot_cy = cur_y - 4
        parts.append(
            f'<g opacity="0" transform="translate(0,5)">'
            f'<circle cx="23" cy="{dot_cy:.1f}" r="2.5" fill="{C_GREEN}"/>'
            f'<text x="34" y="{cur_y}" fill="{C_WHITE}" font-size="12.5">{xe(row["value"])}</text>'
            f'<animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur="{SLIDE_DUR}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" begin="{t:.2f}s" dur="{SLIDE_DUR}s" fill="freeze" calcMode="spline" keySplines="{ks}"/>'
            f'</g>'
        )
        cur_y += LINE_H
        cur_t += STEP

# Adjust H2 to fit content
H2 = max(420, int(cur_y) + 30)

info_parts_svg = "\n".join(parts)

svg2 = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W2}" height="{H2}" viewBox="0 0 {W2} {H2}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">
<defs>
  <linearGradient id="ibg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#111722"/>
    <stop offset="1" stop-color="#0d1117"/>
  </linearGradient>
</defs>
<rect width="{W2}" height="{H2}" rx="12" fill="url(#ibg)"/>
<rect x="0.5" y="0.5" width="{W2-1}" height="{H2-1}" rx="12" fill="none" stroke="#30363d"/>
<line x1="0" y1="30" x2="{W2}" y2="30" stroke="#30363d"/>
<circle cx="20" cy="15.0" r="5" fill="#ff5f56"/>
<circle cx="36" cy="15.0" r="5" fill="#ffbd2e"/>
<circle cx="52" cy="15.0" r="5" fill="#27c93f"/>
<text x="{W2/2:.1f}" y="19.0" fill="{C_GRAY}" font-size="12" text-anchor="middle">{USERNAME}@github: ~$ neofetch</text>
{info_parts_svg}
</svg>"""

out2 = os.path.join(OUT_DIR, "info-card.svg")
with open(out2, "w", encoding="utf-8") as f:
    f.write(svg2)
print(f"[OK] info-card.svg written       ({W2}×{H2}px, {os.path.getsize(out2)//1024} KB)")

# ═══════════════════════════════════════════════════════════════════════════════
# PART 3 — update README.md  (side-by-side table layout)
# ═══════════════════════════════════════════════════════════════════════════════
README_PATH = os.path.join(OUT_DIR, "README.md")

SIDE_BY_SIDE_BLOCK = """\
<table>
  <tr>
    <td valign="top"><img src="terminal-card.svg" alt="ASCII Portrait" width="540"/></td>
    <td valign="top"><img src="info-card.svg" alt="Info Card" width="400"/></td>
  </tr>
</table>

"""

try:
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace old terminal-card/info-card block if it exists, otherwise prepend
    import re
    # Remove any existing <table>...</table> block that contains terminal-card or info-card
    content = re.sub(
        r'<table>[\s\S]*?terminal-card\.svg[\s\S]*?</table>\s*\n?',
        '',
        content
    )
    # Also remove any standalone <p> img tags for these files
    content = re.sub(
        r'<p[^>]*>\s*<img src="terminal-card\.svg"[^>]*/>\s*</p>\s*\n?',
        '',
        content
    )
    content = re.sub(
        r'<p[^>]*>\s*<img src="info-card\.svg"[^>]*/>\s*</p>\s*\n?',
        '',
        content
    )
    # Remove old contribution animation p tag
    content = re.sub(
        r'<p[^>]*>\s*<img src="github-contribution-animation\.svg"[^>]*/>\s*</p>\s*\n?',
        '',
        content
    )

    # Prepend the side-by-side block at the very top, followed by contribution graph
    new_content = (
        SIDE_BY_SIDE_BLOCK
        + '<p align="center">\n  <img src="github-contribution-animation.svg" alt="GitHub Contribution Graph" width="850"/>\n</p>\n\n'
        + content.lstrip()
    )

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"[OK] README.md updated  (side-by-side table + contribution graph)")
except Exception as e:
    print(f"[WARN] Could not update README: {e}")
    print("       Manually add this to the top of your README.md:")
    print(SIDE_BY_SIDE_BLOCK)

print()
print("Done! Commit and push all three files:")
print("  git add terminal-card.svg info-card.svg README.md")
print('  git commit -m "feat: ASCII portrait + neofetch info card side by side"')
print("  git push")
