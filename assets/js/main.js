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
  }

  ['scroll','click','keydown','touchstart'].forEach(function(evt){
    window.addEventListener(evt, loadAnalytics, { once: true, passive: true });
  });
  setTimeout(loadAnalytics, 5000);
})();
