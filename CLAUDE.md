# Bayshore Health — repo guide

Static HTML marketing site. **No build step.** Deploys via GitHub Pages from `main` to **www.bayshore.health** (see `CNAME`). Pushing to `main` publishes within a minute or two — there is no staging.

## Layout

```
index.html            Home (everything inline — does NOT link styles.css)
practice.html         Five practices
case-studies.html
team.html
ecosystem.html        Exec network — exec roster cards
faq.html
contact.html          Consultation booking form
styles.css            Shared base + responsive rules (linked by the 6 above; NOT by index.html)
clients/<slug>/       Per-client packets (orphan pages, not linked from main nav)
  └─ skus/            Productized SKU pages
     └─ _brand.css    Shared style file for that packet
logos/, team/, uploads/   Image assets
```

`bayshore-output/` is the `/bayshore-productize` skill's local working dir (recs, scope docs, deliverable drafts in MD+HTML). Gitignored — promote finalized HTML to `clients/<slug>/` to publish.

## CSS conventions

- **Design tokens** (defined in every page's `:root`): `--ink #0e1d28`, `--terra #d97757`, `--teal #1a3942`, `--sage #3a7a5a`, `--stone`, `--paper`, `--paper-2`, `--rule`.
- **Fonts**: `Fraunces` (display, italic em for accent), `Geist` (body), `Geist Mono` (labels/meta).
- **`styles.css` vs inline `<style>`**: shared components (`.nav`, `.cta-block`, `.contact`, `.foot`, `.page-hero`) live in `styles.css`; page-specific layouts live inline. `index.html` is fully inline (no `styles.css` link) — duplicate shared rules apply there.

## Responsive

Breakpoints: **1080px** (tablet — multi-col grids collapse), **860px** (nav → hamburger), **720px** (phone — single column, padding `56px → 20px`, headings shrink).

The nav uses a **CSS-only hamburger** (checkbox-hack — no JS). Markup pattern inside `.nav`:

```html
<input type="checkbox" id="navToggle" class="nav-toggle" hidden />
<label for="navToggle" class="nav-burger" aria-label="Toggle menu"><span></span><span></span><span></span></label>
```

When adding a new page, copy this from any existing page so the menu works.

## Verification

Static-site checks need a server (relative paths don't resolve over `file://` cleanly):

```bash
pm2 start "python3 -m http.server 8765" --name bayshore-static
# then point Playwright/Brave at http://localhost:8765/<page>.html
pm2 delete bayshore-static   # when done
```

Mobile sanity check — at 390×844 verify `document.body.scrollWidth === clientWidth` (no horizontal overflow) on each touched page.

## Git

- Default branch: `main` — commits here publish live. No PRs in this workflow.
- Repo is **public** (`mike32snake/bayshore-health`).
- Commits attributed `mike32snake`. This is a personal/Bayshore repo, not GenHealth — don't apply the GenHealth SSDLC rules from the global CLAUDE.md here.
