"""ops/publish_daily.sh safety rules, run against a throw-away origin + publish clone (no network, no real check.sh)."""
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import helpers
from helpers import REPO

SCRIPT = REPO / "ops" / "publish_daily.sh"
PAST = "2026-10-01T19:00+09:00"


def git(cwd, *args, check=True):
    return subprocess.run(["git", *args], cwd=cwd, check=check, capture_output=True, text=True,
                          env={**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"})


class PublishDaily(unittest.TestCase):
    def setUp(self):
        site = helpers.make_site(posts=(("alpha-post", PAST),), queue=("next-one", "next-two"))
        self.addCleanup(shutil.rmtree, site, True)
        shutil.copytree(REPO / "scripts", site / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
        # The real repo ignores __pycache__; without it, CI's Python (which writes bytecode next to the scripts the
        # publish run imports) leaves an untracked scripts/__pycache__ and the "unexpected paths" guard rolls back.
        shutil.copy(REPO / ".gitignore", site / ".gitignore")
        shutil.copytree(REPO / "vendor" / "ipe_web_kit", site / "vendor" / "ipe_web_kit", dirs_exist_ok=True)
        helpers.build(site)
        self.tmp = Path(tempfile.mkdtemp(prefix="claimball-pd-"))
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.origin = self.tmp / "origin.git"
        git(self.tmp, "init", "-q", "--bare", "-b", "main", str(self.origin))
        self.clone = site
        git(site, "init", "-q", "-b", "main")
        git(site, "add", "-A")
        git(site, "commit", "-q", "-m", "init")
        git(site, "remote", "add", "origin", str(self.origin))
        git(site, "push", "-q", "origin", "main")
        self.check_cmd = "true"

    def run_script(self, check_cmd=None, publish_dir=None):
        env = {**os.environ, "CLAIMBALL_PUBLISH_DIR": str(publish_dir or self.clone), "CLAIMBALL_CHECK_CMD": check_cmd or self.check_cmd,
               "CLAIMBALL_SKIP_NET": "1", "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
        return subprocess.run(["bash", str(SCRIPT)], capture_output=True, text=True, env=env)

    def head(self, cwd=None):
        return git(cwd or self.clone, "rev-parse", "HEAD").stdout.strip()

    def origin_head(self):
        return git(self.origin, "rev-parse", "main").stdout.strip()

    def test_publishes_and_pushes_only_the_publish_set(self):
        r = self.run_script()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(self.head(), self.origin_head())
        self.assertTrue((self.clone / "content/journal/next-one/en.md").is_file())
        self.assertFalse((self.clone / "content/queue/01-next-one").exists())
        self.assertIn("journal: publish next-one", git(self.clone, "log", "-1", "--format=%s").stdout)
        self.assertEqual(git(self.clone, "status", "--porcelain").stdout, "")

    def test_second_run_same_day_is_a_noop(self):
        self.run_script()
        before = self.origin_head()
        r = self.run_script()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(self.origin_head(), before)

    def test_skips_when_not_on_main(self):
        git(self.clone, "checkout", "-q", "-b", "feature/x")
        before = self.head()
        r = self.run_script()
        self.assertEqual(r.returncode, 0)
        self.assertIn("SKIP", r.stdout)
        self.assertEqual(self.head(), before)
        self.assertEqual(self.origin_head(), before)
        self.assertTrue((self.clone / "content/queue/01-next-one").is_dir())

    def test_skips_when_tree_is_dirty(self):
        (self.clone / "wip.txt").write_text("work in progress")
        r = self.run_script()
        self.assertEqual(r.returncode, 0)
        self.assertIn("SKIP", r.stdout)
        self.assertTrue((self.clone / "content/queue/01-next-one").is_dir())
        self.assertEqual(git(self.clone, "log", "--oneline").stdout.count("\n"), 1)

    def test_failed_green_gate_rolls_back_the_queue_move(self):
        before = self.head()
        r = self.run_script(check_cmd="false")
        self.assertEqual(r.returncode, 1)
        self.assertIn("ROLLBACK", r.stdout)
        self.assertEqual(self.head(), before)
        self.assertEqual(git(self.clone, "status", "--porcelain").stdout, "")
        self.assertTrue((self.clone / "content/queue/01-next-one").is_dir())
        self.assertFalse((self.clone / "content/journal/next-one").exists())
        # no stamp left behind: the next run (gate green again) publishes the same post today
        r = self.run_script()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertTrue((self.clone / "content/journal/next-one/en.md").is_file())

    def test_failed_build_rolls_back(self):
        q = self.clone / "content/queue/01-next-one/en.md"
        q.write_text(q.read_text().replace("Body of", "See /Users/someone/secret. Body of"), encoding="utf-8")
        git(self.clone, "commit", "-qam", "bad post")
        git(self.clone, "push", "-q", "origin", "main")
        before = self.head()
        r = self.run_script()
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertEqual(self.head(), before)
        self.assertEqual(git(self.clone, "status", "--porcelain").stdout, "")
        self.assertTrue((self.clone / "content/queue/01-next-one").is_dir())

    def test_unexpected_path_aborts_and_rolls_back(self):
        # a check command that drops a stray file simulates something touching the tree outside the publish set
        r = self.run_script(check_cmd="echo stray > stray.txt")
        self.assertEqual(r.returncode, 1)
        self.assertIn("unexpected paths", r.stdout)
        self.assertFalse((self.clone / "stray.txt").exists())
        self.assertTrue((self.clone / "content/queue/01-next-one").is_dir())

    def test_commit_failure_rolls_back_the_staged_tree(self):
        hook = self.clone / ".git" / "hooks" / "pre-commit"
        hook.write_text("#!/bin/sh\nexit 1\n")
        hook.chmod(0o755)
        before = self.head()
        r = self.run_script()
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("ROLLBACK", r.stdout)
        self.assertEqual(self.head(), before)
        self.assertEqual(git(self.clone, "status", "--porcelain").stdout, "")
        self.assertTrue((self.clone / "content/queue/01-next-one").is_dir())
        hook.unlink()
        r = self.run_script()  # not stuck: the next run publishes normally
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertTrue((self.clone / "content/journal/next-one/en.md").is_file())

    def test_sigterm_during_the_gate_rolls_back(self):
        before = self.head()
        r = self.run_script(check_cmd="kill -TERM $PPID")
        self.assertEqual(r.returncode, 143, r.stdout + r.stderr)
        self.assertIn("ROLLBACK", r.stdout)
        self.assertEqual(self.head(), before)
        self.assertEqual(git(self.clone, "status", "--porcelain").stdout, "")
        self.assertTrue((self.clone / "content/queue/01-next-one").is_dir())

    def test_second_run_while_locked_is_skipped_and_the_lock_is_released_after_a_run(self):
        lock = self.clone / ".git" / "publish.lock"
        lock.mkdir()
        (lock / "pid").write_text(str(os.getpid()))  # a live process
        before = self.head()
        r = self.run_script()
        self.assertEqual(r.returncode, 0)
        self.assertIn("another publish run is in progress", r.stdout)
        self.assertTrue((self.clone / "content/queue/01-next-one").is_dir())
        self.assertEqual(self.head(), before)
        self.assertTrue(lock.is_dir())  # not ours: untouched
        shutil.rmtree(lock)
        r = self.run_script()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertFalse(lock.exists())

    def test_stale_lock_of_a_dead_process_is_taken_over(self):
        dead = subprocess.Popen(["true"])
        dead.wait()
        lock = self.clone / ".git" / "publish.lock"
        lock.mkdir()
        (lock / "pid").write_text(str(dead.pid))
        r = self.run_script()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("stale lock", r.stdout)
        self.assertTrue((self.clone / "content/journal/next-one/en.md").is_file())
        self.assertFalse(lock.exists())

    def test_lock_is_released_after_a_failed_run(self):
        self.run_script(check_cmd="false")
        self.assertFalse((self.clone / ".git" / "publish.lock").exists())

    def test_git_never_prompts_for_credentials(self):
        out = self.tmp / "env.txt"
        r = self.run_script(check_cmd='echo "$GIT_TERMINAL_PROMPT" > %s' % out)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(out.read_text().strip(), "0")

    def test_empty_queue_warns_loudly_and_exits_zero(self):
        shutil.rmtree(self.clone / "content" / "queue")
        git(self.clone, "add", "-A")
        git(self.clone, "commit", "-qm", "queue consumed")
        git(self.clone, "push", "-q", "origin", "main")
        r = self.run_script()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("QUEUE_EMPTY", r.stdout)
        self.assertEqual(git(self.clone, "status", "--porcelain").stdout, "")

    def test_low_queue_is_logged_with_the_count(self):
        r = self.run_script()  # fixture queues 2 posts
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("QUEUE_LOW 2", r.stdout)

    def test_comfortable_queue_is_not_flagged(self):
        q = self.clone / "content" / "queue"
        for n in (3, 4):
            d = q / ("0%d-extra-%d" % (n, n))
            d.mkdir()
            for lang in ("en", "ko"):
                (d / (lang + ".md")).write_text(helpers.post_text("extra-%d" % n, lang, "Queued extra %d %s" % (n, lang)), encoding="utf-8")
        git(self.clone, "add", "-A")
        git(self.clone, "commit", "-qm", "more queue")
        git(self.clone, "push", "-q", "origin", "main")
        r = self.run_script()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn("QUEUE_LOW", r.stdout)

    def test_unpushed_commit_outside_the_publish_set_is_not_pushed(self):
        (self.clone / "wip.txt").write_text("not for publication")
        git(self.clone, "add", "wip.txt")
        git(self.clone, "commit", "-qm", "wip")
        before = self.origin_head()
        r = self.run_script()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("SKIP", r.stdout)
        self.assertIn("wip.txt", r.stdout)
        self.assertEqual(self.origin_head(), before)
        self.assertTrue((self.clone / "content/queue/01-next-one").is_dir())

    def test_failing_rollback_is_logged_loudly_and_still_releases_the_lock(self):
        # an index.lock makes `git reset --hard` fail, simulating a rollback that cannot complete
        r = self.run_script(check_cmd="touch .git/index.lock; false")
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("ROLLBACK FAILED", r.stdout)
        self.assertFalse((self.clone / ".git" / "publish.lock").exists())
        # same through the EXIT trap (error after the gate, e.g. SIGTERM)
        (self.clone / ".git" / "index.lock").unlink()
        git(self.clone, "reset", "-q", "--hard")
        git(self.clone, "clean", "-fdq")
        r = self.run_script(check_cmd="touch .git/index.lock; kill -TERM $PPID")
        self.assertEqual(r.returncode, 143, r.stdout + r.stderr)
        self.assertIn("ROLLBACK FAILED", r.stdout)
        self.assertFalse((self.clone / ".git" / "publish.lock").exists())

    def test_failed_push_is_retried_by_the_next_run_even_with_nothing_to_publish(self):
        hook = self.origin / "hooks" / "pre-receive"
        hook.write_text("#!/bin/sh\nexit 1\n")
        hook.chmod(0o755)
        r = self.run_script()
        self.assertEqual(r.returncode, 1)
        self.assertIn("commit kept locally", r.stdout)
        ahead = git(self.clone, "rev-list", "--count", "origin/main..HEAD").stdout.strip()
        self.assertEqual(ahead, "1")
        hook.unlink()
        r = self.run_script()  # today already has a post: nothing new, but the leftover commit goes out
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("unpushed", r.stdout)
        self.assertEqual(self.head(), self.origin_head())

    def test_not_a_clone_is_skipped(self):
        r = self.run_script(publish_dir=self.tmp)
        self.assertEqual(r.returncode, 0)
        self.assertIn("SKIP", r.stdout)


class OpsFiles(unittest.TestCase):
    def test_deploy_workflow_settings(self):
        y = (REPO / ".github" / "workflows" / "deploy.yml").read_text(encoding="utf-8")
        self.assertIn("cancel-in-progress: false", y)
        self.assertNotIn("cancel-in-progress: true", y)
        check = y.split("  check:")[1].split("  deploy:")[0]
        self.assertIn("permissions:\n      contents: read", check)

    def test_plist_template_has_no_personal_paths_and_renders(self):
        t = (REPO / "ops" / "rest.ipe.claimball-publish.plist.template").read_text(encoding="utf-8")
        self.assertNotIn("/Users/", t)
        self.assertIn("<key>Hour</key><integer>18</integer>", t)
        self.assertIn("__HOME__/Library/Logs/claimball-publish.log", t)
        self.assertIn("CLAIMBALL_PUBLISH_DIR", t)
        self.assertIn("<key>GIT_TERMINAL_PROMPT</key><string>0</string>", t)
        tmp = Path(tempfile.mkdtemp(prefix="claimball-ld-"))
        self.addCleanup(shutil.rmtree, tmp, True)
        env = {**os.environ, "CLAIMBALL_LAUNCH_AGENTS_DIR": str(tmp / "LA"), "CLAIMBALL_HOME": str(tmp / "home")}
        r = subprocess.run(["bash", str(REPO / "ops" / "install_launchd.sh")], capture_output=True, text=True, env=env)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        out = (tmp / "LA" / "rest.ipe.claimball-publish.plist").read_text(encoding="utf-8")
        self.assertNotIn("__HOME__", out)
        self.assertIn(str(tmp / "home" / "Library" / "Logs" / "claimball-publish.log"), out)
        self.assertIn(str(tmp / "home" / "Developer" / "claimball-rest" / "ops" / "publish_daily.sh"), out)
        if shutil.which("plutil"):
            self.assertEqual(subprocess.run(["plutil", "-lint", str(tmp / "LA" / "rest.ipe.claimball-publish.plist")], capture_output=True).returncode, 0)

    def test_install_rejects_unsafe_home_values(self):
        tmp = Path(tempfile.mkdtemp(prefix="claimball-ld-"))
        self.addCleanup(shutil.rmtree, tmp, True)
        for bad in ("relative/home", "/a\\b", "/a\nb", "/a#b", "/a&b", "/a|b", ""):
            env = {**os.environ, "CLAIMBALL_LAUNCH_AGENTS_DIR": str(tmp / "LA"), "CLAIMBALL_HOME": bad}
            if bad == "":
                env.pop("CLAIMBALL_HOME")
                env["HOME"] = "relative"
            r = subprocess.run(["bash", str(REPO / "ops" / "install_launchd.sh")], capture_output=True, text=True, env=env)
            self.assertEqual(r.returncode, 1, (bad, r.stdout, r.stderr))
            self.assertIn("HOME", r.stderr, bad)  # rejected by our own check, not by a later failure
            self.assertFalse((tmp / "LA" / "rest.ipe.claimball-publish.plist").exists(), bad)

    def test_template_comment_does_not_contain_the_placeholder(self):
        t = (REPO / "ops" / "rest.ipe.claimball-publish.plist.template").read_text(encoding="utf-8")
        comment = t.split("<!--")[1].split("-->")[0]
        self.assertNotIn("__HOME__", comment)

    def test_no_personal_absolute_paths_in_the_repo(self):
        """Public repo: no /Users/<name>/ or /home/<name>/ anywhere except files that deliberately name the forbidden string."""
        import re
        pat = re.compile(r"/(Users|home)/[A-Za-z0-9._-]+/")
        skip_dirs = {".git", "__pycache__", "node_modules"}
        allowed = {"docs/TRANSLATION.md", "scripts/build_site.py"}
        bad = []
        for p in REPO.rglob("*"):
            rel = p.relative_to(REPO)
            if not p.is_file() or skip_dirs & set(rel.parts) or rel.parts[0] == "tests" or rel.as_posix() in allowed:
                continue
            if p.suffix in (".png", ".jpg", ".jpeg", ".ico"):
                continue
            try:
                text = p.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if pat.search(text):
                bad.append(rel.as_posix())
        self.assertEqual(bad, [])


if __name__ == "__main__":
    unittest.main()
