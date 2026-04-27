/* theme.js — Phim & Khói theme switcher */
(function () {
  var KEY = 'pvk-theme';

  function applyTheme(theme, save) {
    document.documentElement.setAttribute('data-theme', theme);
    if (save) localStorage.setItem(KEY, theme);
    document.querySelectorAll('.theme-btn').forEach(function (btn) {
      btn.classList.toggle('active-theme', btn.dataset.theme === theme);
    });
  }

  /* Áp dụng ngay khi DOM ready (tránh flash) */
  document.addEventListener('DOMContentLoaded', function () {
    var saved = localStorage.getItem(KEY) || 'dark';
    applyTheme(saved, false);
  });

  /* Public API — gọi từ onclick */
  window.setTheme = function (theme) { applyTheme(theme, true); };
})();
