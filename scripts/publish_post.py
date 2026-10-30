#!/usr/bin/env python3
"""Publish the next post from the queue — stdlib only.

  python3 scripts/publish_post.py                  # publish the first queued post, stamped with the current KST minute
  python3 scripts/publish_post.py SLUG             # publish this queued post
  python3 scripts/publish_post.py --at 2026-10-30T19:00+09:00   # explicit time (never in the future)
  python3 scripts/publish_post.py --dry-run        # show what would happen, change nothing
  python3 scripts/publish_post.py --daily          # automation: do nothing (exit 0) if a post was already published today (KST)
  python3 scripts/publish_post.py --no-build       # skip the build + sitemap check (tests)

What it does
  1. content/queue/NN-slug/<lang>.md  ->  content/journal/slug/<lang>.md  (the NN- prefix orders the queue)
  2. stamps `published: YYYY-MM-DDTHH:MM+09:00` into every language file (the time is the real publish time; future times are refused)
  3. python3 scripts/build_site.py, then python3 scripts/check_sitemap.py
  4. prints the new URLs for IndexNow. It never commits, pushes or deploys — that is the caller's job (see ops/publish_daily.sh).
Missing translations only warn: a post is published with the languages it has; add the rest later and rebuild.
"""
import argparse
import datetime as dt
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_site as bs  # noqa: E402

DEFAULT_ROOT = Path(__file__).resolve().parent.parent


def queue_items(root):
    q = Path(root) / "content" / "queue"
    out = []
    for d in sorted(p for p in q.iterdir() if p.is_dir()) if q.is_dir() else []:
        m = re.match(r"^(\d+)-(.+)$", d.name)
        out.append((m.group(2) if m else d.name, d))
    return out


def stamp(text, when):
    """Set / replace the `published:` line in the front matter."""
    line = "published: %s" % when
    head, sep, rest = text.partition("\n---\n")
    if not head.startswith("---") or not sep:
        raise ValueError("no front matter")
    if re.search(r"^published:.*$", head, re.M):
        head = re.sub(r"^published:.*$", line, head, flags=re.M)
    else:
        head += "\n" + line
    return head + sep + rest


def last_published(root):
    posts, _ = bs.load_posts(root)
    return max((p["published"] for p in posts), default=None)


def publish(root, slug=None, at=None, dry=False, now=None):
    """-> (slug, when_string, [moved files]). Raises SystemExit with a message on refusal."""
    root = Path(root)
    now = now or dt.datetime.now(bs.KST)
    items = queue_items(root)
    if not items:
        raise SystemExit("queue is empty: nothing to publish")
    if slug:
        match = [(s, d) for s, d in items if s == slug]
        if not match:
            raise SystemExit("not in the queue: %s (queued: %s)" % (slug, ", ".join(s for s, _ in items)))
        slug, src = match[0]
    else:
        slug, src = items[0]
    when_dt = bs.parse_published(at) if at else now.replace(second=0, microsecond=0)
    if when_dt > now:
        raise SystemExit("refusing a future publish time: %s (now %s KST)" % (when_dt.strftime("%Y-%m-%dT%H:%M"), now.strftime("%H:%M")))
    prev = last_published(root)
    if prev and when_dt < prev:
        raise SystemExit("publish time %s is before the latest post (%s)" % (when_dt.strftime("%Y-%m-%dT%H:%M"), prev.strftime("%Y-%m-%dT%H:%M")))
    when = when_dt.strftime("%Y-%m-%dT%H:%M+09:00")
    dest = root / "content" / "journal" / slug
    if dest.exists():
        raise SystemExit("already published: %s" % slug)
    files = sorted(src.glob("*.md"))
    langs = {f.stem for f in files}
    for need in bs.MAIN_LANGS:
        if need not in langs:
            raise SystemExit("%s: %s original missing — refusing to publish" % (slug, need))
    missing = [l for l in bs.LANGS if l not in langs]
    if missing:
        print("warning: translations missing for %s: %s (published without them)" % (slug, ", ".join(missing)), file=sys.stderr)
    stamped = {f.name: stamp(f.read_text(encoding="utf-8"), when) for f in files}
    if dry:
        return slug, when, ["content/journal/%s/%s" % (slug, n) for n in stamped]
    dest.mkdir(parents=True)
    for name, text in stamped.items():
        (dest / name).write_text(text, encoding="utf-8")
    shutil.rmtree(src)
    return slug, when, ["content/journal/%s/%s" % (slug, n) for n in stamped]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug", nargs="?")
    ap.add_argument("--at")
    ap.add_argument("--root", default=str(DEFAULT_ROOT))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--daily", action="store_true")
    ap.add_argument("--no-build", action="store_true")
    a = ap.parse_args(argv)
    root = Path(a.root).resolve()
    now = dt.datetime.now(bs.KST)
    if a.daily:
        prev = last_published(root)
        if prev and prev.date() == now.date():
            print("publish_post: already published today (%s) — nothing to do" % prev.strftime("%Y-%m-%d %H:%M"))
            return 0
        if not queue_items(root):
            print("publish_post: queue is empty — nothing to do")
            return 0
    slug, when, files = publish(root, a.slug, a.at, a.dry_run, now)
    print("publish_post: %s%s at %s KST" % ("(dry run) " if a.dry_run else "", slug, when[:16].replace("T", " ")))
    if a.dry_run or a.no_build:
        return 0
    scripts = Path(__file__).resolve().parent
    for cmd in ([sys.executable, str(scripts / "build_site.py"), "--root", str(root)],
                [sys.executable, str(scripts / "check_sitemap.py"), "--root", str(root)]):
        r = subprocess.run(cmd)
        if r.returncode:
            print("publish_post: %s failed (exit %d)" % (Path(cmd[1]).name, r.returncode), file=sys.stderr)
            return r.returncode
    print("new URLs for IndexNow:")
    for l in bs.LANGS:
        if (root / bs.path_post(l, slug).lstrip("/") / "index.html").is_file():
            print("  " + bs.url(bs.path_post(l, slug)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
