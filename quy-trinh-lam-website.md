# Quy trình làm Static Website — Bài học từ Phim & Khói

> Tài liệu này tổng hợp toàn bộ quy trình và bẫy thường gặp khi xây dựng website tĩnh (HTML + CSS + JS thuần) có hỗ trợ dark/light theme, deploy lên Netlify. Dùng lại cho các dự án tương tự để tiết kiệm thời gian.

---

## 1. Cấu trúc thư mục chuẩn

```
project/
├── index.html               ← Trang chủ
├── _redirects               ← Netlify redirects (ẩn /index.html khỏi URL)
├── assets/
│   ├── css/
│   │   └── style.css        ← CSS toàn cục (theme, nav, footer, components)
│   ├── js/
│   │   └── theme.js         ← Script chuyển theme (không inline trong HTML)
│   └── images/
├── blog/
│   ├── index.html           ← Trang danh sách blog
│   └── [danh-muc]/
│       └── [ten-bai]/
│           └── index.html   ← URL sạch: /blog/danh-muc/ten-bai/
├── khoahoc/
│   └── index.html
├── truc-tiep/
│   └── index.html
└── ve-toi.html
```

**Lưu ý URL:** Mỗi trang là một thư mục chứa `index.html` → URL hiển thị `/blog/ten-bai/` thay vì `/blog/ten-bai/index.html`.

---

## 2. Netlify Setup

### File `_redirects` (đặt ở thư mục gốc)
```
/index.html                    /                              301
/blog/index.html               /blog/                         301
/khoahoc/index.html            /khoahoc/                      301
/truc-tiep/index.html          /truc-tiep/                    301
# Thêm một dòng cho mỗi trang/thư mục con
```

Deploy bằng Netlify Drop (kéo thả thư mục) hoặc kết nối GitHub repo.

---

## 3. Hệ thống CSS Variables & Dark/Light Theme

### 3.1. Khai báo biến màu

```css
/* ── DARK THEME (mặc định) ── */
:root {
  --bg:        #141a13;   /* nền chính */
  --bg-deep:   #0d1109;   /* nền đậm hơn (nav, footer, hero) */
  --bg-card:   #1a2118;   /* nền card */
  --bg-hover:  #1e2a1a;
  --border:    #2a3828;
  --forest:    #628141;   /* màu chủ đạo (accent) */
  --sage:      #7a9e5e;   /* màu phụ */
  --beige:     #c8bfa8;   /* màu chữ sáng */
  --text:      #b5b0a0;   /* chữ thường */
  --text-dim:  #7a8270;   /* chữ mờ */
  --text-faint:#445040;   /* chữ rất mờ */
}

/* ── LIGHT THEME ── */
html[data-theme="light"] {   /* ← PHẢI dùng html[...] không phải [data-theme] */
  --bg:        #F8F4EE;   /* kem */
  --bg-deep:   #2D3C59;   /* navy (dùng cho hero, nav, footer) */
  --bg-card:   #FFFFFF;   /* trắng */
  --bg-hover:  #f0ebe0;
  --border:    #ddd5c8;
  --forest:    #E5BA41;   /* amber */
  --sage:      #94A378;   /* sage xanh */
  --beige:     #2D3C59;   /* navy (chú ý: đây là màu CHỮ trên nền sáng) */
  --text:      #3a3228;
  --text-dim:  #7a6e60;
  --text-faint:#aaa090;
}
```

### 3.2. ⚠️ BẪY SPECIFICITY QUAN TRỌNG NHẤT

**Vấn đề:** Nếu trang có inline `<style>` trong `<head>` (như các trang Phim & Khói), selector `[data-theme="light"]` có specificity `(0,1,0)` — **bằng** với `:root` bên trong inline `<style>`. Khi bằng nhau, inline style thắng vì nằm gần hơn trong cascade.

**Giải pháp:** Luôn dùng `html[data-theme="light"]` (specificity `0,1,1`) thay vì `[data-theme="light"]`:

```css
/* ❌ SAI — có thể bị inline <style> override */
[data-theme="light"] .nav { ... }

/* ✅ ĐÚNG — specificity cao hơn, luôn thắng */
html[data-theme="light"] .nav { ... }
```

---

## 4. Implement Dark/Light Theme

### 4.1. Anti-FOUC (chống nháy màu khi load trang)

Đặt đoạn này là **thẻ đầu tiên** trong `<head>`, trước mọi CSS:

```html
<script>
  (function(){
    var t = localStorage.getItem('pvk-theme');
    if(t) document.documentElement.setAttribute('data-theme', t);
  })();
</script>
```

Nếu không có script này, trang luôn hiện dark mode một thoáng trước khi chuyển sang light → người dùng thấy nháy.

### 4.2. File `assets/js/theme.js`

```javascript
(function () {
  var KEY = 'pvk-theme';

  function applyTheme(theme, save) {
    document.documentElement.setAttribute('data-theme', theme);
    if (save) localStorage.setItem(KEY, theme);
    document.querySelectorAll('.theme-btn').forEach(function (btn) {
      btn.classList.toggle('active-theme', btn.dataset.theme === theme);
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    var saved = localStorage.getItem(KEY) || 'dark';
    applyTheme(saved, false);
  });

  window.setTheme = function (theme) { applyTheme(theme, true); };
})();
```

### 4.3. HTML cho nút chuyển theme (trong footer)

```html
<div class="theme-toggle">
  <span class="theme-toggle-label">GIAO DIỆN</span>
  <button class="theme-btn theme-btn-dark"
          data-theme="dark"
          onclick="setTheme('dark')"
          title="Tối" aria-label="Chế độ tối"></button>
  <button class="theme-btn theme-btn-light"
          data-theme="light"
          onclick="setTheme('light')"
          title="Sáng" aria-label="Chế độ sáng"></button>
</div>
```

---

## 5. Bẫy Màu Sắc Thường Gặp (và cách phòng tránh)

### 5.1. Navy-on-Navy (lỗi phổ biến nhất)

Trong light theme, `--bg-deep` = navy `#2D3C59` và `--beige` = cũng navy `#2D3C59`.

Bất kỳ element nào có cả hai thuộc tính này sẽ bị tàng hình:

```css
/* Ví dụ bẫy: */
.sidebar-widget-title {
  background: var(--bg-deep);  /* navy */
  color: var(--beige);         /* cũng navy trong light mode → tàng hình! */
}

/* Fix: ghi đè riêng trong light theme */
html[data-theme="light"] .sidebar-widget-title {
  background: #2D3C59;    /* giữ navy */
  color: #F8F4EE !important; /* cream để đọc được */
}
```

**Checklist nhanh:** Tìm mọi element có `background: var(--bg-deep)` — kiểm tra màu chữ trong light mode.

### 5.2. Cream-on-White

Khi ghi đè màu chữ thành cream (`#F8F4EE` hoặc `rgba(248,244,238,...)`) để hiển thị trên nền navy, nhưng element đó thực ra nằm trên card trắng → tàng hình.

```css
/* Ví dụ bẫy: section testimonials có nền navy,
   nhưng card bên trong có nền trắng */
.tt-testimonials { background: var(--bg-deep); } /* navy */
.tt-testi-card   { background: var(--bg-card);  } /* trắng! */

/* ❌ Sai: cream text trên card trắng = tàng hình */
html[data-theme="light"] .tt-testi-quote { color: rgba(248,244,238,.88); }

/* ✅ Đúng: phân biệt section vs card */
html[data-theme="light"] .tt-testimonials h2 { color: #F8F4EE; }  /* section title → cream */
html[data-theme="light"] .tt-testi-quote { color: #3a3228 !important; }  /* card text → tối */
```

### 5.3. Hardcoded Colors Không Theo Theme

Màu viết cứng trong CSS (không dùng variable) sẽ **không thay đổi** khi chuyển theme:

```css
/* Ví dụ trong file gốc */
.prose ul li { color: #b0a890; }  /* hardcoded → luôn màu này dù dark/light */

/* Fix: ghi đè trong light theme */
html[data-theme="light"] .prose ul li { color: #3a3228 !important; }
```

**Checklist:** Tìm trong CSS bằng regex `color: #[0-9a-f]{3,6}` — mọi màu hardcoded đều là ứng viên cần kiểm tra.

### 5.4. Cùng Class, Khác Context

Một class dùng ở nhiều nơi với nền khác nhau cần được style theo parent:

```css
/* about-badge xuất hiện ở hero (navy) và sidebar card (trắng) */

/* ✅ Style theo context */
html[data-theme="light"] .about-hero .about-badge {
  color: rgba(248,244,238,.78); /* cream → hiển thị trên navy */
}
html[data-theme="light"] .sb-about-block .about-badge {
  color: #5a5040; /* tối → hiển thị trên trắng */
}
```

### 5.5. Rule Trùng Lặp — Rule Sau Thắng

Nếu cùng selector xuất hiện nhiều lần trong CSS, rule **sau cùng** thắng (kể cả khi rule trước có `!important` nhưng cùng specificity):

```css
/* Dòng 1049 */
html[data-theme="light"] .tt-testi-quote { color: #3a3228; }

/* Dòng 1124 — THẮNG vì sau hơn + có !important */
html[data-theme="light"] .tt-testi-quote { color: rgba(248,244,238,.88) !important; }
```

**Thói quen tốt:** Dùng `grep` để kiểm tra trùng lặp trước khi thêm rule mới.

---

## 6. Quy trình Viết Light Theme CSS

### Bước 1: Lập danh sách "nền navy"

Tìm mọi class có `background: var(--bg-deep)` hoặc `background: var(--bg-card)`:

```bash
grep -n "background: var(--bg" assets/css/style.css
```

Với mỗi class:
- Nền navy → chữ phải cream/sáng
- Nền trắng/kem → chữ phải tối

### Bước 2: Template override cho section navy

```css
html[data-theme="light"] .ten-section { background: #2D3C59; }
html[data-theme="light"] .ten-section h2 { color: #F8F4EE !important; }
html[data-theme="light"] .ten-section p  { color: rgba(248,244,238,.78) !important; }
```

### Bước 3: Template override cho card trắng

```css
html[data-theme="light"] .ten-card { background: #FFFFFF; border-color: #ddd5c8; }
html[data-theme="light"] .ten-card h3 { color: #2D3C59 !important; }
html[data-theme="light"] .ten-card p  { color: #3a3228 !important; }
html[data-theme="light"] .ten-card .meta { color: #9a9080 !important; }
```

### Bước 4: Kiểm tra inline `<style>` trong từng trang

Mỗi trang con (truc-tiep, khoahoc, ve-toi) có thể có inline `<style>` riêng với màu hardcoded. Cần kiểm tra từng trang.

---

## 7. Footer Thống Nhất (copy nguyên cho mọi trang)

```html
<footer>
  <div class="footer-inner">
    <div class="f-top">
      <!-- Logo + mô tả + links -->
    </div>
  </div>
  <div class="footer-bottom">
    <div class="f-copy">© 2026 Tên Website · Tác giả</div>
    <div class="footer-bottom-right">
      <div class="theme-toggle">
        <span class="theme-toggle-label">GIAO DIỆN</span>
        <button class="theme-btn theme-btn-dark" data-theme="dark"
                onclick="setTheme('dark')" title="Tối" aria-label="Chế độ tối"></button>
        <button class="theme-btn theme-btn-light" data-theme="light"
                onclick="setTheme('light')" title="Sáng" aria-label="Chế độ sáng"></button>
      </div>
      <div class="f-social">
        <!-- SVG icons -->
      </div>
    </div>
  </div>
</footer>
<script src="/assets/js/theme.js"></script>
```

**Lưu ý path:** Trang trong thư mục con (vd `/blog/ten-bai/`) phải dùng đường dẫn tuyệt đối (`/assets/js/theme.js`) không phải tương đối (`../../assets/js/theme.js`) để tránh lỗi khi URL thay đổi.

---

## 8. Checklist Trước Khi Deploy

### CSS & Theme
- [ ] Tất cả selector light theme dùng `html[data-theme="light"]` (không phải `[data-theme="light"]`)
- [ ] Anti-FOUC script là thẻ đầu tiên trong `<head>` của **mọi trang**
- [ ] `<script src="/assets/js/theme.js"></script>` ở cuối `<body>` của **mọi trang**
- [ ] Không có selector dark/light bị trùng lặp gây conflict

### Màu sắc Light Theme
- [ ] Mọi element nền navy (`--bg-deep`) → chữ cream
- [ ] Mọi element nền trắng (`--bg-card`) → chữ tối
- [ ] Nút `filter-btn` có background riêng (cream/trắng, không phải navy)
- [ ] Sidebar article: `.sidebar-widget-title` có cream text trên navy bg
- [ ] Card testimonial/review: text tối (không phải cream)
- [ ] Badge dùng nhiều context: style theo parent selector

### Cấu trúc
- [ ] Mọi trang nằm trong thư mục riêng (`/ten-trang/index.html`)
- [ ] File `_redirects` có đủ redirect cho mọi trang
- [ ] Footer giống nhau trên tất cả các trang
- [ ] Favicon, meta tags (title, description, og:image) đầy đủ

### Performance
- [ ] Ảnh dùng `loading="lazy"` cho ảnh dưới fold
- [ ] Font Google được preconnect: `<link rel="preconnect" href="https://fonts.googleapis.com">`

---

## 9. Bảng Màu Vintage Cinema (Phim & Khói)

| Tên | Hex | Dùng cho |
|-----|-----|----------|
| Navy | `#2D3C59` | Nền hero/nav/footer (light), màu chữ tiêu đề (light) |
| Cream | `#F8F4EE` | Nền trang chính (light), chữ trên nền navy |
| Amber | `#E5BA41` | Accent, underline active, hover |
| Sage | `#94A378` | Link phụ, badge, icon |
| Terracotta | `#D1855C` | Hover link, highlight |
| Dark brown | `#3a3228` | Chữ thường (light) |
| Medium brown | `#7a6e60` | Chữ mờ (light) |
| Light brown | `#aaa090` | Chữ rất mờ, metadata (light) |

---

## 10. Debug Nhanh Khi Có Lỗi Màu

```bash
# 1. Tìm mọi chỗ dùng class bị lỗi
grep -n "ten-class" assets/css/style.css

# 2. Kiểm tra có rule trùng không
grep -n "data-theme.*ten-class\|ten-class.*data-theme" assets/css/style.css

# 3. Tìm hardcoded colors cần override
grep -n "color: #" assets/css/style.css | grep -v "data-theme"

# 4. Kiểm tra background nào dùng var(--bg-deep)
grep -n "background: var(--bg" assets/css/style.css
```

**Khi thấy chữ tàng hình:**
1. Inspect element → xem `computed` color và background
2. Nếu cả hai đều là `#2D3C59` → navy-on-navy → fix text thành `#F8F4EE`
3. Nếu text là `rgba(248,244,238,...)` nhưng background là `#fff` → cream-on-white → fix text thành `#3a3228`
4. Kiểm tra có rule nào sau đó override không (grep tên class)
