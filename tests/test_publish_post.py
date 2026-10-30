import datetime as dt
import shutil
import unittest
from pathlib import Path

from helpers import NOW, REPO, bs, make_site

import publish_post as pp  # noqa: E402  (helpers put scripts/ on sys.path)


class Publish(unittest.TestCase):
    def setUp(self):
        self.root = make_site(posts=(("old-post", "2026-11-02T19:00+09:00"),), queue=("first-up", "second-up"))
        self.addCleanup(shutil.rmtree, self.root, True)

    def test_takes_queue_head_and_stamps_every_language(self):
        slug, when, files = pp.publish(self.root, now=NOW)
        self.assertEqual(slug, "first-up")
        self.assertEqual(when, "2026-11-03T20:00+09:00")
        self.assertFalse((self.root / "content/queue/01-first-up").exists())
        for l in ("en", "ko"):
            t = (self.root / ("content/journal/first-up/%s.md" % l)).read_text()
            self.assertIn("published: 2026-11-03T20:00+09:00", t)
        self.assertEqual([p["slug"] for p in bs.load_posts(self.root, NOW)[0]][0], "first-up")
        self.assertEqual(bs.load_posts(self.root, NOW)[1], [])

    def test_named_slug_and_unknown_slug(self):
        self.assertEqual(pp.publish(self.root, "second-up", now=NOW)[0], "second-up")
        with self.assertRaises(SystemExit):
            pp.publish(self.root, "nope", now=NOW)

    def test_future_time_refused(self):
        with self.assertRaises(SystemExit) as cm:
            pp.publish(self.root, at="2026-11-03T20:01+09:00", now=NOW)
        self.assertIn("future", str(cm.exception))
        self.assertTrue((self.root / "content/queue/01-first-up").exists())  # nothing moved

    def test_explicit_past_time_ok_but_not_before_latest_post(self):
        self.assertEqual(pp.publish(self.root, at="2026-11-03T19:00+09:00", now=NOW)[1], "2026-11-03T19:00+09:00")
        with self.assertRaises(SystemExit):
            pp.publish(self.root, at="2026-11-01T19:00+09:00", now=NOW)

    def test_dry_run_changes_nothing(self):
        pp.publish(self.root, dry=True, now=NOW)
        self.assertTrue((self.root / "content/queue/01-first-up").exists())
        self.assertFalse((self.root / "content/journal/first-up").exists())

    def test_missing_original_refused_and_empty_queue(self):
        (self.root / "content/queue/01-first-up/ko.md").unlink()
        with self.assertRaises(SystemExit):
            pp.publish(self.root, now=NOW)
        shutil.rmtree(self.root / "content/queue")
        with self.assertRaises(SystemExit):
            pp.publish(self.root, now=NOW)

    def test_stamp_replaces_existing_line(self):
        t = "---\ntitle: x\npublished: 2020-01-01T00:00+09:00\n---\nbody\n"
        self.assertEqual(pp.stamp(t, "2026-11-03T20:00+09:00"), "---\ntitle: x\npublished: 2026-11-03T20:00+09:00\n---\nbody\n")

    def test_daily_skips_when_already_published_today(self):
        # last post is 2026-11-02; "today" in the CLI is the real clock, so build a post stamped with the real today
        today = dt.datetime.now(bs.KST).replace(hour=0, minute=0, second=0, microsecond=0)
        f = self.root / "content/journal/old-post"
        for p in f.glob("*.md"):
            p.write_text(p.read_text().replace("2026-11-02T19:00+09:00", today.strftime("%Y-%m-%dT00:00+09:00")))
        self.assertEqual(pp.main(["--daily", "--root", str(self.root), "--no-build"]), 0)
        self.assertTrue((self.root / "content/queue/01-first-up").exists())


if __name__ == "__main__":
    unittest.main()
