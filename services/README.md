# Aetas Wealth — website framework

A static-site framework for a new Aetas Wealth website, ready to host on GitHub Pages. Built around two core sections, **Aetas Wealth** (about) and **Individuals** (personal planning), with a supporting Insights/blog area.

Content has been adapted from `aetas-wealth.com/home` and the relevant sections of `aetas-partners.com`, then rewritten into a single, consistent voice (UK English, formal but warm, no em dashes, no jargon).

---

## What's in the box

```
aetas-wealth/
├── index.html                    Home
├── our-approach.html             About / Lifetime to Legacy
├── our-people.html               Team hub
├── individuals.html              Personal Planning hub (9 service cards)
├── businesses.html               Businesses hub
├── business-owners.html          Personal advice for SME owners and directors
├── workplace.html                ITW summary, links to itw.aetaspartners.com
├── fees.html                     How we charge (full Costs &amp; Charges page)
├── contact.html                  Enquiry form & contact details
├── privacy.html                  Privacy &amp; Cookies (bridges to Insight IFA)
├── terms.html                    Terms of Use (bridges to Insight IFA)
├── complaints.html               Complaints procedure
│
├── team/                         Adviser profile pages
│   ├── matthew-steiner.html
│   ├── daniel-cottam.html
│   └── peter-rose.html
│
├── services/                     Nine service pages (one per offering)
│   ├── cash-flow-planning.html
│   ├── director-owner-advisory.html
│   ├── financial-planning.html
│   ├── inheritance-tax.html
│   ├── investment-management.html
│   ├── later-life-planning.html
│   ├── mortgages.html
│   ├── pensions-retirement.html
│   └── protection-planning.html
│
├── insights/                     Blog / insights
│   ├── index.html
│   └── posts/
│       └── sample-post.html
│
├── assets/
│   ├── css/styles.css            Single design-system stylesheet
│   ├── js/main.js                Nav toggle, active link, scroll reveal
│   ├── docs/
│   │   └── aetas-wealth-costs-and-charges.pdf   Linked from /fees.html
│   └── images/                   (Team headshots currently hot-linked from
│                                  aetas-partners.com)
│
├── 404.html                      Custom not-found page
├── robots.txt                    SEO crawler rules
├── sitemap.xml                   XML sitemap
├── .nojekyll                     Tells GitHub Pages to skip Jekyll
├── .gitignore
└── README.md                     This file
```

**Top navigation**: Home · Our approach · Our People · Individuals · Businesses · Fees · Insights · Contact · Book a meeting

**Compliance & legal pages**: privacy.html, terms.html and complaints.html sit at the foot of every page. Privacy and Terms are bridge pages that frame the Aetas Wealth / Insight Financial Associates relationship and link out to the canonical Insight documents (https://www.insightifa.com). Complaints is a self-contained page with the firm's complaints contact details and the FOS escalation route.

---

## Brand and design

The site uses the Aetas brand system end-to-end:

| Token | Hex | Use |
|---|---|---|
| Deep Blue | `#00205B` | Primary, headings, headers |
| Turquoise | `#009CA6` | Accent, hover states, links |
| Gold | `#9A7B3A` | Premium accent, eyebrows, rules |

Typography is **Open Sans** throughout, loaded from Google Fonts. Design hierarchy is built through weight (300 / 400 / 500 / 600 / 700) rather than additional font families.

All design tokens live as CSS custom properties at the top of `assets/css/styles.css`. Edit them once and the change flows through every page.

---

## Local preview

The site is plain HTML, CSS and JavaScript. No build step.

To preview locally:

```bash
# Option 1: open files directly in a browser
open index.html

# Option 2 (recommended): serve over HTTP so all paths resolve correctly
python3 -m http.server 8000
# then open http://localhost:8000

# or with Node:
npx serve .
```

---

## Deploying to GitHub Pages

### One-time setup

1. Create a new GitHub repository (e.g. `aetas-wealth-website`)
2. From your local machine:
   ```bash
   cd aetas-wealth
   git init
   git add .
   git commit -m "Initial site framework"
   git branch -M main
   git remote add origin git@github.com:YOUR-ORG/aetas-wealth-website.git
   git push -u origin main
   ```
3. In the GitHub repo, go to **Settings → Pages**
4. Under "Build and deployment":
   - **Source:** Deploy from a branch
   - **Branch:** `main` / `(root)`
   - Click **Save**
5. After 1–2 minutes the site will be live at `https://YOUR-ORG.github.io/aetas-wealth-website/`

### Custom domain (optional)

To serve from a custom domain such as `aetas-wealth.com` or a sub-domain:

1. Create a file named `CNAME` in the repo root containing only your domain, e.g.:
   ```
   aetas-wealth.com
   ```
2. In your DNS, add records pointing at GitHub Pages:
   - **Apex domain**: four `A` records to `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - **Sub-domain (e.g. www)**: a `CNAME` record pointing to `YOUR-ORG.github.io`
3. In **Settings → Pages**, enter the custom domain and tick "Enforce HTTPS"

### Subsequent updates

```bash
git add .
git commit -m "Edit homepage hero copy"
git push
```

GitHub Pages rebuilds automatically within a minute or two.

---

## Editing the site

### Add a new blog post

1. Copy `insights/posts/sample-post.html` and rename it (e.g. `2026-pension-changes.html`)
2. Update the `<title>`, `<meta description>`, banner, breadcrumbs and article body
3. In `insights/index.html`, copy the existing `<li>` block and update it to point at the new post

### Add a new service page

1. Copy `services/pensions-retirement.html` (fullest example) and rename it
2. Update the `<title>`, banner content, intro paragraphs and the "How we help" list
3. Add a card to `individuals.html` linking to the new page

### Update navigation, header or footer

The header and footer are duplicated across pages (kept simple, no Jekyll/build step required). Each is wrapped in `<!-- SHARED: site-header -->` / `<!-- SHARED: site-footer -->` comments.

If you change the nav links, contact details, or footer copy, search across all `.html` files for `SHARED:` and update each one.

### Wire up the contact form

The contact form in `contact.html` posts to `#`. Replace the `action=` attribute with one of:

- **Formspree**: e.g. `action="https://formspree.io/f/your-form-id"` — same approach used for the ITW diagnostic
- **Netlify Forms**: requires Netlify hosting (not GitHub Pages)
- **GoHighLevel** form embed (since the existing Aetas sites use leadconnector)

---

## Voice and content style

Content has been written in line with house style:

- UK English throughout
- Formal but warm advisory tone
- Approximately Grade 9 reading level
- No em dashes (commas or full stops instead)
- No "Hope you're well" style openers
- No sales-driven language; no jargon
- Measured, senior-adviser voice

Service pages currently contain placeholder body copy in the same voice. Replace where deeper content is needed.

---

## Compliance

Each page that gives any kind of guidance on regulated matters carries a footer disclaimer noting:

- Aetas Wealth is a trading style of Insight Financial Associates Ltd
- FCA registration 458421
- The FCA does not regulate Wills, Trusts or Tax advice
- Standard "value can go down as well as up" wording

The Insights template carries an additional article-level disclaimer.

Before publishing, please review compliance copy with your Insight FA contact to confirm it remains accurate for the firm's current regulatory position.

---

## Browser support

Modern evergreen browsers (Chrome, Edge, Safari, Firefox) on desktop and mobile. The site uses CSS custom properties, CSS grid, `backdrop-filter` and `IntersectionObserver` — all widely supported. There's a `prefers-reduced-motion` fallback for the scroll-reveal effect.

---

## Next steps suggested

1. Replace placeholder copy on the seven shorter service pages with full content
2. Add real headshots and team bios (`our-people.html` page is a natural addition)
3. Wire up the contact form to your preferred handler
4. Add proper Privacy Policy, Terms of Use and Cookies Policy pages and update the footer links
5. Add real OG/Twitter share images per page
6. Configure GitHub Actions if you want a build/lint step in future

---

© Aetas Wealth. Built as a static-site framework, ready for GitHub Pages.
