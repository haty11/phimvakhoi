"""
patch2.py — fixes:
  1. Create small optimised thumbnail SVG (no particles, ~2 KB)
  2. Revert navbar to text in ALL pages
  3. Replace Unsplash images in ARTICLES array → local SVG
  4. Add data-filter attrs to tabs + rewrite renderArticles / setTab
  5. Update sidebar thumbnails → small SVG
"""
import re, os, shutil

BASE = "/sessions/stoic-vibrant-dijkstra/mnt/outputs/"

# ── 1. Create lightweight thumbnail for sidebars (~2 KB, no particles) ──────
SMALL_SVG = """<svg viewBox="0 0 1200 675" xmlns="http://www.w3.org/2000/svg">
<defs>
  <linearGradient id="a" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#3c2e18" stop-opacity=".5"/>
    <stop offset="100%" stop-color="#030201" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="b" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#5e4828" stop-opacity=".8"/>
    <stop offset="100%" stop-color="#060503" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="c" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#705a32" stop-opacity=".85"/>
    <stop offset="100%" stop-color="#080604" stop-opacity="0"/>
  </linearGradient>
</defs>
<rect width="1200" height="675" fill="#070707"/>
<polygon points="600,-80 -60,675 1260,675" fill="url(#a)"/>
<polygon points="600,-80 300,675 900,675" fill="url(#b)"/>
<polygon points="600,-80 450,675 750,675" fill="url(#c)"/>
<line x1="90" y1="452" x2="1110" y2="452" stroke="#28221a" stroke-width="1"/>
<text x="600" y="295" font-family="Georgia,serif" font-style="italic"
  font-size="92" text-anchor="middle" fill="#baa88a">Phim &amp; Kh&#xF3;i</text>
<text x="600" y="472" font-family="monospace" font-size="11"
  letter-spacing="5" text-anchor="middle" fill="#4e7a60">PH&#xC2;N T&#xCD;CH &#x110;I&#x1EC6;N &#x1EA2;NH</text>
</svg>"""

small_path = BASE + "assets/images/phimvakhoi-thumb-sm.svg"
with open(small_path, "w") as f:
    f.write(SMALL_SVG)
print(f"✓ Created {small_path} ({len(SMALL_SVG)} bytes)")

# ── 2. Revert navbar logo → text in ALL pages ─────────────────────────────
NAV_IMG_RE = re.compile(
    r'class="nav-logo"><img src="[^"]*phimvakhoi-logo-navbar\.svg"[^/]*/></a>'
)
NAV_TEXT = 'class="nav-logo">Phim <span class="amp">&</span> Khói</a>'

pages = (
    ["index.html", "blog/index.html"] +
    [f"blog/phan-tich-phim/{s}/index.html" for s in [
        "nolan-va-thoi-gian","mau-sac-wes-anderson",
        "kubrick-anh-sang-tu-nhien","jordan-peele-spectacle"]] +
    ["blog/ky-thuat/shot-reverse-shot/index.html"] +
    [f"blog/bien-kich/{s}/index.html" for s in [
        "tarantino-doi-thoai-pulp-fiction","viet-phim-kinh-di",
        "phan-tich-kich-ban-kinh-di"]]
)

for rel in pages:
    p = BASE + rel
    with open(p) as f: c = f.read()
    new_c = NAV_IMG_RE.sub(NAV_TEXT, c)
    if new_c != c:
        with open(p, "w") as f: f.write(new_c)
        print(f"  ✓ navbar reverted: {rel}")

# ── 3 + 4. Patch index.html — images + tabs + render script ──────────────
idx_path = BASE + "index.html"
with open(idx_path) as f:
    idx = f.read()

# 3a. Replace Unsplash URLs in ARTICLES array (image: "https://..." lines)
idx = re.sub(
    r'(image:\s*")https://images\.unsplash\.com/[^"]*(")',
    r'\1assets/images/phimvakhoi-thumbnail.svg\2',
    idx
)
# Also fix Unsplash in col-news static articles
idx = re.sub(
    r'(src=")https://images\.unsplash\.com/[^"]*(")',
    r'\1assets/images/phimvakhoi-thumb-sm.svg\2',
    idx
)
print("  ✓ Replaced Unsplash image URLs in index.html")

# 3b. Add data-filter to tabs
idx = idx.replace(
    '<div class="tab active" onclick="setTab(this)">✍️ Phân tích phim</div>',
    '<div class="tab active" data-filter="phan-tich" onclick="setTab(this)">✍️ Phân tích phim</div>'
)
idx = idx.replace(
    '<div class="tab" onclick="setTab(this)">🎥 Kỹ thuật</div>',
    '<div class="tab" data-filter="ky-thuat" onclick="setTab(this)">🎥 Kỹ thuật</div>'
)
idx = idx.replace(
    '<div class="tab" onclick="setTab(this)">📰 Tin tức phim</div>',
    '<div class="tab" data-filter="tin-tuc" onclick="setTab(this)">📰 Tin tức phim</div>'
)
idx = idx.replace(
    '<div class="tab" onclick="setTab(this)">🎓 Khoá học</div>',
    '<div class="tab" data-filter="khoa-hoc" onclick="setTab(this)">🎓 Khoá học</div>'
)
idx = idx.replace(
    '<div class="tab" onclick="setTab(this)">🌍 Liên hoan phim</div>',
    '<div class="tab" data-filter="lien-hoan" onclick="setTab(this)">🌍 Liên hoan phim</div>'
)
print("  ✓ Added data-filter to tabs")

# 4. Replace JS render + setTab block
OLD_SCRIPT_START = "// ── Render Hero ──"
OLD_SCRIPT_END   = "// ── Nav shadow on scroll ──"

NEW_JS = """// ── Helpers ──────────────────────────────────────────────────────────────
const DEF_IMG = 'assets/images/phimvakhoi-thumbnail.svg';

function cardBig(a) {
  return `<a href="${a.url}" class="acard" style="display:block;text-decoration:none;color:inherit;">
    <div class="acard-img"><img src="${a.image||DEF_IMG}" alt="${a.title}" loading="lazy"/></div>
    <div class="acard-cat ${a.catClass}">● ${a.category}</div>
    <h2 class="acard-title">${a.title}</h2>
    <p class="acard-excerpt">${a.excerpt||''}</p>
    <div class="acard-meta"><span>${a.readTime}</span><span class="sep">·</span><span>${a.date}</span></div>
  </a>`;
}

function cardSm(a) {
  return `<a href="${a.url}" class="acard" style="display:block;text-decoration:none;color:inherit;">
    <div class="acard-row">
      <div class="acard-img-sm"><img src="${a.image||DEF_IMG}" alt="${a.title}" loading="lazy"/></div>
      <div class="acard-row-text">
        <div class="acard-cat ${a.catClass}">● ${a.category}</div>
        <h3 class="acard-title-sm">${a.title}</h3>
        <div class="acard-meta"><span>${a.readTime}</span><span class="sep">·</span><span>${a.date}</span></div>
      </div>
    </div>
  </a>`;
}

// ── Render articles by filter key ─────────────────────────────────────────
function renderArticles(filterKey) {
  const list = document.getElementById('articles-list');
  const hdr  = document.querySelector('.col-articles .sec-ttl');

  // Category keyword map
  const CAT = {
    'phan-tich': 'phân tích',
    'ky-thuat':  'kỹ thuật',
    'lien-hoan': 'liên hoan',
  };

  if (filterKey === 'tin-tuc') {
    hdr.textContent = '📰 Tin tức phim mới nhất';
    list.innerHTML = NEWS.map(n => `
      <div class="nitem" style="margin-bottom:14px;">
        <div class="ndot ${n.dot}"></div>
        <div><div class="n-text">${n.text}</div>
             <div class="n-src">${n.source}</div></div>
      </div>`).join('');
    return;
  }

  if (filterKey === 'khoa-hoc') {
    hdr.textContent = '🎓 Khoá học';
    list.innerHTML = COURSES.map(c => `
      <a href="${c.url}" class="acard" style="display:block;text-decoration:none;color:inherit;">
        <div class="acard-row">
          <div class="acard-img-sm" style="display:flex;align-items:center;justify-content:center;font-size:30px;background:var(--bg-card);">${c.icon}</div>
          <div class="acard-row-text">
            <div class="acard-cat cat-tech">● Khoá học</div>
            <h3 class="acard-title-sm">${c.name}</h3>
            <div class="acard-meta">${c.meta} &nbsp;<span class="badge ${c.badgeClass}">${c.badge}</span></div>
          </div>
        </div>
      </a>`).join('');
    return;
  }

  // Article filter
  const catKw = CAT[filterKey] || null;
  hdr.textContent = filterKey === 'all'
    ? '✍️ Bài viết mới nhất'
    : document.querySelector(`.tab[data-filter="${filterKey}"]`).textContent.trim();

  const pool = ARTICLES.filter(a => {
    if (a.featured) return false;
    if (!catKw) return true; // 'all' or unknown → show all
    return a.category.toLowerCase().includes(catKw);
  });

  if (!pool.length) {
    list.innerHTML = '<div style="padding:32px 0;text-align:center;color:var(--text-faint);font-size:13px;">Chưa có bài viết trong mục này — đang cập nhật.</div>';
    return;
  }

  const [first, ...rest] = pool;
  list.innerHTML = cardBig(first) + rest.map(cardSm).join('');
}

// ── Tab switching ─────────────────────────────────────────────────────────
function setTab(el) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  el.classList.add('active');
  renderArticles(el.dataset.filter);
}

// ── Render Hero ──"""

NEW_JS_END = """  // ── Render initial articles (all) ──
  renderArticles('all');

  // ── Render News ──"""

# --- do the replacement ---
start_idx = idx.find(OLD_SCRIPT_START)
end_idx   = idx.find(OLD_SCRIPT_END)

if start_idx == -1 or end_idx == -1:
    print("  ⚠ Could not find script boundaries — check manually")
else:
    old_block   = idx[start_idx:end_idx]
    # Extract just the Hero render + News/Courses render lines we want to keep
    hero_block = ""
    in_hero = False
    skip_render_articles = False
    for line in old_block.split('\n'):
        stripped = line.strip()
        # Skip the old standalone articles render block
        if stripped.startswith('const list = document.getElementById') or \
           stripped.startswith('const others = ARTICLES') or \
           stripped.startswith('const [first') or \
           stripped.startswith('// Rest —') or \
           stripped.startswith('// First non-featured') or \
           (skip_render_articles and stripped.startswith('rest.forEach')):
            skip_render_articles = True
            continue
        if skip_render_articles and stripped.startswith('// ── Render News'):
            skip_render_articles = False
        if skip_render_articles:
            continue
        hero_block += line + '\n'

    new_block = NEW_JS + '\n' + hero_block.strip()
    idx = idx[:start_idx] + new_block + '\n\n  ' + NEW_JS_END + idx[end_idx + len(OLD_SCRIPT_END):]
    print("  ✓ Rewrote renderArticles + setTab in index.html")

with open(idx_path, "w") as f:
    f.write(idx)
print("  ✓ index.html saved")

# ── 5. Sidebar thumbnails in all 8 articles → small SVG ──────────────────
ARTICLE_FILES = [
    "blog/phan-tich-phim/nolan-va-thoi-gian/index.html",
    "blog/phan-tich-phim/mau-sac-wes-anderson/index.html",
    "blog/phan-tich-phim/kubrick-anh-sang-tu-nhien/index.html",
    "blog/phan-tich-phim/jordan-peele-spectacle/index.html",
    "blog/ky-thuat/shot-reverse-shot/index.html",
    "blog/bien-kich/tarantino-doi-thoai-pulp-fiction/index.html",
    "blog/bien-kich/viet-phim-kinh-di/index.html",
    "blog/bien-kich/phan-tich-kich-ban-kinh-di/index.html",
]

# Replace the full-size SVG thumbnail in sidebars with the small version
for rel in ARTICLE_FILES:
    p = BASE + rel
    with open(p) as f: c = f.read()
    new_c = c.replace(
        '../../../assets/images/phimvakhoi-thumbnail.svg',
        '../../../assets/images/phimvakhoi-thumb-sm.svg'
    )
    if new_c != c:
        with open(p, "w") as f: f.write(new_c)
        print(f"  ✓ sidebar thumbnails updated: {rel}")

print("\nAll patches done ✓")
