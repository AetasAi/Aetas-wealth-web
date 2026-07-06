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
// ---------- Nav dropdowns ----------
(function() {
  var allItems = Array.from(document.querySelectorAll('.nav-has-dropdown'));

  function closeAll(except) {
    allItems.forEach(function(it) {
      if (it === except) return;
      var d = it.querySelector('.nav-dropdown');
      var t = it.querySelector('.nav-dropdown-toggle');
      if (d) { d.classList.remove('is-open'); d.classList.remove('is-open-mobile'); }
      if (t) { t.setAttribute('aria-expanded', 'false'); }
      if (it._closeTimer) { clearTimeout(it._closeTimer); it._closeTimer = null; }
    });
  }

  allItems.forEach(function(item) {
    var toggle = item.querySelector('.nav-dropdown-toggle');
    var dropdown = item.querySelector('.nav-dropdown');
    if (!toggle || !dropdown) return;
    item._closeTimer = null;

    function openDropdown() {
      closeAll(item);
      if (item._closeTimer) { clearTimeout(item._closeTimer); item._closeTimer = null; }
      dropdown.classList.add('is-open');
      toggle.setAttribute('aria-expanded', 'true');
    }
    function closeDropdown(delay) {
      item._closeTimer = setTimeout(function() {
        dropdown.classList.remove('is-open');
        dropdown.classList.remove('is-open-mobile');
        toggle.setAttribute('aria-expanded', 'false');
      }, delay || 0);
    }

    // Desktop hover
    item.addEventListener('mouseenter', openDropdown);
    item.addEventListener('mouseleave', function() { closeDropdown(400); });
    dropdown.addEventListener('mouseenter', function() {
      if (item._closeTimer) { clearTimeout(item._closeTimer); item._closeTimer = null; }
    });
    dropdown.addEventListener('mouseleave', function() { closeDropdown(400); });

    // Mobile/keyboard: click toggle
    toggle.addEventListener('click', function(e) {
      e.preventDefault();
      var isOpen = dropdown.classList.contains('is-open-mobile');
      closeAll(null);
      if (!isOpen) {
        dropdown.classList.add('is-open-mobile');
        toggle.setAttribute('aria-expanded', 'true');
      }
    });

    // Close on Escape
    item.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') { closeDropdown(0); toggle.focus(); }
    });

    // Close when focus leaves
    item.addEventListener('focusout', function(e) {
      if (!item.contains(e.relatedTarget)) { closeDropdown(100); }
    });
  });

  // Close all on outside click
  document.addEventListener('click', function(e) {
    if (!e.target.closest('.nav-has-dropdown')) { closeAll(null); }
  });
})();
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

/* =====================================================================
   Aetas Wealth — Analytics
   --------------------------------------------------------------------
   Defers GA4 load until first user interaction.
   Cookiebot removed — replaced with first-party cookie notice.
   anonymize_ip: true applied for GDPR best practice.

   GA4 ID: G-MXS6JSC1LE
   Clarity ID: wtmefby0kh
   ===================================================================== */
(function () {
  'use strict';

  var GA4_ID = 'G-MXS6JSC1LE';
  var CLARITY_ID = 'wtmefby0kh';
  var loaded = false;

  function loadAnalytics() {
    if (loaded) return;
    loaded = true;

    // GA4
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA4_ID;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    function gtag() { window.dataLayer.push(arguments); }
    window.gtag = gtag;
    gtag('js', new Date());
    gtag('config', GA4_ID, { anonymize_ip: true });

    // Clarity
    (function(c,l,a,r,i,t,y){
      c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
      t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
      y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    })(window,document,"clarity","script",CLARITY_ID);

    // GHL tracking (interaction-deferred)
    var ghl = document.createElement('script');
    ghl.async = true;
    ghl.src = 'https://link.aetas-wealth.com/js/external-tracking.js';
    ghl.setAttribute('data-tracking-id', 'tk_db86e3fbbdec4a14a52fb3fcfdb0a517');
    document.head.appendChild(ghl);
  }

  ['scroll','click','keydown','touchstart'].forEach(function(evt){
    window.addEventListener(evt, loadAnalytics, { once: true, passive: true });
  });
  setTimeout(loadAnalytics, 8000);
})();
