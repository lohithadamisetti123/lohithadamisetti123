import random
random.seed(77)

W, H   = 900, 520
TOTAL  = 16.0   # loop seconds

PROMPT = "$ whoami"
N      = len(PROMPT)
CTIME  = 0.09          # type speed per char
DTIME  = 0.06          # delete speed per char
t_end  = N * CTIME
t_p1   = t_end + 0.9   # pause after typing
t_ds   = t_p1
t_de   = t_ds + N * DTIME
t_info = t_de + 0.35
STEP   = 0.37           # reveal delay per line
t_hold = t_info + 16 * STEP
t_fade = min(t_hold + 0.8, TOTAL - 0.5)

def f(t): return f"{min(max(t/TOTAL,0),1):.4f}"

# particles
pcl = ""
for _ in range(22):
    px,py = random.randint(30,870), random.randint(30,510)
    pr    = round(random.uniform(0.5,1.4),1)
    pd    = round(random.uniform(4,11),1)
    dy    = random.randint(-28,28)
    pcl  += (f'<circle cx="{px}" cy="{py}" r="{pr}" fill="#00d4aa" opacity="0.1">'
             f'<animate attributeName="cy" values="{py};{py+dy};{py}" dur="{pd}s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values="0.04;0.18;0.04" dur="{pd}s" repeatCount="indefinite"/>'
             f'</circle>\n')

# typewriter tspans
CW = 8.15
CX = 52.0
tspans = ""
for i, ch in enumerate(PROMPT):
    ta  = (i * CTIME) / TOTAL
    ta2 = min(ta + 0.008, 0.99)
    td  = (t_ds + (N-1-i) * DTIME) / TOTAL
    td2 = min(td + 0.015, 0.99)
    safe_ch = ch.replace("&","&amp;").replace("<","&lt;")
    tspans += (f'<tspan opacity="0">{safe_ch}'
               f'<animate attributeName="opacity" values="0;0;1;1;0;0"'
               f' keyTimes="0;{ta:.4f};{ta2:.4f};{td:.4f};{td2:.4f};1"'
               f' dur="{TOTAL}s" repeatCount="indefinite"/></tspan>')

# cursor x keyframes
cx_v, cx_t = [CX], [0.0]
for i in range(N):
    cx_v.append(CX+(i+1)*CW); cx_t.append(min((i+1)*CTIME/TOTAL,0.99))
cx_v.append(CX+N*CW); cx_t.append(min(t_p1/TOTAL,0.99))
for i in range(N):
    cx_v.append(CX+(N-i-1)*CW); cx_t.append(min((t_ds+(i+1)*DTIME)/TOTAL,0.99))
cx_v.append(CX); cx_t.append(1.0)
cx_vals  = ";".join(f"{v:.2f}" for v in cx_v)
cx_times = ";".join(f"{t:.4f}" for t in cx_t)

# info lines
LX,VX,LH,Y0 = 52,190,20,118
info = [
    ("user","lohitha@github",   "#00d4aa", None, None),
    ("sep", "\u2500"*36,        "#30363d", None, None),
    ("kv",  "Name",   "#00d4aa","Lohitha Damisetti",           "#e6edf3"),
    ("kv",  "Role",   "#00d4aa","Full Stack Developer",         "#e6edf3"),
    ("kv",  "College","#00d4aa","Aditya CE&amp;T  |  Data Science","#e6edf3"),
    ("bl",  None,None,None,None),
    ("sec", "\u2500\u2500 Stack","#00d4aa",None,None),
    ("kv",  "Frontend","#00d4aa","React  Next.js  TypeScript  Vue",     "#8b949e"),
    ("kv",  "Backend", "#00d4aa","Node.js  Express  FastAPI  Spring",   "#8b949e"),
    ("kv",  "Database","#00d4aa","MongoDB  PostgreSQL  Redis",           "#8b949e"),
    ("kv",  "AI / ML", "#00d4aa","OpenAI  Gemini  Ollama  LangChain",   "#8b949e"),
    ("bl",  None,None,None,None),
    ("sec", "\u2500\u2500 Competitive","#00d4aa",None,None),
    ("kv",  "LeetCode",  "#00d4aa","480+ Solved",           "#e6edf3"),
    ("kv",  "CodeChef",  "#00d4aa","500+ Solved",           "#e6edf3"),
    ("kv",  "HackerRank","#00d4aa","7 Badges  |  20 Stars", "#e6edf3"),
    ("bl",  None,None,None,None),
    ("sec", "\u2500\u2500 Focus","#00d4aa",None,None),
    ("kv",  "Current","#00d4aa","Building scalable modern web apps","#e6edf3"),
]

info_xml = ""
y = Y0
li = 0
for kind,label,lc,val,vc in info:
    if kind == "bl":
        y += LH; continue
    ts = t_info + li * STEP
    ts2= ts + 0.15
    # keep as floats, clamp to [0,1], ensure strictly increasing
    ks = [0.0,
          min(max(ts/TOTAL,       0.0), 1.0),
          min(max(ts2/TOTAL,      0.0), 0.99),
          min(max(t_fade/TOTAL,   0.0), 0.98),
          min(max((t_fade+0.4)/TOTAL,0.0), 0.99),
          1.0]
    for i in range(1, len(ks)):
        if ks[i] <= ks[i-1]:
            ks[i] = min(ks[i-1] + 0.001, 1.0)
    kt = ";".join(f"{k:.4f}" for k in ks)
    an = (f'<animate attributeName="opacity" values="0;0;1;1;0;0"'
          f' keyTimes="{kt}" dur="{TOTAL}s" repeatCount="indefinite"'
          f' calcMode="spline" keySplines="0 0 1 1;0.3 0 0.7 1;0 0 1 1;0.3 0 0.7 1;0 0 1 1"/>')
    fw = "bold" if kind == "user" else "normal"
    if kind in ("user","sep","sec"):
        info_xml += (f'<text x="{LX}" y="{y}" font-family="ui-monospace,Menlo,monospace"'
                     f' font-size="13" fill="{lc}" font-weight="{fw}" opacity="0">{label}{an}</text>\n')
    else:
        info_xml += (f'<text x="{LX}" y="{y}" font-family="ui-monospace,Menlo,monospace"'
                     f' font-size="13" fill="{lc}" font-weight="bold" opacity="0">{label}{an}</text>\n'
                     f'<text x="{VX}" y="{y}" font-family="ui-monospace,Menlo,monospace"'
                     f' font-size="13" fill="{vc}" opacity="0">{val}{an}</text>\n')
    y += LH; li += 1

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <radialGradient id="bg1" cx="25%" cy="25%" r="65%">
    <stop offset="0%" stop-color="#0d2137"/>
    <stop offset="100%" stop-color="#0d1117"/>
    <animate attributeName="cx" values="25%;75%;25%" dur="11s" repeatCount="indefinite"/>
    <animate attributeName="cy" values="25%;65%;25%" dur="13s" repeatCount="indefinite"/>
  </radialGradient>
  <radialGradient id="bg2" cx="75%" cy="70%" r="55%">
    <stop offset="0%" stop-color="#001a0a" stop-opacity="0.7"/>
    <stop offset="100%" stop-color="#0d1117" stop-opacity="0"/>
  </radialGradient>
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#ffffff" stroke-width="0.25" stroke-opacity="0.04"/>
  </pattern>
  <linearGradient id="bglass" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" stop-color="#161b22" stop-opacity="0.96"/>
    <stop offset="100%" stop-color="#0d1117" stop-opacity="0.99"/>
  </linearGradient>
  <linearGradient id="hdrGrad" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" stop-color="#1e2530"/>
    <stop offset="100%" stop-color="#161b22"/>
  </linearGradient>
  <linearGradient id="borderAnim" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#00d4aa" stop-opacity="0.7"/>
    <stop offset="50%" stop-color="#0ea5e9" stop-opacity="0.35"/>
    <stop offset="100%" stop-color="#7c3aed" stop-opacity="0.7"/>
    <animate attributeName="x1" values="0%;100%;0%" dur="4s" repeatCount="indefinite"/>
    <animate attributeName="x2" values="100%;0%;100%" dur="4s" repeatCount="indefinite"/>
  </linearGradient>
  <filter id="tglow">
    <feGaussianBlur stdDeviation="6" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="cglow">
    <feGaussianBlur stdDeviation="2.5" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <pattern id="scanlines" width="900" height="3" patternUnits="userSpaceOnUse">
    <line x1="0" y1="1" x2="900" y2="1" stroke="white" stroke-opacity="0.025" stroke-width="1"/>
  </pattern>
  <clipPath id="tc"><rect x="28" y="28" width="844" height="464" rx="13"/></clipPath>
</defs>

<!-- background -->
<rect width="{W}" height="{H}" fill="url(#bg1)"/>
<rect width="{W}" height="{H}" fill="url(#bg2)"/>
<rect width="{W}" height="{H}" fill="url(#grid)"/>

<!-- particles -->
{pcl}

<!-- border glow -->
<rect x="26" y="26" width="848" height="468" rx="14" fill="none" stroke="url(#borderAnim)" stroke-width="1.5">
  <animate attributeName="stroke-opacity" values="0.6;1;0.6" dur="3s" repeatCount="indefinite"/>
</rect>

<!-- floating terminal -->
<g>
  <animateTransform attributeName="transform" type="translate"
    values="0,0;0,-5;0,0" dur="5s" repeatCount="indefinite"
    calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1"/>

  <!-- window body -->
  <rect x="28" y="28" width="844" height="464" rx="13" fill="url(#bglass)" stroke="#30363d" stroke-width="1"/>

  <!-- glass sheen -->
  <rect x="28" y="28" width="844" height="90" rx="13" fill="white" fill-opacity="0.02" clip-path="url(#tc)"/>

  <!-- header -->
  <rect x="28" y="28" width="844" height="46" rx="13" fill="url(#hdrGrad)"/>
  <rect x="28" y="58" width="844" height="16" fill="url(#hdrGrad)"/>
  <line x1="28" y1="74" x2="872" y2="74" stroke="#30363d" stroke-width="1"/>

  <!-- traffic lights -->
  <circle cx="54"  cy="51" r="7" fill="#ff5f57"/>
  <circle cx="78"  cy="51" r="7" fill="#febc2e"/>
  <circle cx="102" cy="51" r="7" fill="#28c840"/>

  <!-- title -->
  <text x="450" y="56" text-anchor="middle" fill="#8b949e"
    font-family="ui-monospace,Menlo,monospace" font-size="13">lohitha@github: ~$ whoami</text>

  <!-- scanlines -->
  <rect x="28" y="74" width="844" height="418" fill="url(#scanlines)" clip-path="url(#tc)"/>

  <!-- scan sweep line -->
  <rect x="28" y="74" width="844" height="2" fill="white" fill-opacity="0.04" clip-path="url(#tc)">
    <animate attributeName="y" values="74;492;74" dur="5s" repeatCount="indefinite"
      calcMode="spline" keySplines="0.4 0 0.6 1;0.4 0 0.6 1"/>
  </rect>

  <!-- prompt line -->
  <text x="52" y="100" font-family="ui-monospace,Menlo,monospace" font-size="13.5" fill="#00d4aa" filter="url(#cglow)">
    <tspan fill="#8b949e">lohitha@github</tspan>
    <tspan fill="#e6edf3"> ~ </tspan>
    {tspans}
  </text>

  <!-- blinking cursor -->
  <rect y="87" width="7" height="14" rx="1" fill="#00d4aa" filter="url(#cglow)">
    <animate attributeName="x" values="{cx_vals}"
      keyTimes="{cx_times}" dur="{TOTAL}s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="1;0;1" dur="0.75s" repeatCount="indefinite"/>
  </rect>

  <!-- info content -->
  {info_xml}

  <!-- divider line between prompt and content -->
  <line x1="52" y1="108" x2="848" y2="108" stroke="#21262d" stroke-width="1" opacity="0">
    <animate attributeName="opacity" values="0;0;0.6;0.6;0;0"
      keyTimes="0;{f(t_info)};{f(t_info+0.2)};{f(t_fade)};{f(t_fade+0.3)};1"
      dur="{TOTAL}s" repeatCount="indefinite"/>
  </line>

</g>
</svg>"""

with open("terminal-card.svg","w",encoding="utf-8") as fh:
    fh.write(svg)
print("[OK] terminal-card.svg written")
