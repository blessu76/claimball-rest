"""ops/publish_gate.py: random afternoon slot, never the same hour as yesterday, date rollover, already-published ignored."""
import json
import os
import random
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from helpers import REPO

GATE = REPO / "ops" / "publish_gate.py"


class Gate(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="claimball-gate-"))
        self.slot = self.tmp / "q" / "slot.json"
        self.marker = self.tmp / "ran"

    def run_gate(self, now, cmd=None, seed="1"):
        cmd = cmd or "echo ran >> %s; echo 'publish_daily: pushed x'" % self.marker
        env = {**os.environ, "CLAIMBALL_SLOT_FILE": str(self.slot), "CLAIMBALL_NOW": now, "CLAIMBALL_PUBLISH_CMD": cmd, "CLAIMBALL_SEED": seed}
        return subprocess.run([sys.executable, str(GATE)], env=env, capture_output=True, text=True, check=True).stdout

    def state(self):
        return json.loads(self.slot.read_text())

    def put(self, **kw):
        self.slot.parent.mkdir(parents=True, exist_ok=True)
        self.slot.write_text(json.dumps(kw))

    def test_draw_in_window_and_excludes_yesterdays_hour(self):
        sys.path.insert(0, str(REPO / "ops"))
        import publish_gate
        for prev_hour in range(12, 18):
            for seed in range(60):
                t = publish_gate.draw_time("%02d:30" % prev_hour, random.Random(seed))
                h, m = map(int, t.split(":"))
                self.assertTrue(12 <= h <= 17 and 0 <= m <= 59, t)
                self.assertNotEqual(h, prev_hour)

    def test_new_day_rolls_slot_and_moves_yesterday_to_prev(self):
        self.put(date="2026-11-12", time="15:20", prev_date=None, prev_time=None, published=True)
        self.run_gate("2026-11-13 11:00")
        st = self.state()
        self.assertEqual((st["date"], st["prev_date"], st["prev_time"], st["published"]), ("2026-11-13", "2026-11-12", "15:20", False))
        self.assertNotEqual(st["time"].split(":")[0], "15")
        self.assertFalse(self.marker.exists())  # before the slot: nothing runs

    def test_runs_once_at_or_after_slot_then_ignores(self):
        self.put(date="2026-11-13", time="14:10", prev_date="2026-11-12", prev_time="16:00", published=False)
        self.run_gate("2026-11-13 14:00"); self.assertFalse(self.marker.exists())
        self.run_gate("2026-11-13 14:15"); self.assertEqual(self.marker.read_text().count("ran"), 1)
        self.assertTrue(self.state()["published"])
        self.run_gate("2026-11-13 14:30"); self.assertEqual(self.marker.read_text().count("ran"), 1)

    def test_already_published_is_ignored(self):
        self.put(date="2026-11-13", time="12:00", prev_date=None, prev_time=None, published=True)
        self.run_gate("2026-11-13 17:00")
        self.assertFalse(self.marker.exists())

    def test_skip_or_failure_keeps_unpublished_for_retry(self):
        self.put(date="2026-11-13", time="12:00", prev_date=None, prev_time=None, published=False)
        self.run_gate("2026-11-13 13:00", cmd="echo 'publish_daily: SKIP — working tree is not clean'")
        self.assertFalse(self.state()["published"])
        self.run_gate("2026-11-13 13:15", cmd="exit 1")
        self.assertFalse(self.state()["published"])


if __name__ == "__main__":
    unittest.main()
