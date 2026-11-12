# claimball-rest

Claimball (F-021) official site, https://claimball.ipe.rest. Static, GitHub Pages, generator `scripts/build_site.py` (stdlib only, Python 3.8+ compatible).

- Never hand-edit generated files (`index.html`, `about/`, `privacy/`, `support/`, `terms/`, `journal/`, `ko/`, `sitemap.xml`, `robots.txt`, `llms.txt`, `404.html`). Edit `content/` or the generator, then run `python3 scripts/build_site.py`.
- Green gate before every commit: `bash scripts/check.sh` must print GREEN. UI check: `tests/ui_check.js` (see README).
- Bump `ASSET_V` in `build_site.py` when `assets/claimball.css` or `claimball.js` change; bump `SITE_UPDATED` when home/404 text changes; each page's "Last updated" is its front matter `updated:`.
- Content rules: game facts only from the approved intro (6x10 notebook grid, bounce tile becomes land, center hit smash = 3 tiles, about 90 second match, 6 AI rivals in 2 leagues at launch (more in updates), iOS/Android coming soon, monetization = free to try + one purchase unlocks everything, no ads, no subscription, price amount unannounced). No price, no rival names, no ratings or counts, no emoji, never the words Pong / 핑퐁 / 탁구 (the build rejects them).
- Privacy / terms / support derive from iltonggi-rest with the app name swapped; do not add new clauses without the owner's decision.
- Journal publishes daily at 18:00 KST via `ops/` (template only; launchd is installed by the maintainer, never by this repo). GA4 (G-XG4BH800J0, same property as ipe.rest) is inserted into every page by `GA_SNIPPET` in `build_site.py` (owner 2026-11-01); the website privacy policy / support FAQ / llms.txt say so. The app itself has no analytics SDK. Change them together.
- The shared web kit `ipe_web_kit` is private, so its source is never committed (this repo is public) — only `vendor/ipe_web_kit.lock` is. Install: `python3 scripts/kit_lock.py sync --kit <kit clone>`; CI installs it with a read-only deploy key (`.github/actions/ipe-web-kit`). `deploy.yml` excludes `vendor` from the published site; `scripts/indexnow.py` is a thin shell over the kit.
- No `docs/` folder and no planning markdown in this repo.
