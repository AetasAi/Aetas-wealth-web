/* ============================================================
   Aetas Wealth — Site interactions
   Mobile nav toggle, active link, scroll reveal
   ============================================================ */

(function () {
  'use strict';

  // ---------- Mobile nav toggle ----------
  const toggle = document.querySelector('.nav-toggle');
  const links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      const open = links.classList.toggle('is-open');
      toggle.classList.toggle('is-open', open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // ---------- Highlight active nav link ----------
  const path = window.location.pathname.replace(/\/$/, '');
  document.querySelectorAll('.nav-links a').forEach(function (a) {
    const href = a.getAttribute('href') || '';
    const cleaned = href.replace(/\/$/, '').replace(/^\.\//, '');
    if (
      (cleaned && (path.endsWith('/' + cleaned) || path.endsWith(cleaned))) ||
      (cleaned === 'index.html' && (path === '' || path === '/'))
    ) {
      a.classList.add('is-active');
    }
  });

  // ---------- Scroll reveal ----------
  if ('IntersectionObserver' in window) {
    const obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

    document.querySelectorAll('.reveal').forEach(function (el) { obs.observe(el); });
  } else {
    document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('is-visible'); });
  }

  // ---------- Year in footer ----------
  const yr = document.querySelector('[data-year]');
  if (yr) yr.textContent = new Date().getFullYear();
})();
