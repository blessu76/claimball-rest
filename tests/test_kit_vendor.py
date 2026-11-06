"""Web kit (vendor/ipe_web_kit, installed from the lock, see test_kit_lock.py): indexnow comes from it; the deploy never publishes it."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import indexnow  # noqa: E402


class KitVendor(unittest.TestCase):
    def test_indexnow_comes_from_vendor(self):
        self.assertEqual(indexnow.find_key.__module__, "ipe_web_kit.indexnow")

    def test_deploy_does_not_publish_vendor(self):
        wf = (ROOT / ".github" / "workflows" / "deploy.yml").read_text(encoding="utf-8")
        self.assertRegex(wf, r"--exclude='vendor'")
        self.assertIn("uses: ./.github/actions/ipe-web-kit", wf)


if __name__ == "__main__":
    unittest.main()
