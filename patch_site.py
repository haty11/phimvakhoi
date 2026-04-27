"""
patch_site.py — 3 tasks:
  1. Copy SVG assets → assets/images/
  2. Navbar logo text → SVG img (all pages)
  3. Sidebar Unsplash thumbnails → local SVG
  4. Standardise article-nav (old style → card style, update labels)
  5. Add .nav-logo img CSS
"""
import re, shutil, os

BASE = "/sessions/stoic-vibrant-dijkstra/mnt/outputs/"

# ── 1. Copy SVGs to assets/images ─────────────────────────────────────────
for name in ("phimvakhoi-logo-navbar.svg", "phimvakhoi-thumbnail.svg",
             "phimvakhoi-logo-square.svg"):
    src = BASE + name
    dst = BASE + "assets/images/" + name
    if os.path.exists(src):
        shutil.copy(src, dst)
        print(f"  copied → {dst}")

# ── 2. CSS patch: .nav-logo img ────────────────────────────────────────────
css_path = BASE + "assets/css/style.css"
with open(css_path) as f:
    css = f.read()

NAV_LOGO_IMG_CSS = "\n.nav-logo img { height: 34px; display: block; }\n"
if ".nav-logo img" not in css:
    css = css.replace(
        ".nav-logo .amp { color: var(--sage); font-style: italic; }",
        ".nav-logo .amp { color: var(--sage); font-style: italic; }" + NAV_LOGO_IMG_CSS
    )
    with open(css_path, "w") as f:
        f.write(css)
    print("  CSS updated: .nav-logo img")

# ── helpers ────────────────────────────────────────────────────────────────
OLD_NAV_TEXT = 'Phim <span class="amp">&</span> Khói'

def logo_img(rel_prefix):
    return f'<img src="{rel_prefix}assets/images/phimvakhoi-logo-navbar.svg" alt="Phim &amp; Khói" />'

def patch_nav_logo(content, rel_prefix):
    return content.replace(OLD_NAV_TEXT, logo_img(rel_prefix))

# Replace Unsplash URLs inside sidebar-related-img or sb-post-img divs
UNSPLASH_RE = re.compile(
    r'(class="(?:sidebar-related-img|sb-post-img)">'
    r'<img src=")https://images\.unsplash\.com/[^"]*(")',
    re.DOTALL
)

def patch_unsplash(content, thumb_path):
    return UNSPLASH_RE.sub(lambda m: m.group(1) + thumb_path + m.group(2), content)

# Convert old-style <nav class="article-nav"> → card <div class="article-nav">
OLD_NAV_RE = re.compile(
    r'<nav class="article-nav">\s*'
    r'<a href="([^"]+)" class="article-nav-prev">←\s*(.+?)</a>\s*'
    r'<a href="([^"]+)" class="article-nav-next">(.+?)\s*→</a>\s*'
    r'</nav>',
    re.DOTALL
)

def make_card_nav(prev_href, prev_title, next_href, next_title):
    return (
        '<div class="article-nav">\n'
        f'  <a href="{prev_href}" class="art-nav-btn" style="text-decoration:none;">\n'
        f'    <div class="art-nav-label">← BÀI TRƯỚC</div>\n'
        f'    <div class="art-nav-title">{prev_title.strip()}</div>\n'
        f'  </a>\n'
        f'  <a href="{next_href}" class="art-nav-btn art-nav-right" style="text-decoration:none;">\n'
        f'    <div class="art-nav-label">BÀI TIẾP THEO →</div>\n'
        f'    <div class="art-nav-title">{next_title.strip()}</div>\n'
        f'  </a>\n'
        '</div>'
    )

def patch_old_nav(content):
    return OLD_NAV_RE.sub(
        lambda m: make_card_nav(m.group(1), m.group(2), m.group(3), m.group(4)),
        content
    )

# Update existing card-style labels (capitalise)
def patch_nav_labels(content):
    content = content.replace('← Bài trước', '← BÀI TRƯỚC')
    content = content.replace('← Quay lại Blog', '← TẤT CẢ BÀI VIẾT')
    content = content.replace('Xem tất cả bài viết', 'Tất cả bài viết')
    content = content.replace('Bài tiếp theo →', 'BÀI TIẾP THEO →')
    return content

# ── 3. Process each article (depth = 3, prefix = ../../../) ───────────────
ARTICLES = [
    "blog/phan-tich-phim/nolan-va-thoi-gian/index.html",
    "blog/phan-tich-phim/mau-sac-wes-anderson/index.html",
    "blog/phan-tich-phim/kubrick-anh-sang-tu-nhien/index.html",
    "blog/phan-tich-phim/jordan-peele-spectacle/index.html",
    "blog/ky-thuat/shot-reverse-shot/index.html",
    "blog/bien-kich/tarantino-doi-thoai-pulp-fiction/index.html",
    "blog/bien-kich/viet-phim-kinh-di/index.html",
    "blog/bien-kich/phan-tich-kich-ban-kinh-di/index.html",
]

for rel_path in ARTICLES:
    path = BASE + rel_path
    with open(path) as f:
        c = f.read()

    c = patch_nav_logo(c, "../../../")
    c = patch_unsplash(c, "../../../assets/images/phimvakhoi-thumbnail.svg")
    c = patch_old_nav(c)
    c = patch_nav_labels(c)

    with open(path, "w") as f:
        f.write(c)
    print(f"  ✓ {rel_path}")

# ── 4. Process blog/index.html (depth=1, prefix=../) ─────────────────────
blog_path = BASE + "blog/index.html"
with open(blog_path) as f:
    c = f.read()

c = patch_nav_logo(c, "../")
# In blog listing, sidebar sb-post-img images → SVG
c = patch_unsplash(c, "../assets/images/phimvakhoi-thumbnail.svg")

with open(blog_path, "w") as f:
    f.write(c)
print("  ✓ blog/index.html")

# ── 5. Process root index.html (depth=0, prefix="") ──────────────────────
root_path = BASE + "index.html"
with open(root_path) as f:
    c = f.read()

c = patch_nav_logo(c, "")

with open(root_path, "w") as f:
    f.write(c)
print("  ✓ index.html")

print("\nAll done ✓")
