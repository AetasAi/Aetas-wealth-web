/* ============================================================
   Aetas Wealth €” Site interactions
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


/* =====================================================================
   Aetas Wealth €” Analytics & Cookie Consent
   --------------------------------------------------------------------
   Loads Cookiebot first (shows consent banner). Only loads GA4 and
   Microsoft Clarity AFTER the visitor accepts the "statistics" category.

   IDs:
     Cookiebot: f87c63d7-fd2d-4dfd-8854-081181829426
     GA4:       G-MXS6JSC1LE
     Clarity:   wtmefby0kh

   To change any ID later, edit the three constants below.
   ===================================================================== */
(function () {
  'use strict';

  var COOKIEBOT_ID = 'f87c63d7-fd2d-4dfd-8854-081181829426';
  var GA4_ID = 'G-MXS6JSC1LE';
  var CLARITY_ID = 'wtmefby0kh';

  // --- Step 1: inject Cookiebot consent banner script -----------------
  var cb = document.createElement('script');
  cb.id = 'Cookiebot';
  cb.src = 'https://consent.cookiebot.com/uc.js';
  cb.setAttribute('data-cbid', COOKIEBOT_ID);
  cb.setAttribute('data-blockingmode', 'auto');
  cb.type = 'text/javascript';
  document.head.appendChild(cb);

  // --- Step 2: define GA4 loader (only called after consent) ----------
  function loadGA4() {
    if (window.__aetasGA4Loaded) return;
    window.__aetasGA4Loaded = true;

    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA4_ID;
    document.head.appendChild(s);

    window.dataLayer = window.dataLayer || [];
    function gtag() { window.dataLayer.push(arguments); }
    window.gtag = gtag;
    gtag('js', new Date());
    gtag('config', GA4_ID, { anonymize_ip: true });
  }

  // --- Step 3: define Clarity loader (only called after consent) ------
  function loadClarity() {
    if (window.__aetasClarityLoaded) return;
    window.__aetasClarityLoaded = true;

    (function (c, l, a, r, i, t, y) {
      c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
      t = l.createElement(r); t.async = 1; t.src = 'https://www.clarity.ms/tag/' + i;
      y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);
    })(window, document, 'clarity', 'script', CLARITY_ID);
  }

  // --- Step 4: load trackers only when "statistics" consent is given --
  function maybeLoadTrackers() {
    if (window.Cookiebot && window.Cookiebot.consent && window.Cookiebot.consent.statistics) {
      loadGA4();
      loadClarity();
    }
  }

  // Fires after Cookiebot loads with an existing valid consent cookie
  window.addEventListener('CookiebotOnLoad', maybeLoadTrackers);

  // Fires when the user clicks Accept on the banner
  window.addEventListener('CookiebotOnAccept', maybeLoadTrackers);
})();

