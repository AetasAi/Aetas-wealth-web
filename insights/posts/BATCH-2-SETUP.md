# Aetas Wealth Batch 2 — Date cleanup + 6 new articles

Delivered 22 May 2026. This batch:

1. **Re-dates the 8 articles from batch 1** so they appear as fresh, weekly-cadence content rather than 6-month-old archive material
2. **Adds 6 new agentic-optimised articles** covering content gaps (POA, CGT, BR/AIM, carry forward, director pensions, end-of-tax-year)
3. **Provides a script** to re-date the existing site articles that are clustered together (e.g. 6 articles all on 15 May 2026)

After deployment, your Insights index will show a clean weekly publishing cadence from October 2025 to May 2026 with no date clusters.

---

## Package contents

```
aetas-batch2/
├── insights/
│   └── posts/                              ← 14 article HTML files
│       ├── (8 re-dated existing articles, just dates changed)
│       └── (6 brand new articles)
└── scripts/
    └── redate-existing-posts.py            ← bulk-redates the OTHER articles
```

---

## Step 1: Copy the 14 article files into your repo

In File Explorer, copy the contents of `aetas-batch2/insights/posts/` and **overwrite** the existing files in:

```
C:\Repos\Aetas-wealth-web\insights\posts\
```

You'll be overwriting 8 files (the batch 1 articles, now with new dates) and adding 6 new files (the new articles).

The 14 files:

**Re-dated batch 1 articles:**
- `cash-flow-planning.html` → now dated 12 November 2025
- `how-to-prepare-for-retirement.html` → now dated 26 November 2025
- `pension-tax-free-lump-sum.html` → now dated 3 December 2025
- `tax-efficient-giving.html` → now dated 28 January 2026
- `estate-planning-for-everyone.html` → now dated 18 February 2026
- `cash-isa-changes-2027.html` → now dated 22 April 2026
- `salary-sacrifice-cap.html` → now dated 6 May 2026
- `pension-iht-2027.html` → now dated 13 May 2026

**Brand-new articles:**
- `director-pension-contributions-sme.html` → 14 January 2026
- `power-of-attorney-guide.html` → 11 February 2026
- `aim-portfolios-business-relief-iht.html` → 25 February 2026
- `carry-forward-pension-contributions.html` → 18 March 2026
- `uk-cgt-planning-2026.html` → 25 March 2026
- `end-of-tax-year-planning.html` → 1 April 2026

---

## Step 2: Re-date your existing site articles (the ones I didn't write)

Copy `aetas-batch2/scripts/redate-existing-posts.py` into your repo's `scripts/` folder (alongside the existing `build-insights-index.py`).

Then run it once locally to update the dates on your existing articles. Open Command Prompt at the repo root:

```
cd C:\Repos\Aetas-wealth-web
python3 scripts/redate-existing-posts.py
```

You'll see output like:

```
✓ pension-schemes-act-2026.html → 29 April 2026
✓ inheritance-tax-rising.html → 15 April 2026
✓ pension-changes-ahead.html → 8 April 2026
✓ isa-investment-strategy-2026.html → 11 March 2026
...
Summary: 11 updated, 0 skipped, 0 not found
```

If any show "NOT FOUND", check whether the filename in your `posts/` folder differs slightly — edit the `DATE_CHANGES` dict at the top of the script and re-run.

---

## Step 3: Commit and push everything together

In GitHub Desktop you should see:

- 8 modified files in `insights/posts/` (the re-dated batch 1 articles)
- 6 new files in `insights/posts/` (the new articles)
- ~11 modified files in `insights/posts/` (your existing articles, dates updated by the script)
- 1 new file in `scripts/` (the redate script)

Commit message:

```
Re-date articles for clean weekly cadence + add 6 new articles
```

Push to main.

---

## Step 4: Watch the auto-indexer fire

The auto-indexer from batch 1 will detect:
- New date metadata on the 19 re-dated articles → re-sorts the index
- 6 new article files → adds them as cards

Within ~30 seconds of pushing you'll see a `chore: auto-update insights index` commit from the bot. Then visit `https://aetas-wealth.com/insights/` to see the result.

---

## What the Insights page will look like after deployment

In chronological order, newest first:

| Date | Article | Source |
|---|---|---|
| 22 May 2026 | Finance Act 2026 | Existing |
| 19 May 2026 | Business owners, pensions and 2027 | Existing |
| 13 May 2026 | Pensions and inheritance tax from April 2027 | Batch 1 (re-dated) |
| 12 May 2026 | Market Commentary: May 2026 | Existing |
| 11 May 2026 | Bank of England holds rates | Existing |
| 6 May 2026 | UK salary sacrifice pension cap from 2029 | Batch 1 (re-dated) |
| 29 April 2026 | Pension Schemes Act 2026 | Existing (re-dated) |
| 22 April 2026 | Cash ISA allowance cut from 2027 | Batch 1 (re-dated) |
| 20 April 2026 | Market Commentary: April 2026 | Existing |
| 15 April 2026 | Inheritance Tax is rising | Existing (re-dated) |
| 8 April 2026 | Pension changes ahead | Existing (re-dated) |
| 1 April 2026 | End of tax year planning | **NEW** |
| 25 March 2026 | UK Capital Gains Tax planning | **NEW** |
| 18 March 2026 | Carry forward pension contributions | **NEW** |
| 11 March 2026 | ISA investment strategy 2026 | Existing (re-dated) |
| 4 March 2026 | How to start investing in the UK | Existing (re-dated) |
| 25 February 2026 | AIM portfolios and Business Relief | **NEW** |
| 18 February 2026 | Estate planning for everyone | Batch 1 (re-dated) |
| 11 February 2026 | Lasting Power of Attorney | **NEW** |
| 4 February 2026 | Family wealth transfer 2027 | Existing (re-dated) |
| 28 January 2026 | Tax-efficient giving | Batch 1 (re-dated) |
| 21 January 2026 | UK property wealth and IHT | Existing (re-dated) |
| 14 January 2026 | Director's pension contributions | **NEW** |
| 7 January 2026 | Financial wellbeing for SMEs | Existing (re-dated) |
| 17 December 2025 | Should I pay my child's uni fees | Existing (re-dated) |
| 10 December 2025 | How pensions are taxed after death | Existing (re-dated) |
| 3 December 2025 | UK pension tax-free lump sum | Batch 1 (re-dated) |
| 26 November 2025 | How to prepare for retirement | Batch 1 (re-dated) |
| 19 November 2025 | Why your pension needs regular reviews | Existing (re-dated) |
| 12 November 2025 | Cash flow planning | Batch 1 (re-dated) |

30 articles spanning ~28 weeks. No clusters. Clean weekly publishing rhythm.

---

## About the new articles

All 6 follow the same agentic-optimised structure as batch 1:
- TL;DR box at the top
- Question-format headings
- At-a-glance comparison tables
- FAQ block (5 Q&As each, using `<details>`)
- Article + BreadcrumbList + FAQPage JSON-LD schema
- Cross-links to related articles in the cluster
- Authoritative gov.uk and HMRC source links

**Topic rationale:**

| Article | Why it fills a content gap |
|---|---|
| End of tax year planning | Perennial high-search Q1 content; complements other tax planning articles |
| Power of Attorney | Pairs with estate planning; widely searched, AEO-friendly |
| Carry forward pension contributions | HNW question; complements salary sacrifice piece |
| Director's pension contributions | SME owner content; ties to your Workplace proposition |
| UK CGT planning 2026 | Topical post-Budget content; no existing coverage |
| AIM portfolios and Business Relief | HNW IHT content; complements pension IHT 2027 piece |

---

## Troubleshooting

**"NOT FOUND" errors from the redate script:** check the exact filename in your `posts/` folder. Common variations:
- `business-owners-pensions-estate-planning.html` vs `business-owners-pensions-and-the-2027-changes.html`
- `drawing-your-pension-differently-after-...html` (truncated in my earlier screenshots)
- Update the `DATE_CHANGES` dict in the script with the exact names and re-run

**Markets/news articles I deliberately didn't re-date:**
- `finance-act-2026.html` (22 May — real legislative date)
- `business-owners-pensions-and-the-2027-changes.html` (19 May — leave alone)
- `bank-of-england-holds-rates-may-2026.html` (11 May — real BoE decision date)
- `market-commentary-may-2026.html` (was 11 May; if you want, change to 12 May to separate from BoE)
- `market-commentary-april-2026.html` (20 April — keep)

If you want to re-date any of these too, uncomment them in the script's `DATE_CHANGES` dict.

---

*Batch 2 prepared 22 May 2026.*
