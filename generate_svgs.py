import random, math, textwrap

random.seed(42)

# ── helpers ────────────────────────────────────────────────────────────────────
COLORS = ["#161b22","#0e4429","#006d32","#26a641","#39d353"]

def pick_level():
    r = random.random()
    if r < 0.35: return 0
    if r < 0.55: return 1
    if r < 0.72: return 2
    if r < 0.87: return 3
    return 4

WEEKS = 53
DAYS  = 7
SQ    = 11   # square size
GAP   = 3    # gap between squares
STEP  = SQ + GAP  # 14
GRAPH_X = 34   # left offset (after weekday labels)
GRAPH_Y = 28   # top offset (after month labels)

MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

# ── BUILD contribution-animation.svg ───────────────────────────────────────────
def build_contrib():
    W, H = 850, 165
    lines = []

    # defs
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    lines.append('<defs>')
    # clip path for card
    lines.append(f'<clipPath id="card-clip"><rect width="{W}" height="{H}" rx="16"/></clipPath>')
    # sweep gradient
    lines.append('''<linearGradient id="sweep" x1="0%" y1="0%" x2="100%" y2="100%">
  <stop offset="0%" stop-color="white" stop-opacity="0"/>
  <stop offset="45%" stop-color="white" stop-opacity="0.06"/>
  <stop offset="55%" stop-color="white" stop-opacity="0.12"/>
  <stop offset="100%" stop-color="white" stop-opacity="0"/>
</linearGradient>''')
    # glow filter
    lines.append('''<filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
  <feGaussianBlur stdDeviation="1.5" result="blur"/>
  <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>''')
    lines.append('</defs>')

    # background card
    lines.append(f'<rect width="{W}" height="{H}" rx="16" fill="#0d1117" stroke="#30363d" stroke-width="1"/>')

    g = lines.append

    # month labels
    month_positions = []
    weeks_per_month = WEEKS / 12
    for i, m in enumerate(MONTHS):
        x = GRAPH_X + round(i * weeks_per_month) * STEP
        month_positions.append(x)
        lines.append(f'<text x="{x}" y="18" fill="#8b949e" font-size="10" font-family="system-ui,sans-serif">{m}</text>')

    # weekday labels
    for i, label in enumerate(["Mon","","Wed","","Fri","",""]):
        if label:
            y = GRAPH_Y + i * STEP + SQ - 1
            lines.append(f'<text x="0" y="{y}" fill="#8b949e" font-size="9" font-family="system-ui,sans-serif">{label}</text>')

    # build squares with animations
    total_cols = WEEKS
    anim_dur = 4.0   # seconds for reveal
    pause    = 2.0
    total    = anim_dur + pause
    col_delay_s = anim_dur / total_cols  # seconds per column

    for col in range(WEEKS):
        for row in range(DAYS):
            lvl   = pick_level()
            color = COLORS[lvl]
            x     = GRAPH_X + col * STEP
            y     = GRAPH_Y + row * STEP
            sq_id = f"s{col}_{row}"

            # delay in seconds
            delay = col * col_delay_s
            # each square appears, scales 0→1 with bounce
            # keyTimes: 0, delay_norm, delay_norm+spread, 1
            spread = 0.06  # fraction of total
            d0 = delay / total
            d1 = min(d0 + spread * 0.5, 0.99)
            d2 = min(d0 + spread, 0.99)

            filter_attr = ' filter="url(#glow)"' if lvl >= 3 else ''
            cx = x + SQ/2
            cy = y + SQ/2

            lines.append(
                f'<rect id="{sq_id}" x="{x}" y="{y}" width="{SQ}" height="{SQ}" rx="2" fill="{color}"{filter_attr}>'
            )
            # opacity animation
            lines.append(
                f'<animate attributeName="opacity" values="0;0;1;1" '
                f'keyTimes="0;{d0:.4f};{d2:.4f};1" dur="{total}s" repeatCount="indefinite"/>'
            )
            # scale via transform
            lines.append(
                f'<animateTransform attributeName="transform" type="scale" '
                f'values="1 1;0 0;1.15 1.15;1 1" '
                f'keyTimes="0;{d0:.4f};{d1:.4f};{d2:.4f}" '
                f'additive="sum" '
                f'dur="{total}s" repeatCount="indefinite" '
                f'calcMode="spline" keySplines="0 0 1 1;0.34 1.56 0.64 1;0.25 0.46 0.45 0.94"/>'
            )
            lines.append('</rect>')

    # diagonal sweep overlay
    sweep_w = W * 1.5
    lines.append(
        f'<rect x="{-sweep_w}" y="0" width="{sweep_w}" height="{H}" fill="url(#sweep)" opacity="0.6">'
    )
    lines.append(
        f'<animateTransform attributeName="transform" type="translate" '
        f'values="{-sweep_w} 0;{W+sweep_w} 0" dur="6s" repeatCount="indefinite"/>'
    )
    lines.append('</rect>')

    # CSS hover brightness (works in browsers, not GitHub – kept for completeness)
    lines.append('<style>rect[id^="s"]{transition:filter .15s}rect[id^="s"]:hover{filter:brightness(1.5)}</style>')

    lines.append('</svg>')
    return "\n".join(lines)

# ── BUILD terminal-card.svg ────────────────────────────────────────────────────
def build_terminal():
    W, H = 900, 520
    lines = []

    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')

    # ── defs ──────────────────────────────────────────────────────────────────
    lines.append('<defs>')

    # animated radial gradient background
    lines.append('''<radialGradient id="bg1" cx="20%" cy="30%" r="60%">
  <stop offset="0%" stop-color="#0d2137"/>
  <stop offset="100%" stop-color="#0d1117"/>
  <animate attributeName="cx" values="20%;80%;20%" dur="10s" repeatCount="indefinite"/>
  <animate attributeName="cy" values="30%;70%;30%" dur="12s" repeatCount="indefinite"/>
</radialGradient>
<radialGradient id="bg2" cx="80%" cy="70%" r="50%">
  <stop offset="0%" stop-color="#0a1a2e" stop-opacity="0.8"/>
  <stop offset="100%" stop-color="#0d1117" stop-opacity="0"/>
</radialGradient>''')

    # terminal glow
    lines.append('''<filter id="termglow">
  <feGaussianBlur stdDeviation="8" result="blur"/>
  <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<filter id="cyanglow">
  <feGaussianBlur stdDeviation="3" result="blur"/>
  <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<filter id="softglow">
  <feGaussianBlur stdDeviation="6" result="b"/>
  <feComposite in="b" in2="SourceGraphic" operator="over"/>
</filter>''')

    # glass gradient for terminal body
    lines.append('''<linearGradient id="glass" x1="0%" y1="0%" x2="0%" y2="100%">
  <stop offset="0%" stop-color="#161b22" stop-opacity="0.95"/>
  <stop offset="100%" stop-color="#0d1117" stop-opacity="0.98"/>
</linearGradient>
<linearGradient id="headerGrad" x1="0%" y1="0%" x2="0%" y2="100%">
  <stop offset="0%" stop-color="#1c2128"/>
  <stop offset="100%" stop-color="#161b22"/>
</linearGradient>
<linearGradient id="borderGlow" x1="0%" y1="0%" x2="100%" y2="100%">
  <stop offset="0%" stop-color="#00ffcc" stop-opacity="0.6"/>
  <stop offset="50%" stop-color="#0ea5e9" stop-opacity="0.3"/>
  <stop offset="100%" stop-color="#7c3aed" stop-opacity="0.6"/>
  <animate attributeName="x1" values="0%;100%;0%" dur="4s" repeatCount="indefinite"/>
  <animate attributeName="x2" values="100%;0%;100%" dur="4s" repeatCount="indefinite"/>
</linearGradient>''')

    # scanline pattern
    lines.append('''<pattern id="scanlines" x="0" y="0" width="900" height="3" patternUnits="userSpaceOnUse">
  <line x1="0" y1="1" x2="900" y2="1" stroke="white" stroke-opacity="0.03" stroke-width="1"/>
</pattern>''')

    # grid pattern
    lines.append('''<pattern id="grid" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse">
  <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#ffffff" stroke-width="0.3" stroke-opacity="0.04"/>
</pattern>''')

    # clip for terminal body
    lines.append('<clipPath id="termclip"><rect x="30" y="30" width="840" height="460" rx="14"/></clipPath>')
    lines.append('<clipPath id="bgclip"><rect width="900" height="520" rx="0"/></clipPath>')

    lines.append('</defs>')

    # ── background ────────────────────────────────────────────────────────────
    lines.append(f'<rect width="{W}" height="{H}" fill="url(#bg1)"/>')
    lines.append(f'<rect width="{W}" height="{H}" fill="url(#bg2)"/>')
    lines.append(f'<rect width="{W}" height="{H}" fill="url(#grid)" opacity="1"/>')

    # floating particles
    pts = [(random.randint(50,850), random.randint(50,470), random.uniform(0.3,1.2), random.uniform(3,9))
           for _ in range(28)]
    for px,py,pr,pdur in pts:
        dy = random.randint(-30,30)
        lines.append(
            f'<circle cx="{px}" cy="{py}" r="{pr:.1f}" fill="#00ffcc" opacity="0.18">'
            f'<animate attributeName="cy" values="{py};{py+dy};{py}" dur="{pdur:.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0.05;0.25;0.05" dur="{pdur:.1f}s" repeatCount="indefinite"/>'
            f'</circle>'
        )

    # ── terminal card shadow ──────────────────────────────────────────────────
    # outer glow border (pulsing)
    lines.append('<rect x="28" y="28" width="844" height="464" rx="15" fill="none" stroke="url(#borderGlow)" stroke-width="2">')
    lines.append('<animate attributeName="stroke-opacity" values="0.7;1;0.7" dur="3s" repeatCount="indefinite"/>')
    lines.append('</rect>')

    # floating animation wrapper (use translate)
    lines.append('<g>')
    lines.append('<animateTransform attributeName="transform" type="translate" values="0 0;0 -4;0 0" dur="4s" repeatCount="indefinite" calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1"/>')

    # terminal body
    lines.append('<rect x="30" y="30" width="840" height="460" rx="14" fill="url(#glass)" stroke="#30363d" stroke-width="1"/>')

    # glass sheen (top reflection)
    lines.append('<rect x="30" y="30" width="840" height="80" rx="14" fill="white" fill-opacity="0.025" clip-path="url(#termclip)"/>')

    # header bar
    lines.append('<rect x="30" y="30" width="840" height="44" rx="14" fill="url(#headerGrad)"/>')
    lines.append('<rect x="30" y="58" width="840" height="16" fill="url(#headerGrad)"/>')
    lines.append('<line x1="30" y1="74" x2="870" y2="74" stroke="#30363d" stroke-width="1"/>')

    # macOS buttons
    btns = [("#ff5f57","#ff5f57",55), ("#febc2e","#febc2e",79), ("#28c840","#28c840",103)]
    for fc,sc,bx in btns:
        lines.append(f'<circle cx="{bx}" cy="52" r="7" fill="{fc}" stroke="{sc}" stroke-width="0.5"/>')

    # title
    lines.append('<text x="450" y="57" text-anchor="middle" fill="#8b949e" font-size="13" font-family="ui-monospace,monospace">~/portfolio</text>')

    # scanlines overlay
    lines.append('<rect x="30" y="74" width="840" height="416" fill="url(#scanlines)" clip-path="url(#termclip)"/>')

    # animated scan line sweep
    lines.append('<rect x="30" y="74" width="840" height="2" fill="white" fill-opacity="0.04" clip-path="url(#termclip)">')
    lines.append('<animate attributeName="y" values="74;490;74" dur="5s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.6 1;0.4 0 0.6 1"/>')
    lines.append('</rect>')

    # ── terminal content ──────────────────────────────────────────────────────
    # Prompt line with typewriter
    TX = 56  # text x start

    # typing animation for "$ whoami" using SMIL visibility
    prompt_chars = list("$ whoami")
    lines.append('<text x="56" y="106" font-family="ui-monospace,Menlo,monospace" font-size="14" fill="#00ffcc">')
    # We'll show the prompt character by character using tspan + visibility animation
    # Each char appears at: char_index * 0.15s delay
    typing_dur = 8.0   # total loop
    char_dur   = 0.12  # seconds per character
    delete_start = 1.5  # pause before delete
    for i, ch in enumerate(prompt_chars):
        appear = i * char_dur
        vanish = len(prompt_chars) * char_dur + delete_start + (len(prompt_chars) - i - 1) * char_dur * 0.5
        a0 = appear / typing_dur
        a1 = vanish / typing_dur
        a1 = min(a1, 0.98)
        lines.append(
            f'<tspan opacity="0">{ch}'
            f'<animate attributeName="opacity" values="0;0;1;1;0;0" '
            f'keyTimes="0;{a0:.3f};{min(a0+0.01,0.99):.3f};{a1:.3f};{min(a1+0.02,0.99):.3f};1" '
            f'dur="{typing_dur}s" repeatCount="indefinite"/>'
            f'</tspan>'
        )
    lines.append('</text>')

    # blinking cursor
    lines.append('<rect x="56" y="92" width="8" height="14" fill="#00ffcc" rx="1">')
    lines.append(f'<animate attributeName="x" values="{56};{56 + len(prompt_chars)*8.5:.0f};{56}" '
                 f'keyTimes="0;{len(prompt_chars)*char_dur/typing_dur:.3f};1" '
                 f'dur="{typing_dur}s" repeatCount="indefinite"/>')
    lines.append('<animate attributeName="opacity" values="1;0;1" dur="0.8s" repeatCount="indefinite"/>')
    lines.append('</rect>')

    # ── content sections reveal ────────────────────────────────────────────────
    # Each section fades in with a delay, all content after the typing completes
    reveal_start = len(prompt_chars) * char_dur + 0.3  # seconds after typing
    sections = [
        ("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", "#30363d", 120, False),
        ("👤 Name:", "#8b949e", 138, False),
        ("   Lohitha Damisetti", "#e6edf3", 154, False),
        ("💻 Role:", "#8b949e", 172, False),
        ("   Full Stack Developer", "#00ffcc", 188, False),
        ("🚀 Stack:  React · Next.js · Node.js · TypeScript · Python", "#8b949e", 206, False),
        ("⚡ Interests:  AI · Open Source · Backend · Cloud", "#8b949e", 224, False),
        ("🏆 GitHub:  120 repositories", "#8b949e", 242, False),
        ("⭐ Stars:  450+", "#febc2e", 260, False),
        ("🔥 Current Focus:", "#8b949e", 278, False),
        ("   Building modern web experiences", "#39d353", 294, False),
        ("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", "#30363d", 312, False),
    ]

    sec_delay_each = 0.25  # seconds between sections appearing
    for idx, (text, color, y_pos, bold) in enumerate(sections):
        appear_t = (reveal_start + idx * sec_delay_each) / typing_dur
        appear_t = min(appear_t, 0.97)
        weight = "bold" if bold else "normal"
        lines.append(
            f'<text x="{TX}" y="{y_pos}" font-family="ui-monospace,Menlo,monospace" '
            f'font-size="12.5" fill="{color}" font-weight="{weight}" opacity="0">'
            f'{text}'
            f'<animate attributeName="opacity" values="0;0;1;1" '
            f'keyTimes="0;{appear_t:.3f};{min(appear_t+0.04,0.99):.3f};1" '
            f'dur="{typing_dur}s" repeatCount="indefinite"/>'
            f'</text>'
        )

    lines.append('</g>')  # close floating group
    lines.append('</svg>')
    return "\n".join(lines)


# ── write files ───────────────────────────────────────────────────────────────
with open("github-contribution-animation.svg","w",encoding="utf-8") as f:
    f.write(build_contrib())
print("[OK] github-contribution-animation.svg written")

with open("terminal-card.svg","w",encoding="utf-8") as f:
    f.write(build_terminal())
print("[OK] terminal-card.svg written")
