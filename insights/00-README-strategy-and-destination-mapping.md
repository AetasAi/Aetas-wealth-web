# Aetas Wealth Insights — Agentic-Optimised Article HTML Files

**Batch:** 8 articles, sourced from aetas-partners.com blog pages 3–5, rewritten for AI search citation and converted to HTML matching the aetas-wealth.com template.
**Drop into:** `aetas-wealth-web/insights/posts/`

---

## What you have

| File | Purpose |
|---|---|
| `pension-tax-free-lump-sum.html` | Pension PCLS explainer |
| `how-to-prepare-for-retirement.html` | 10/5/1-year retirement guide |
| `tax-efficient-giving.html` | Gift Aid, payroll giving, legacy gifts |
| `cash-flow-planning.html` | Cash flow planning explainer |
| `estate-planning-for-everyone.html` | Estate planning for non-wealthy |
| `salary-sacrifice-cap.html` | 2029 NI cap on salary sacrifice |
| `cash-isa-changes-2027.html` | Cash ISA cut from April 2027 |
| `pension-iht-2027.html` | Pensions joining IHT net April 2027 |

Each file matches the existing template exactly:
- Same `<head>` font + CSS imports + favicon links
- Same site-header navigation
- Same breadcrumb + page-banner pattern
- Same `<article class="prose">` content wrapper
- Same disclaimer block + CTA section styling
- Same site-footer with full nav

---

## ⚠️ Collision check — read this before copying

The existing `posts` folder already contains files at some of these slugs and adjacent topics. Decide what to do before overwriting.

| New file | Existing file | Recommendation |
|---|---|---|
| `cash-flow-planning.html` | `cash-flow-planning.html` (existing) | **Overwrite** — same topic, the new version is the expanded agentic-optimised one |
| `pension-iht-2027.html` | `how-pensions-are-taxed-after-death.html` | Topic overlap. Consider: keep both (different angles) OR redirect the old one to the new |
| `pension-iht-2027.html` | `family-wealth-transfer-2027.html` | Topic overlap. Likely keep both — `family-wealth-transfer-2027` is broader |
| `estate-planning-for-everyone.html` | `inheritance-tax-rising.html` | Different — keep both |
| `cash-isa-changes-2027.html` | `isa-investment-strategy-2026.html` | Different angle — keep both |
| `pension-tax-free-lump-sum.html` | `drawing-your-pension-differently-after-...html` | Possible overlap, depends on what the existing one covers — review |
| `salary-sacrifice-cap.html` | `pension-changes-ahead.html`, `pension-schemes-act-2026.html` | Topic-adjacent; sit alongside |
| `how-to-prepare-for-retirement.html` | (none obvious) | New |
| `tax-efficient-giving.html` | (none obvious) | New |

If you overwrite `cash-flow-planning.html`, the existing URL stays valid — internal links and any external backlinks continue to work, just point to the better content.

---

## What's different about these articles

These have been rewritten for **agentic / AI-search optimisation** (Generative Engine Optimisation / GEO), which is the practice of structuring content so AI assistants — ChatGPT, Claude, Perplexity, Gemini, Google AI Overviews — confidently cite it when users ask financial planning questions.

Every article now includes:

1. **TL;DR box** at the top — direct 2–3 sentence answer LLMs lift wholesale
2. **Question-format H1 and H2 headings** matching real user queries
3. **At-a-glance comparison tables** — LLMs prefer extractable structured data
4. **FAQ block with `<details>` elements** — accessible AND feeds FAQPage schema
5. **Triple JSON-LD schema** in `<head>`:
   - `Article` schema with author, dates, publisher
   - `BreadcrumbList` schema
   - `FAQPage` schema — the single biggest AI citation lever
6. **Specific numbers, dates, and sourced facts** — no vague hedging
7. **Authoritative external links** — gov.uk, HMRC, MoneyHelper
8. **Cross-links** between the 8 articles, building a topic cluster

The schema and FAQ structure mean these articles are also eligible for Google rich results (FAQ rich snippets, breadcrumb display) — useful regardless of AI search.

---

## Posting cadence

Recommend one per week for the first 8 weeks. Lead with the highest-search-volume pieces:

1. `pension-iht-2027.html` — high volume, urgent
2. `cash-isa-changes-2027.html` — high volume, current news cycle
3. `salary-sacrifice-cap.html` — directly tied to recent Budget
4. `pension-tax-free-lump-sum.html` — perennial high search
5. `how-to-prepare-for-retirement.html` — perennial high search
6. `cash-flow-planning.html` — replaces existing
7. `estate-planning-for-everyone.html` — broad audience
8. `tax-efficient-giving.html` — niche but valuable

This order also lets the more time-sensitive Budget-related pieces hit while the news interest is highest.

---

## After publishing each article

1. **Add to the Insights index page** (`insights-index.html`) with a card or list entry
2. **Update any "related articles" sections** on existing posts where these new articles fit
3. **Submit URL to Google Search Console** for faster indexing
4. **Spot-check AI citation** monthly — ask ChatGPT, Claude, Perplexity questions matching the article topics and note whether Aetas Wealth appears in the citations
5. **Apply the same structure to future articles** — the agentic optimisation framework here is reusable

---

## Adapting for ITW, Charity Wellbeing, LinkedIn, Medium

These HTML files are the **canonical Aetas Wealth versions**. To adapt for other destinations:

- **ITW (Aetas in the Workplace)** subdomain: Best fits are `how-to-prepare-for-retirement`, `cash-flow-planning`, `salary-sacrifice-cap`, `cash-isa-changes-2027`. Reframe intro to address employees/HR, swap CTA to workplace booking link.
- **Charity Wellbeing** subdomain: Strongest fit is `tax-efficient-giving`. Also `how-to-prepare-for-retirement`, `cash-flow-planning`, `estate-planning-for-everyone` work for charity staff financial wellbeing.
- **Medium / LinkedIn syndication**: Wait 7–14 days after publishing on Aetas Wealth, then add a "Originally published on aetas-wealth.com" line at the top. Soften the CTA. LinkedIn: post from author's personal profile (Matthew Steiner / Daniel Cottam) for 3–5x reach.

---

## Files in this set

```
aetas-wealth-web/insights/
├── 00-README-strategy-and-destination-mapping.md   ← this file (internal ref, never publish)
└── posts/
    ├── pension-tax-free-lump-sum.html              ← publish
    ├── how-to-prepare-for-retirement.html          ← publish
    ├── tax-efficient-giving.html                   ← publish
    ├── cash-flow-planning.html                     ← OVERWRITES existing
    ├── estate-planning-for-everyone.html           ← publish
    ├── salary-sacrifice-cap.html                   ← publish
    ├── cash-isa-changes-2027.html                  ← publish
    └── pension-iht-2027.html                       ← publish
```

You can now delete the original `.md` files (01–08) from the posts folder — they were intermediate working files; the `.html` files are the final deliverables.

---

*Updated 22 May 2026 — HTML conversion complete.*
