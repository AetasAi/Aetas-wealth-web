# Aetas Wealth — Insights Auto-Indexer

Automatically updates `insights/index.html` whenever you add, change, or remove articles in `insights/posts/`.

## What you get

- Drop a new article HTML file into `insights/posts/` → it appears on the Insights index automatically
- Delete a file → it disappears from the index
- Articles sorted by date (newest first)
- Category filter pills continue to work as before
- Opt-out per article when you want to hide one from the index

## One-time setup

### 1. Add the two files to your repo

| File | Location |
|---|---|
| `build-insights-index.py` | `scripts/build-insights-index.py` |
| `update-insights-index.yml` | `.github/workflows/update-insights-index.yml` |

Create the `scripts/` folder if it doesn't exist. The `.github/workflows/` folder may already exist if you have other Actions.

### 2. Add the marker comments to `insights/index.html`

The indexer needs to know where to put the article cards. Find the existing `<ul class="post-list" id="insights-list">` block in your index file. Replace **everything between the opening and closing `<ul>` tags** with the two marker comments:

```html
<ul class="post-list" id="insights-list">

  <!-- AUTO-INSIGHTS-START -->
  <!-- AUTO-INSIGHTS-END -->

</ul>
```

The first time the indexer runs, it will fill in all the article cards. After that, every push to `insights/posts/` will keep it in sync.

### 3. Commit and push

Commit the three changes (script, workflow, index.html with markers) and push to main. GitHub Actions will fire, run the indexer, and commit back an updated `insights/index.html` with all your articles listed.

You'll see a second commit appear in your repo named "chore: auto-update insights index" — that's the bot.

## How articles are read

For each article in `insights/posts/`, the indexer extracts:

| Card field | Where it comes from |
|---|---|
| Date | JSON-LD `datePublished` → "Published X" byline → file modified date |
| Title | `<h1>` → `<title>` tag (with "· Aetas Wealth" stripped) |
| Description | `<p class="lead">` → `<meta name="description">` |
| Category | `<span class="eyebrow">` → mapped to display label and filter tags |

If an article doesn't have these elements, the indexer uses sensible fallbacks.

## Per-article controls

You can add these optional meta tags to any article's `<head>` to override defaults:

```html
<!-- Hide this article from the index entirely -->
<meta name="aw-listed" content="false">

<!-- Override the display label that shows next to the date -->
<meta name="aw-display-category" content="Inheritance tax">

<!-- Override the filter tags (space-separated, must match the filter pills) -->
<meta name="aw-categories" content="iht pensions">
```

Filter tags must match what's in the filter pill buttons on the index page. Currently those are: `pensions`, `investments`, `iht`, `markets`, `planning`, `workplace`.

## Running locally (optional)

If you want to preview the change before pushing, you can run the indexer manually:

```bash
cd /path/to/your/repo
python3 scripts/build-insights-index.py
```

It will print which articles it found and whether the index changed.

Requires Python 3.8+. No external dependencies — uses only the standard library.

## Category mapping

The eyebrow text on each article is mapped to a short display label and one or more filter tags. The mapping is in `scripts/build-insights-index.py` at the top, in the `CATEGORY_MAP` constant. Edit it there if you add new categories or want to rename existing ones.

Current mappings:

| Eyebrow contains | Display label | Filter tags |
|---|---|---|
| Inheritance Tax & Pensions | Inheritance tax | iht, pensions |
| Inheritance Tax & Giving | Inheritance tax | iht, planning |
| Estate Planning & IHT | Inheritance tax | iht, planning |
| Pensions & Retirement | Pensions | pensions |
| Savings & Investments | Investments | investments |
| Market commentary | Market commentary | markets |
| Financial Planning | Financial planning | planning |
| (just "Pensions") | Pensions | pensions |
| (just "Markets") | Markets | markets |
| (just "ISAs") | ISAs | investments |
| (just "Workplace" / "SMEs") | Workplace | workplace |
| (unrecognised) | Insights | all |

## Troubleshooting

**The workflow didn't run.** Check the Actions tab on GitHub. The most common reasons:
- Workflow file wasn't in `.github/workflows/`
- Repository setting "Settings → Actions → Workflow permissions" needs to be "Read and write" so the bot can push back
- Your push didn't actually touch a file under `insights/posts/`

**The index didn't change.** Run it locally — `python3 scripts/build-insights-index.py` — and see what it prints. If "No change needed" then it thinks the index is correct. If you don't see your article listed, check it has the marker tags in its `<head>` (the script depends on the standard template).

**An article shows the wrong category.** Either:
- Update the `<span class="eyebrow">` text in the article, or
- Add `<meta name="aw-display-category">` and `<meta name="aw-categories">` to override

**The bot's commit triggers another build.** It won't — the workflow's `paths:` filter only triggers on changes to `insights/posts/`, not `insights/index.html`. So the bot's commit is a dead-end and stops the cycle.

## Removing the system

If you ever want to go back to managing the index by hand:
- Delete `.github/workflows/update-insights-index.yml`
- Optionally delete `scripts/build-insights-index.py`
- Replace the markers in `insights/index.html` with manually-written `<li>` blocks
