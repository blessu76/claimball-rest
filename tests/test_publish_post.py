import contextlib
import datetime as dt
import io
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
        self.assertEqual(when, "2026-11-12T20:00+09:00")
        self.assertFalse((self.root / "content/queue/01-first-up").exists())
        for l in ("en", "ko"):
            t = (self.root / ("content/journal/first-up/%s.md" % l)).read_text()
            self.assertIn("published: 2026-11-12T20:00+09:00", t)
        self.assertEqual([p["slug"] for p in bs.load_posts(self.root, NOW)[0]][0], "first-up")
        self.assertEqual(bs.load_posts(self.root, NOW)[1], [])

    def test_named_slug_and_unknown_slug(self):
        self.assertEqual(pp.publish(self.root, "second-up", now=NOW)[0], "second-up")
        with self.assertRaises(SystemExit):
            pp.publish(self.root, "nope", now=NOW)

    def test_future_time_refused(self):
        with self.assertRaises(SystemExit) as cm:
            pp.publish(self.root, at="2026-11-12T20:01+09:00", now=NOW)
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
            pp.publish(self.root, "first-up", now=NOW)
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


class TwelveLanguages(unittest.TestCase):
    def setUp(self):
        self.root = make_site(posts=(("old-post", "2026-11-02T19:00+09:00"),), queue=("first-up", "second-up"))
        self.addCleanup(shutil.rmtree, self.root, True)
        self.q1 = self.root / "content/queue/01-first-up"
        self.q2 = self.root / "content/queue/02-second-up"

    def test_all_twelve_reviewed_publishes(self):
        self.assertEqual(sorted(p.stem for p in self.q1.glob("*.md")), sorted(pp.REQUIRED_LANGS))
        self.assertEqual(pp.publish(self.root, "first-up", now=NOW)[0], "first-up")
        self.assertTrue((self.root / "content/journal/first-up/pt-BR.md").is_file())

    def test_missing_language_refused_when_named_and_skipped_without_name(self):
        (self.q1 / "pt-BR.md").unlink()
        with self.assertRaises(SystemExit) as cm:
            pp.publish(self.root, "first-up", now=NOW)
        self.assertIn("pt-BR.md", str(cm.exception))
        self.assertTrue(self.q1.exists())
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            slug, _, _ = pp.publish(self.root, now=NOW)
        self.assertEqual(slug, "second-up")
        self.assertIn("skip first-up: missing pt-BR.md", err.getvalue())
        self.assertTrue(self.q1.exists())

    def test_missing_copy_review_refused_when_named(self):
        f = self.q2 / "th.md"
        f.write_text(f.read_text(encoding="utf-8").replace("copy_review: iris 2026-11-13\n", ""), encoding="utf-8")
        with self.assertRaises(SystemExit) as cm:
            pp.publish(self.root, "second-up", now=NOW)
        self.assertIn("th.md", str(cm.exception))
        self.assertTrue(self.q2.exists())

    def test_no_complete_post_is_a_noop_for_daily(self):
        (self.q1 / "id.md").unlink()
        (self.q2 / "id.md").unlink()
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(pp.main(["--daily", "--root", str(self.root), "--no-build"]), 0)
        self.assertIn("no reviewed post in the queue", out.getvalue())
        self.assertTrue(self.q1.exists() and self.q2.exists())


class CopyReview(unittest.TestCase):
    def setUp(self):
        self.root = make_site(posts=(("old-post", "2026-11-02T19:00+09:00"),), queue=("first-up", "second-up"), unreviewed=("first-up",))
        self.addCleanup(shutil.rmtree, self.root, True)

    def unstamp_review(self, slug, lang):
        f = self.root / "content/queue" / ("01-" + slug if slug == "first-up" else "02-" + slug) / ("%s.md" % lang)
        f.write_text(f.read_text(encoding="utf-8").replace("copy_review: iris 2026-11-13\n", ""), encoding="utf-8")

    def test_named_unreviewed_slug_refused_and_names_the_file(self):
        with self.assertRaises(SystemExit) as cm:
            pp.publish(self.root, "first-up", now=NOW)
        self.assertIn("copy_review", str(cm.exception))
        self.assertIn("en.md", str(cm.exception))
        self.assertIn("ko.md", str(cm.exception))
        self.assertTrue((self.root / "content/queue/01-first-up").exists())

    def test_named_slug_with_one_language_unreviewed_refused(self):
        self.unstamp_review("second-up", "ko")
        with self.assertRaises(SystemExit) as cm:
            pp.publish(self.root, "second-up", now=NOW)
        self.assertIn("ko.md", str(cm.exception))
        self.assertNotIn("en.md", str(cm.exception))

    def test_unnamed_publish_skips_unreviewed_head(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            slug, when, _ = pp.publish(self.root, now=NOW)
        self.assertEqual(slug, "second-up")
        self.assertIn("skip first-up", err.getvalue())
        self.assertTrue((self.root / "content/queue/01-first-up").exists())

    def test_no_reviewed_post_is_a_clean_noop_for_daily(self):
        self.unstamp_review("second-up", "en")
        self.unstamp_review("second-up", "ko")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(pp.main(["--daily", "--root", str(self.root), "--no-build"]), 0)
        self.assertIn("no reviewed post in the queue — nothing to publish", out.getvalue())
        self.assertTrue((self.root / "content/queue/01-first-up").exists())
        self.assertTrue((self.root / "content/queue/02-second-up").exists())
        self.assertFalse((self.root / "content/journal/second-up").exists())

    def test_no_reviewed_post_refused_for_manual_publish(self):
        self.unstamp_review("second-up", "en")
        with self.assertRaises(SystemExit) as cm:
            pp.publish(self.root, now=NOW)
        self.assertIn("no reviewed post in the queue — nothing to publish", str(cm.exception))

    def test_copy_review_line_is_carried_into_journal_and_builds_clean(self):
        slug, when, _ = pp.publish(self.root, "second-up", now=NOW)
        for l in ("en", "ko"):
            t = (self.root / ("content/journal/second-up/%s.md" % l)).read_text(encoding="utf-8")
            self.assertIn("copy_review: iris 2026-11-13\n", t)
            self.assertIn("published: 2026-11-12T20:00+09:00", t)
        _, errs = bs.load_posts(self.root, NOW)
        self.assertEqual(errs, [])


if __name__ == "__main__":
    unittest.main()
