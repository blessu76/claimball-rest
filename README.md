# claimball-rest

Official website of **Claimball**, a casual player-versus-AI duel game for iOS and Android (coming soon). Live at https://claimball.ipe.rest

Static site on GitHub Pages. The generator is `scripts/build_site.py` (Python 3.8+, standard library only). Generated files (`index.html`, `about/`, `ko/`, `journal/`, `sitemap.xml`, ...) are never edited by hand.

## Layout

| Path | What |
|---|---|
| `content/i18n/<lang>.json` | UI strings and home copy (same keys in every language) |
| `content/pages/<lang>/{about,privacy,support,terms}.md` | pages (front matter: title, description, updated) |
| `content/releases.json` | release notes (empty until a build is public) |
| `content/journal/<slug>/<lang>.md` | published posts |
| `content/queue/NN-slug/{en,ko}.md` | queued posts (no `published:` yet) |
| `assets/` | CSS (design tokens are CSS variables), JS, icons, og image |
| `scripts/` | build, checks, publish, IndexNow |
| `ops/` | daily 18:00 KST publish job (template only, not installed) |
| `tests/` | unit tests and the Playwright UI check |

English is at the root; every other language lives under `/<code>/` (ko, ja, zh, es, pt, id, ru, vi, fr, de, ar, hi; ar is right-to-left, `dir="rtl"`). English and Korean are the originals; the other eleven are translations of the English text (`translation_of: en` in each page and post). To add a language, add `content/i18n/<code>.json`, `content/pages/<code>/*.md` and the code to `LANGS` in `build_site.py`. Journal posts without a translation simply do not appear in that language yet.

## Commands

```
python3 scripts/build_site.py          # regenerate the site
bash scripts/check.sh                  # green gate: sources, tests, build up to date, sitemap
NODE_PATH=<dir with playwright> node tests/ui_check.js [outDir]   # overflow / clipping / console check at 375, 320, 768, 1280 px
NODE_PATH=<dir with playwright> node scripts/render_png.js        # og-image and icons from assets/og-source.html and favicon.svg
python3 scripts/publish_post.py --daily                           # move the next queued post into the journal
python3 scripts/indexnow.py --help
```

Deploy: every push to `main` runs `.github/workflows/deploy.yml` (green gate, then publish to GitHub Pages). `CNAME` holds the custom domain.

## Rules

- Build and tests must be green before any commit.
- No price, ratings, download counts or reviews on the site; no emoji; no real secrets in the repo.
- Colors and fonts live in CSS variables at the top of `assets/claimball.css` because the design is still changing.

## ipe_web_kit (private) — local setup

The shared web kit is a private repo, so its source is **not** committed here (this repo is public). Only `vendor/ipe_web_kit.lock` (tag, commit, manifest hash) is. Before building:

```sh
python3 scripts/kit_lock.py sync --kit ~/Developer/ipe_web_kit   # copy the locked tag from a local kit clone into vendor/ipe_web_kit/ (gitignored)
python3 scripts/kit_lock.py check                                  # installed copy == lock
```

CI (`.github/actions/ipe-web-kit`) checks out the kit at the locked commit with a read-only deploy key (secret `IPE_WEB_KIT_DEPLOY_KEY`) and runs the same `sync`.
To move to another kit tag: `python3 scripts/kit_lock.py sync --kit <clone> --update --tag vX.Y.Z`, run `bash scripts/check.sh`, commit the lock.
