# Aetas Wealth — Scheduled Publishing System

You can now batch-upload articles to your repo with **future dates**, and they'll appear on the Insights index automatically when their date arrives — Tuesday and Thursday cadence built in.

LinkedIn teasers (via GHL) can be generated automatically with matching dates, so each article and its LinkedIn teaser fire the same day.

---

## What's in this package

| File | Goes to | Purpose |
|---|---|---|
| `build-insights-index.py` | `scripts/` (overwrites existing) | Updated indexer — hides future-dated articles |
| `scheduled-publish.yml` | `.github/workflows/` (new) | Daily 7am UK action — releases articles when dates arrive |
| `schedule-articles.py` | `scripts/` (new) | Helper — sets Tue/Thu dates on a batch of articles |
| `generate-linkedin-csv.py` | `scripts/` (new) | Generates a GHL CSV matched to article dates |

---

## How the system works

### Two GitHub Actions, two jobs

You'll have **two workflows** running in your repo after this is deployed:

**1. `update-insights-index.yml`** *(existing — no changes)*

- Fires when you push changes to `insights/posts/**`
- Runs the indexer immediately
- Best for: real-time updates when you push an article that should be live now

**2. `scheduled-publish.yml`** *(new)*

- Fires every day at 06:30 UTC (around 7-7:30am UK time)
- Runs the indexer with today's date
- Articles whose `datePublished` is now in the past get added to the index
- Best for: revealing future-dated articles on schedule

### The new "future date" filter

The indexer now ignores any article with a `datePublished` later than today's date. So:

```
posts/
├── article-1.html     (datePublished: 2026-05-15)   ← published, visible
├── article-2.html     (datePublished: 2026-05-22)   ← published today, visible
├── article-3.html     (datePublished: 2026-05-26)   ← FUTURE, hidden
└── article-4.html     (datePublished: 2026-06-15)   ← FUTURE, hidden
```

The article URLs **still work directly** — `https://aetas-wealth.com/insights/posts/article-3.html` will load fine. They just don't appear on the Insights index page until their date arrives.

This means you can:
- Submit hidden URLs to Google Search Console early to get pre-indexed
- Share preview links with colleagues before public publication
- Make the LinkedIn teaser go live on the same day as the article (because the article URL works the moment you push)

---

## One-time setup (the boring bit)

### Step 1: Replace the existing indexer

In your repo:
- File Explorer → `C:\Repos\Aetas-wealth-web\scripts\`
- Overwrite `build-insights-index.py` with the new version from this package
- Don't delete it, just replace

### Step 2: Add the new GitHub Action

- File Explorer → `C:\Repos\Aetas-wealth-web\.github\workflows\`
- Drop `scheduled-publish.yml` into this folder (alongside your existing `update-insights-index.yml`)

### Step 3: Add the helper scripts

- Drop `schedule-articles.py` and `generate-linkedin-csv.py` into `C:\Repos\Aetas-wealth-web\scripts\`

### Step 4: Commit and push

In GitHub Desktop:
- Commit message: `Add scheduled publishing system`
- Push to main

The new daily workflow is now live. It'll start firing tomorrow at 06:30 UTC. You can also trigger it manually from the Actions tab whenever you want.

---

## Day-to-day usage

### Workflow A: Schedule a batch of new articles

You've just written or received 10 new articles. You want them released Tuesday and Thursday over the next 5 weeks.

**1. Copy the articles** into `insights/posts/` as usual.

**2. Open `scripts/schedule-articles.py`** in Notepad. Edit two things at the top:
   ```python
   START_FROM = date(2026, 6, 2)  # First publish date (will round to next Tue/Thu)
   
   ARTICLE_ORDER = [
       "first-article.html",
       "second-article.html",
       "third-article.html",
       # ... in the order you want them released
   ]
   ```

**3. Save the script, then run it:**
   ```
   py scripts\schedule-articles.py
   ```

This updates each article's `datePublished` (both JSON-LD and the byline text) to a Tuesday or Thursday in sequence.

**4. (Optional) Generate matching LinkedIn teasers:**
   ```
   py scripts\generate-linkedin-csv.py
   ```
   
This creates `ghl-linkedin-teasers.csv` at the repo root, with auto-generated teasers timed to each article's release date. Upload it to GHL Social Planner.

**5. Commit and push.**

That's it. Articles will appear on the Insights index automatically on their scheduled days. LinkedIn teasers will fire from GHL the same day.

---

### Workflow B: Release something immediately (the old way)

Sometimes you'll want to publish an article RIGHT NOW (e.g. responding to a news event). Just set its `datePublished` to today's date and push. The existing `update-insights-index.yml` action fires on the push and adds it immediately.

Both workflows coexist happily — the manual-push workflow handles "publish now", the daily scheduled workflow handles "publish on schedule".

---

### Workflow C: Adjust a scheduled article's date

Future-dated article needs to slip a week? Just open the file in Notepad, find the JSON-LD `datePublished` and the byline date, change them. Push the change. The system will respect the new date on the next daily run.

Or, more easily — re-run `schedule-articles.py` with an updated `ARTICLE_ORDER` to re-shuffle the dates.

---

## The full automated flow, end to end

Here's what happens when you set up a batch correctly:

```
Day 0 (today):  Run schedule-articles.py + generate-linkedin-csv.py
                Commit and push.
                → 10 articles sit in posts/ with future dates
                → 10 LinkedIn teaser rows sit in ghl-linkedin-teasers.csv
                → You upload the CSV to GHL Social Planner

Day 0:          Tuesday 2 June 2026 at 06:30 UTC:
                → Daily workflow fires
                → Sees article-1.html dated 2026-06-02 is now today
                → Adds it to the index
                → Auto-commits index.html change
                → Site rebuilds in 30 seconds

Day 0 (later):  GHL Social Planner posts LinkedIn teaser at 8:00 UK
                → Article and LinkedIn post fire same day

Day 2:          Thursday 4 June 2026 at 06:30 UTC:
                → Daily workflow fires again
                → Sees article-2.html dated 2026-06-04 is now today
                → Same flow
                → ... and so on for the next 5 weeks
```

Zero manual intervention required between the initial push and the final article going live 5 weeks later.

---

## Troubleshooting

### "The daily workflow ran but didn't do anything"

This is normal on days when no articles are scheduled to release. The workflow runs every day, but only commits a change if there's something new to add to the index. Check the Actions log if curious — you'll see "· No scheduled articles to release today".

### "My article was supposed to release at 7am but didn't appear until 9am"

GitHub Actions schedules can run with a delay during peak hours. The cron isn't a hard guarantee — articles can release any time between 06:30 and 09:00 UK time. Usually closer to 7am.

If you need precise timing for a specific article (e.g. a market commentary tied to a Budget speech), publish it manually that day by pushing it with today's date.

### "I want to see what's scheduled but not yet released"

Run the indexer locally:
```
py scripts\build-insights-index.py
```
It'll print both the "Visible (published)" list and the "Scheduled for future release" list.

### "An article shows the wrong date"

The system reads dates in this priority:
1. JSON-LD `datePublished` (most reliable)
2. The "Published X" byline text
3. The file modification date (last-resort fallback)

If they disagree, JSON-LD wins. The `schedule-articles.py` helper updates both 1 and 2 together, but if you've manually edited the file you may have a mismatch.

### "I want to release an article TODAY that's currently scheduled for next month"

Two options:
1. **Quick fix**: open the file, change `datePublished` to today's date, push. Article appears on next workflow run (or you can manually trigger via Actions tab to make it instant).
2. **Bulk fix**: re-run `schedule-articles.py` with the article moved to position 1 in `ARTICLE_ORDER`.

### "I made a mistake and pushed an article with the wrong date"

GitHub keeps full history. You can either:
- Push a corrected version (the system handles it gracefully)
- Use GitHub Desktop's "Discard changes" or revert a commit if you really need to

---

## What about Christmas / holidays?

The system runs every day regardless. If you've scheduled articles for Christmas Day, they'll publish on Christmas Day. If that's not what you want, just leave gaps in your `ARTICLE_ORDER` schedule — easier to plan around holidays than to pause the system.

The `schedule-articles.py` script can also be configured to skip specific dates by adding them to a blacklist (let me know if this would help and I can add the feature).

---

## A note on the Tuesday / Thursday cadence

You picked Tue+Thu twice-weekly. The system will respect this — Tuesday is the strongest LinkedIn engagement day per Sprout Social's annual analytics, and Thursday is the next best. Avoiding Mondays (catch-up emails) and Fridays (lower attention spans) is a deliberate algorithm play.

If you ever want to change the cadence, edit `PUBLISH_DAYS` in `schedule-articles.py`:
```python
PUBLISH_DAYS = [1, 3]  # 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri
```

---

*Prepared 22 May 2026.*
