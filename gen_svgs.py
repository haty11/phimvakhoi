import random, math, os

random.seed(77)
W, H = 1200, 675
BX, BY = 600, -80

particles = []
for _ in range(700):
    a_off = random.gauss(0, 0.13)
    a_off = max(-0.27, min(0.27, a_off))
    d = random.uniform(40, H + 90)
    px = BX + d * math.sin(a_off)
    py = BY + d * math.cos(a_off)
    if 0 <= px <= W and 0 <= py <= H:
        b = random.uniform(0.12, 0.60)
        r = random.uniform(0.4, 1.8)
        particles.append((px, py, r, b))

def cone_pts(half_a, spread=0):
    dist = H - BY
    hw = dist * math.tan(half_a) + spread
    return f"{BX},{BY} {BX-hw:.1f},{H} {BX+hw:.1f},{H}"

OUT = "/sessions/stoic-vibrant-dijkstra/mnt/outputs/"
ly  = int(H * 0.67)
ty  = int(H * 0.43)

# ── 1. FULL THUMBNAIL SVG ──────────────────────────────────────────────
header = f"""<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<defs>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@1,400&amp;display=swap');
  </style>
  <linearGradient id="gw" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%"   stop-color="#3c2e18" stop-opacity="0.50"/>
    <stop offset="70%"  stop-color="#120e08" stop-opacity="0.15"/>
    <stop offset="100%" stop-color="#030201" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="gm" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%"   stop-color="#4a3820" stop-opacity="0.65"/>
    <stop offset="55%"  stop-color="#1a1208" stop-opacity="0.25"/>
    <stop offset="100%" stop-color="#050402" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="gc" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%"   stop-color="#5e4828" stop-opacity="0.80"/>
    <stop offset="42%"  stop-color="#221a0e" stop-opacity="0.45"/>
    <stop offset="100%" stop-color="#060503" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="gn" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%"   stop-color="#705a32" stop-opacity="0.85"/>
    <stop offset="32%"  stop-color="#2a2012" stop-opacity="0.55"/>
    <stop offset="100%" stop-color="#080604" stop-opacity="0"/>
  </linearGradient>
</defs>
<rect width="{W}" height="{H}" fill="#070707"/>
<polygon points="{cone_pts(0.44, 40)}" fill="url(#gw)"/>
<polygon points="{cone_pts(0.33)}"      fill="url(#gm)"/>
<polygon points="{cone_pts(0.20)}"      fill="url(#gc)"/>
<polygon points="{cone_pts(0.09)}"      fill="url(#gn)"/>"""

dust_lines = []
for (px, py, r, b) in particles:
    cr = int(190*b); cg = int(155*b); cb = int(100*b)
    dust_lines.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r:.1f}" fill="rgb({cr},{cg},{cb})" opacity="{b:.2f}"/>')

footer = f"""<line x1="90" y1="{ly}" x2="{W-90}" y2="{ly}" stroke="#28221a" stroke-width="1"/>
<text x="{W//2+2}" y="{ty+2}"
  font-family="Lora, Georgia, 'Times New Roman', serif"
  font-style="italic" font-size="92" text-anchor="middle"
  fill="#1a140c" opacity="0.7">Phim &amp; Khói</text>
<text x="{W//2}" y="{ty}"
  font-family="Lora, Georgia, 'Times New Roman', serif"
  font-style="italic" font-size="92" text-anchor="middle"
  fill="#baa88a">Phim &amp; Khói</text>
<text x="{W//2}" y="{ly+20}"
  font-family="'Courier New', monospace"
  font-size="11" letter-spacing="5" text-anchor="middle"
  fill="#4e7a60">PHAN TICH DIEN ANH</text>
<text x="{W//2}" y="28"
  font-family="'Courier New', monospace"
  font-size="10" letter-spacing="3" text-anchor="middle"
  fill="#1c180e">f/1.4  -  24fps  -  35mm</text>
</svg>"""

svg = header + "\n" + "\n".join(dust_lines) + "\n" + footer
with open(OUT + "phimvakhoi-thumbnail.svg", "w") as f:
    f.write(svg)
print(f"Thumbnail SVG done ({len(particles)} particles)")

# ── 2. NAVBAR LOGO SVG ────────────────────────────────────────────────
nav_svg = """<svg viewBox="0 0 260 52" xmlns="http://www.w3.org/2000/svg">
<defs>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@1,400&amp;display=swap');
  </style>
  <linearGradient id="nb" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%"   stop-color="#6a5430" stop-opacity="0.9"/>
    <stop offset="100%" stop-color="#1a1208" stop-opacity="0"/>
  </linearGradient>
</defs>
<rect width="260" height="52" fill="#080808"/>
<polygon points="22,-4 6,52 38,52"  fill="url(#nb)" opacity="0.55"/>
<polygon points="22,-4 12,52 32,52" fill="url(#nb)" opacity="0.60"/>
<polygon points="22,-4 17,52 27,52" fill="url(#nb)" opacity="0.70"/>
<line x1="50" y1="12" x2="50" y2="40" stroke="#2a2418" stroke-width="1"/>
<text x="62" y="33"
  font-family="Lora, Georgia, serif"
  font-style="italic" font-size="22"
  fill="#b8a68a">Phim &amp; Khoi</text>
</svg>"""

with open(OUT + "phimvakhoi-logo-navbar.svg", "w") as f:
    f.write(nav_svg)
print("Navbar logo done")

# ── 3. SQUARE / FAVICON SVG ───────────────────────────────────────────
sq_svg = """<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
<defs>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@1,400&amp;display=swap');
  </style>
  <linearGradient id="fb" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%"   stop-color="#7a6038" stop-opacity="0.9"/>
    <stop offset="100%" stop-color="#0e0a06" stop-opacity="0"/>
  </linearGradient>
</defs>
<rect width="100" height="100" fill="#070707" rx="6"/>
<polygon points="50,-8 16,100 84,100" fill="url(#fb)" opacity="0.50"/>
<polygon points="50,-8 28,100 72,100" fill="url(#fb)" opacity="0.55"/>
<polygon points="50,-8 38,100 62,100" fill="url(#fb)" opacity="0.65"/>
<polygon points="50,-8 44,100 56,100" fill="url(#fb)" opacity="0.75"/>
<text x="50" y="68"
  font-family="Lora, Georgia, serif"
  font-style="italic" font-size="34"
  text-anchor="middle"
  fill="#baa78a">P&amp;K</text>
<line x1="18" y1="80" x2="82" y2="80" stroke="#2a2218" stroke-width="0.8"/>
</svg>"""

with open(OUT + "phimvakhoi-logo-square.svg", "w") as f:
    f.write(sq_svg)
print("Square logo done")
