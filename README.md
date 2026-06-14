# Aetas Wealth €” Website Repository

The source code for **aetas-wealth.com**, hosted on GitHub Pages and served from the `main` branch.

This README is a working document for anyone who needs to make changes to the site. If you're returning to this in six months and have forgotten the details, start here.

---

## Quick facts

| | |
|---|---|
| Live site | https://aetas-wealth.com |
| Repo | `AetasAi/Aetas-Wealth-Web` |
| Hosting | GitHub Pages (deploys automatically on push to `main`) |
| Domain config | `CNAME` file in repo root sets the custom domain |
| Stack | Static HTML / CSS / JS (no build step, no framework) |
| Brand | Open Sans typeface, Deep Blue #00205B, Turquoise #009CA6, Gold #9A7B3A |

---

## Repo structure

Where things live. Files in the **wrong folder will not render correctly**, because the CSS, JS and image paths use relative references (`../assets/`, `./assets/` etc.).

```
/
”œ”€”€ index.html               † Homepage
”œ”€”€ home.html                † Redirect file (catches /home requests, sends to /)
”œ”€”€ 404.html                 † Custom 404 page
”œ”€”€ CNAME                    † Custom domain config (do not edit)
”œ”€”€ README.md                † This file
”‚
”œ”€”€ Root-level pages         † One file per top-level page
”‚   business-owners.html
”‚   businesses.html
”‚   complaints.html
”‚   contact.html
”‚   fees.html
”‚   individuals.html
”‚   inheritance-tax.html
”‚   lifetime-to-legacy.html
”‚   our-approach.html
”‚   our-people.html
”‚   pensions-iht-2027.html
”‚   privacy.html
”‚   professional-introducers.html
”‚   terms.html
”‚   working-with-us.html
”‚   workplace.html
”‚
”œ”€”€ assets/                  † All shared assets
”‚   ”œ”€”€ css/styles.css
”‚   ”œ”€”€ js/main.js
”‚   ”””€”€ images/              † Logos, favicons, adviser photos
”‚
”œ”€”€ team/                    † Adviser profile pages
”‚   ”œ”€”€ matthew-steiner.html
”‚   ”œ”€”€ daniel-cottam.html
”‚   ”””€”€ peter-rose.html
”‚
”œ”€”€ services/                † Individual service pages
”‚   ”œ”€”€ cash-flow-planning.html
”‚   ”œ”€”€ director-owner-advisory.html
”‚   ”œ”€”€ financial-planning.html
”‚   ”œ”€”€ inheritance-tax.html
”‚   ”œ”€”€ investment-management.html
”‚   ”œ”€”€ later-life-planning.html
”‚   ”œ”€”€ mortgages.html       † Exists but not linked from main nav (intentional)
”‚   ”œ”€”€ pensions-retirement.html
”‚   ”””€”€ protection-planning.html
”‚
”œ”€”€ case-studies/            † Real-client case studies
”‚   ”œ”€”€ index.html
”‚   ”œ”€”€ business-owner-exit.html
”‚   ”œ”€”€ inherited-wealth-clarity.html
”‚   ”””€”€ retiring-with-confidence.html
”‚
”œ”€”€ insights/                † Blog index and posts
”‚   ”œ”€”€ index.html           † Article list with category filter
”‚   ”””€”€ posts/               † Individual articles
”‚
”œ”€”€ aetas-adeus-life-digital-wills/   † Partner landing page (adeus Life)
”‚   ”””€”€ index.html
”‚
”œ”€”€ aetas-tls-solicitors/    † Partner landing page (TLS Solicitors)
”‚   ”””€”€ index.html
”‚
”””€”€ aetas-gympanzees/        † Partner landing page (Gympanzees)
    ”””€”€ index.html
```

### The most common upload mistake

When uploading via the GitHub web UI, **navigate INTO the destination folder first** before clicking "Add file †’ Upload files". Files dropped at the repo root will land at the root regardless of their original filename, and orphaned duplicates will accumulate.

For example: to update `team/daniel-cottam.html`, click into the `team/` folder first. The URL bar should read `/Aetas-Wealth-Web/tree/main/team` before you upload.

---

## Booking links €” calendar ID mapping

All booking buttons should point to `link.aetas-wealth.com` (the new GoHighLevel domain). The previous `links.aetas-partners.com` domain has been retired and will 404.

| Button | Calendar ID | URL |
|---|---|---|
| Generic "Book a meeting" (used in nav and most CTAs) | `LlxFl4DIfn023BvfaFO7` | `https://link.aetas-wealth.com/widget/booking/LlxFl4DIfn023BvfaFO7` |
| Peter Rose (dedicated) | `56ArZJ2rvBIOdrI7uxf8` | `https://link.aetas-wealth.com/widget/booking/56ArZJ2rvBIOdrI7uxf8` |
| Daniel Cottam (dedicated) | `P2aXZCK3ZolC87VOHAQG` | `https://link.aetas-wealth.com/widget/booking/P2aXZCK3ZolC87VOHAQG` |
| Matthew Steiner (dedicated) | `30C6BtjFERcoVPRqei6t` | `https://link.aetas-wealth.com/widget/booking/30C6BtjFERcoVPRqei6t` |

When adding a new page, default to the generic booking ID in the nav. Use a dedicated calendar only on pages that specifically promote one adviser.

---

## Conventions for new pages

If you're creating a new page, copy an existing similar page (`fees.html` or `our-approach.html` are simple starting points) and adapt. Pay attention to:

**Relative paths.** Pages at the root link to `assets/css/styles.css`. Pages one level deep (in `team/`, `services/`, `case-studies/`) link to `../assets/css/styles.css`. Pages two levels deep (`insights/posts/`) link to `../../assets/css/styles.css`. Get this wrong and the page will load with no styling.

**The shared header and footer.** Both are duplicated across every HTML file (there is no template system). If you change one, change all of them. The site nav lives in `<header class="site-header">` and the footer in `<footer class="site-footer">`.

**Writing style.** UK English. Consultative and warm, not salesy. Grade 9 reading level. No em dashes (use commas or full stops). No jargon. No generic openers like "In today's fast-paced world".

**Page banner.** Most pages have a `<section class="page-banner">` at the top with breadcrumbs and a short lead paragraph. Keep the lead under two sentences.

---

## Deployment workflow

GitHub Pages rebuilds the site automatically every time you push to `main`. Usually live within a couple of minutes. There is no separate build step.

### Option 1 €” GitHub web UI (best for one or two file changes)

1. Navigate to the destination folder in the repo
2. Click **Add file †’ Upload files**
3. Drag in the file(s)
4. If the file already exists, GitHub will overwrite it on commit
5. Commit message: short, descriptive, present tense (e.g. "Fix booking link on contact page")
6. Click **Commit changes**

### Option 2 €” GitHub Desktop (best for batches of changes)

1. Make changes to files in your local clone
2. GitHub Desktop will show the changed files in the Changes tab
3. Write a commit message in the summary field
4. Click **Commit to main**
5. Click **Push origin** to upload to GitHub

**If you've made changes via both the web UI AND GitHub Desktop**, your local clone will be out of sync. Pull first before making more local changes, or you'll hit merge conflicts.

### Cache busting after deploys

GitHub Pages uses a CDN. Your edits may take a few minutes to appear, and the page you're testing may be cached. To force-refresh:

- **Windows:** Ctrl + Shift + R
- **Mac:** Cmd + Shift + R

Sometimes adding a meaningless query string (e.g. `aetas-wealth.com/contact.html?v=1`) helps bypass the cache. View Source (Ctrl + U) is the ground truth for what's actually deployed.

---

## Recent history

A high-level log of major changes. For details, see the Git commit history.

### May 2026 €” Booking links and site cleanup

- Migrated all booking links from `links.aetas-partners.com` (retired) to `link.aetas-wealth.com`
- Mapped dedicated booking calendars for Peter, Daniel and Matthew
- Localised Peter's headshot to `assets/images/` and edited the photo (removed teal blob, square frame)
- Localised Matthew and Daniel headshots to `assets/images/`
- Reframed Daniel's profile copy to "Independent Financial Planner" across mini-bio, full profile, page banner and meta description
- Restored insights index with category filter pills (had been overwritten by a version without them)
- Stripped phone number from contact meta, complaints contact strip, and mortgages footer
- Updated "Workplace Performance Review" †’ "Workplace Performance Audit" terminology
- Reworked partner-network language sitewide (removed references to "Aetas network of professional advisers" etc.)
- Three partner pages (adeus, TLS, Gympanzees) €” fixed About / Services / Privacy / Terms nav links to point at Wealth pages rather than the retired Partners URLs

### April 2026 €” Partner pages built

- Created three partner-introducer landing pages at `aetas-adeus-life-digital-wills/`, `aetas-tls-solicitors/`, `aetas-gympanzees/`
- Each is an Aetas Wealth landing page tailored to clients arriving from that partner

### Early 2026 €” Site built from scratch

- Replaced previous WordPress site
- Custom static HTML build, deployed via GitHub Pages

---

## Things to be careful of

A few items that have caused real problems in the past:

**Files at the wrong path.** When uploading via the web UI, always check you're in the correct folder before clicking Upload Files. Orphan duplicates at the repo root will not render correctly (because of relative paths) and clutter the structure.

**Forgetting to update all instances of a shared element.** The header and footer are duplicated across every HTML file. If you update one, update all.

**Editing locally AND on the web UI in parallel.** Pick one route per session, or you'll create merge conflicts. If conflicts arise in GitHub Desktop, the safest reset is to abort the merge, rename the local clone folder to `-old`, and re-clone fresh.

**Cross-domain image references.** If you reference an image on a different domain (e.g. an old `aetas-partners.com` URL), it will break if that domain goes down or changes. Prefer localised images in `assets/images/`.

---

## Related sites

- **aetas-partners.com** €” group parent site (separate WordPress)
- **workplace.aetas-wealth.com** €” Aetas in the Workplace site (separate GitHub repo, `AetasInTheWorkplace`)
- **fpa.aetaspartners.com** €” Flexible Pension Annuity site (separate GitHub repo)

These sites are independent but share brand conventions. If you're updating something cross-cutting (e.g. office address), it may need updating in multiple places.

---

*Last updated May 2026. Brief description of any major future change can be added to the Recent history section above.*

