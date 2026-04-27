/* ── NAV: Hamburger + Auto-hide + Search ── */
(function () {

  /* ── 1. Hamburger toggle ── */
  var btn   = document.getElementById('navHamburger');
  var links = document.querySelector('.nav-links');

  if (btn && links) {
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = links.classList.toggle('open');
      btn.classList.toggle('open', open);
      btn.setAttribute('aria-expanded', String(open));
    });

    links.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        links.classList.remove('open');
        btn.classList.remove('open');
        btn.setAttribute('aria-expanded', 'false');
      });
    });

    document.addEventListener('click', function (e) {
      if (!btn.contains(e.target) && !links.contains(e.target)) {
        links.classList.remove('open');
        btn.classList.remove('open');
        btn.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* ── 2. Auto-hide nav on scroll ── */
  var nav       = document.querySelector('.nav');
  var lastY     = 0;
  var threshold = 80;

  if (nav) {
    window.addEventListener('scroll', function () {
      var currentY = window.scrollY;
      if (currentY > threshold && currentY > lastY) {
        nav.classList.add('nav--hidden');
        if (links) {
          links.classList.remove('open');
          if (btn) { btn.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); }
        }
        // Đóng search dropdown
        var dd = document.querySelector('.search-dropdown');
        if (dd) dd.classList.remove('open');
      } else {
        nav.classList.remove('nav--hidden');
      }
      lastY = currentY;
    }, { passive: true });
  }

  /* ── 3. Search thật ── */
  var searchInput = document.querySelector('.nav-search');
  var searchWrap  = document.querySelector('.nav-search-wrap');

  if (!searchInput || !searchWrap) return;

  // Tạo dropdown
  var dropdown = document.createElement('div');
  dropdown.className = 'search-dropdown';
  searchWrap.appendChild(dropdown);

  // Lấy dữ liệu bài viết (từ articles.js)
  var articles = window.PHIM_ARTICLES || [];

  function highlight(text, query) {
    if (!query) return text;
    var re = new RegExp('(' + query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi');
    return text.replace(re, '<mark style="background:var(--forest);color:var(--beige);border-radius:2px;padding:0 2px;">$1</mark>');
  }

  function doSearch(query) {
    query = query.trim();
    dropdown.innerHTML = '';

    if (query.length < 2) {
      dropdown.classList.remove('open');
      return;
    }

    var q = query.toLowerCase();
    var results = articles.filter(function (a) {
      return a.title.toLowerCase().indexOf(q) >= 0 ||
             a.category.toLowerCase().indexOf(q) >= 0 ||
             a.desc.toLowerCase().indexOf(q) >= 0;
    });

    if (results.length === 0) {
      dropdown.innerHTML = '<div class="search-no-result">Không tìm thấy bài viết nào cho "<strong>' + query + '</strong>"</div>';
    } else {
      results.forEach(function (a) {
        var item = document.createElement('a');
        item.className = 'search-result-item';
        item.href = a.url;
        item.innerHTML =
          '<span class="search-result-cat">' + a.category + '</span>' +
          '<span class="search-result-title">' + highlight(a.title, query) + '</span>' +
          '<span class="search-result-desc">' + a.desc + '</span>';
        dropdown.appendChild(item);
      });
    }

    dropdown.classList.add('open');
  }

  // Lắng nghe input
  searchInput.addEventListener('input', function () {
    doSearch(this.value);
  });

  searchInput.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      dropdown.classList.remove('open');
      searchInput.blur();
    }
    if (e.key === 'Enter' && dropdown.querySelector('.search-result-item')) {
      window.location.href = dropdown.querySelector('.search-result-item').href;
    }
  });

  // Đóng khi click ra ngoài
  document.addEventListener('click', function (e) {
    if (!searchWrap.contains(e.target)) {
      dropdown.classList.remove('open');
    }
  });

  // Mở lại dropdown khi focus nếu có text
  searchInput.addEventListener('focus', function () {
    if (this.value.length >= 2) doSearch(this.value);
  });

})();
