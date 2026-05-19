# Aetas Wealth — three batch updates in one

This bundle is 50 HTML files. Drop them into your local repo (overwriting where
prompted), commit, push. That's it.

## What it does

Three things, applied across the whole site in one pass:

### 1. Case studies surfaced on the homepage (`index.html` only)
A new "Recent client work" section sits between the existing dark blue stats
band and the "Ready to have a conversation?" CTA strip. Three cards link
through to the existing case studies:
- A couple in their late 50s, retiring with confidence
- A business owner planning the right exit
- Bringing clarity after an inheritance

A "View all case studies" link sits beneath the cards, pointing to your
existing /case-studies/ index.

### 2. "55+" → "50+" in the stats band (`index.html` only)
Fixes the inconsistency between the hero (50+ advisers) and the dark blue
stats band (55+). Both now agree.

### 3. Professional Introducers added to the footer Site column
Applied to every page in the repo that has a full footer. The link sits just
before Contact, with the correct relative path per file depth (so insights
posts get `../../professional-introducers.html` and root pages get
`professional-introducers.html`).

## Files included

50 in total. The breakdown:

- **Root pages (16)**: business-owners, businesses, complaints, contact, fees,
  index, lifetime-to-legacy, our-approach, our-people, pensions-iht-2027,
  privacy, terms, working-with-us, workplace, and others
- **Case studies (4)**: business-owner-exit, index, inherited-wealth-clarity,
  retiring-with-confidence
- **Insights index + 20 posts**
- **Services (9)**: cash-flow-planning, director-owner-advisory,
  financial-planning, investment-management, later-life-planning, mortgages,
  pensions-retirement, protection-planning, and others (inheritance-tax already
  has the footer link from the earlier batch, so it's not included here)
- **Team (3)**: daniel-cottam, matthew-steiner, peter-rose

## Files NOT in the bundle (deliberately)

- **`home.html`** — it's just a redirect to `/`, no footer to update
- **`404.html`** — typically no full footer, skipped to be safe
- **`individuals.html`**, **`professional-introducers.html`**, **`services/inheritance-tax.html`** — already have the footer link from the previous batch

## How to install

1. Extract the zip
2. In Windows File Explorer, select all the extracted files and folders, and
   drag them into the root of your local repo
3. Windows will ask whether to merge folders and overwrite files. Say yes to
   both
4. (Optional but recommended) Preview the homepage and one other page locally
   to confirm everything renders:
   ```
   python -m http.server 8000
   ```
   Then open http://localhost:8000 and http://localhost:8000/contact.html
5. In GitHub Desktop, you should see 50 changed files. Commit:

   > Surface case studies on homepage, align stats band, add Professional Introducers footer link site-wide

6. Push

## Verification

Each file has been:
- Downloaded fresh from GitHub at the start of this batch (so we're patching
  the current live state, not stale versions)
- Patched only where the patch was needed
- Validated as well-formed HTML
- Hash-compared against the live version, so only genuinely-changed files are
  in this bundle (no "no-op" commits cluttering the history)

The footer-link patch is idempotent: it checks for an existing
"Professional Introducers" link in the footer Site column before adding,
and won't double-up if the file already has it.
