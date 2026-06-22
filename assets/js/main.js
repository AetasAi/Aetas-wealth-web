
(function () {
'use strict';
const toggle = document.querySelector('.nav-toggle');
const links = document.querySelector('.nav-links');
if (toggle && links) {
toggle.addEventListener('click', function () {
const open = links.classList.toggle('is-open');
toggle.classList.toggle('is-open', open);
toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
});
}
const path = window.location.pathname.replace(/\/$/, '');
document.querySelectorAll('.nav-links a').forEach(function (a) {
const href = a.getAttribute('href') || '';
const cleaned = href.replace(/\/$/, '').replace(/^\.\
if (
(cleaned && (path.endsWith('/' + cleaned) || path.endsWith(cleaned))) ||
(cleaned === 'index.html' && (path === '' || path === '/'))
) {
a.classList.add('is-active');
}
});
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
const yr = document.querySelector('[data-year]');
if (yr) yr.textContent = new Date().getFullYear();
})();
(function () {
'use strict';
var COOKIEBOT_ID = 'f87c63d7-fd2d-4dfd-8854-081181829426';
var GA4_ID = 'G-MXS6JSC1LE';
var CLARITY_ID = 'wtmefby0kh';
var cb = document.createElement('script');
cb.id = 'Cookiebot';
cb.src = 'https://consent.cookiebot.com/uc.js';
cb.setAttribute('data-cbid', COOKIEBOT_ID);
cb.setAttribute('data-blockingmode', 'auto');
cb.type = 'text/javascript';
document.head.appendChild(cb);
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
function loadClarity() {
if (window.__aetasClarityLoaded) return;
window.__aetasClarityLoaded = true;
(function (c, l, a, r, i, t, y) {
c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
t = l.createElement(r); t.async = 1; t.src = 'https://www.clarity.ms/tag/' + i;
y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);
})(window, document, 'clarity', 'script', CLARITY_ID);
}
function maybeLoadTrackers() {
if (window.Cookiebot && window.Cookiebot.consent && window.Cookiebot.consent.statistics) {
loadGA4();
loadClarity();
}
}
window.addEventListener('CookiebotOnLoad', maybeLoadTrackers);
window.addEventListener('CookiebotOnAccept', maybeLoadTrackers);
})();