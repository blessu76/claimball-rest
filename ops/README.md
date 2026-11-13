# Daily publish automation (not installed by this repo)

Policy: **one post a day at a random afternoon time (12:00–17:59 KST, never the same hour as yesterday; `publish_gate.py`)** while the app is unreleased (2026-10-29). The publish time recorded in each post is the real time
the script ran (HH:MM KST); a future time is refused.

| File | Role |
|---|---|
| `publish_daily.sh` | safety checks → push leftovers → `publish_post.py --daily` → green gate → commit → push → live check → IndexNow |
| `rest.ipe.claimball-publish.plist.template` | launchd job template (`__HOME__` placeholder; launchd does not expand `~`), calls `publish_gate.py` every 15 min 12:00–18:45; the gate draws the day's slot into `~/.ipe/queue/claimball/slot.json` and runs `publish_daily.sh` once from then on (no-op once published), log `~/Library/Logs/claimball-publish.log` |
| `publish_gate.py` | random-slot gate (tests/test_publish_gate.py); retries each tick while publish_daily SKIPs/fails |
| `install_launchd.sh` | renders the template for the current user, `plutil -lint`, writes `~/Library/LaunchAgents/…plist` — does **not** load it |

## Safety rules (tests: `tests/test_publish_daily.py`)

- Runs in a **dedicated publish clone**: `CLAIMBALL_PUBLISH_DIR` (default `~/Developer/claimball-rest`). That clone must stay on `main` with a clean tree and
  must not be a place where anyone (or any agent) works on feature branches. On any other branch, or with uncommitted changes, the run logs `SKIP` and exits 0.
- A previous failed push is retried first (`origin/main..HEAD`), even when nothing new is due — but only if those commits touch nothing outside the publish set; otherwise `SKIP` (a local work-in-progress commit never rides along to main).
- An empty queue logs `QUEUE_EMPTY` (exit 0). Check the log for `SKIP`/`FAIL`/`QUEUE_EMPTY` regularly — they do not alert anyone.
- Publishing is atomic: if `publish_post.py` (build + sitemap check), the green gate or the path check fails, the tree is reset to where it started
  (`ROLLBACK` in the log), so no stamp for today is left behind and the next run can retry.
- One run at a time (`.git/publish.lock`; a lock from a dead process or older than 3 h is taken over). A second run logs `SKIP — another publish run is in progress`.
- Only the publish set is staged (`content/journal`, `content/queue`, generated pages); anything else in the tree aborts the run. Never `git add -A`.
- IndexNow gets the new post in every published language plus `/` and `/journal/`.

## Install (by the maintainer, once; the repo never does this itself)

1. Make the publish clone: `git clone https://github.com/blessu76/claimball-rest.git ~/Developer/claimball-rest` (must be on `main`; `git push` must work non-interactively).
2. The Mac's time zone must be KST (launchd's 18:00 is local time).
3. Check that pushing works the way launchd will do it (no terminal, no prompt):

```
git -C ~/Developer/claimball-rest push --dry-run origin HEAD:main     # must succeed without asking for anything (osxkeychain / ssh key / gh credential helper)
```

   [Whether the keychain is reachable from the LaunchAgent session itself is only proven by the first real 18:00 run — watch the log that day.]
4. Install and load:

```
launchctl bootout gui/$(id -u)/rest.ipe.claimball-publish 2>/dev/null   # only if an older version is already loaded; ignore the error otherwise
bash ops/install_launchd.sh                                      # renders + lints; loads nothing
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/rest.ipe.claimball-publish.plist
launchctl kickstart gui/$(id -u)/rest.ipe.claimball-publish        # run once now (only if you want a post now); never with -k: that kills a run in progress
```

Uninstall: `launchctl bootout gui/$(id -u)/rest.ipe.claimball-publish && rm ~/Library/LaunchAgents/rest.ipe.claimball-publish.plist`.
Log: `tail -f ~/Library/Logs/claimball-publish.log` (lines: `SKIP`, `FAIL`, `ROLLBACK` / `ROLLBACK FAILED`, `QUEUE_LOW n` (3 or fewer queued), `QUEUE_EMPTY`, `committed`, `pushed`).

Before relying on it: the queue (`content/queue/`) has posts and their translations exist (docs/TRANSLATION.md). When the queue is empty the job does
nothing and exits 0 — write new posts into `content/queue/NN-slug/` (NN keeps the order).
