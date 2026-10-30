# claimball-rest

Official website of **Claimball**, a casual player-versus-AI duel game for iOS and Android (coming soon). Live at https://claimball.ipe.rest

Static site on GitHub Pages. The generator is `scripts/build_site.py` (Python 3.8+, standard library only). Generated files (`index.html`, `about/`, `ko/`, `journal/`, `sitemap.xml`, ...) are never edited by hand.

## Layout

| Path | What |
|---|---|
| `content/i18n/{en,ko}.json` | UI strings and home copy (same keys in every language) |
| `content/pages/{en,ko}/{about,privacy,support,terms}.md` | pages (front matter: title, description, updated) |
| `content/releases.json` | release notes (empty until a build is public) |
| `content/journal/<slug>/{en,ko}.md` | published posts |
| `content/queue/NN-slug/{en,ko}.md` | queued posts (no `published:` yet) |
| `assets/` | CSS (design tokens are CSS variables), JS, icons, og image |
| `scripts/` | build, checks, publish, IndexNow |
| `ops/` | daily 18:00 KST publish job (template only, not installed) |
| `tests/` | unit tests and the Playwright UI check |

English is at the root, Korean under `/ko/`. More languages can be added later by adding `content/i18n/<code>.json`, `content/pages/<code>/*.md` and the code to `LANGS` in `build_site.py`.

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
