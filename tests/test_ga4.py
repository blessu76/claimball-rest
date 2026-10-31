"""GA4: one snippet per generated page, and the privacy / FAQ / llms.txt text that must match it."""
import re
import shutil
import unittest

from helpers import build, bs, make_site

GA_ID = "G-XG4BH800J0"


class Ga4(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = make_site()
        build(cls.root)
        cls.pages = {str(p.relative_to(cls.root)): p.read_text(encoding="utf-8") for p in cls.root.rglob("*.html") if "assets" not in p.relative_to(cls.root).parts}

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.root, True)

    def test_constant_is_the_ipe_rest_property(self):
        self.assertEqual(bs.GA_MEASUREMENT_ID, GA_ID)

    def test_every_generated_page_has_the_snippet_once(self):
        self.assertGreater(len(self.pages), 15)
        for rel, text in self.pages.items():
            with self.subTest(rel):
                self.assertEqual(text.count(GA_ID), 1)
                self.assertEqual(text.count("googletagmanager.com/gtag/js"), 1)
                self.assertLess(text.index(GA_ID), text.index("</body>"))
                self.assertEqual(text.count("window.gtag('config',GA_ID)"), 1)
                self.assertNotIn("doubleclick", text)

    def test_no_snippet_outside_html(self):
        for rel in ("assets/claimball.js", "assets/claimball.css"):
            self.assertNotIn(GA_ID, (bs.Path(__file__).resolve().parent.parent / rel).read_text(encoding="utf-8"))

    def test_privacy_matches_the_tracking(self):
        for rel in ("privacy/index.html", "ko/privacy/index.html"):
            text = self.pages[rel]
            with self.subTest(rel):
                self.assertIn("Google Analytics", text)
                self.assertIn("_ga", text)
                self.assertIn("https://tools.google.com/dlpage/gaoptout", text)
                self.assertIn(bs.EFFECTIVE, text)

    def test_no_stale_no_tracking_claims_about_the_site(self):
        stale = re.compile(r"no analytics or advertising tags|uses no cookies|neither the app nor the website|"
                           r"쿠키를 사용하지 않|분석 도구나 광고 태그를 넣지|앱과 웹사이트 모두 개인정보를 수집하지", re.I)
        for rel in ("privacy/index.html", "ko/privacy/index.html", "support/index.html", "ko/support/index.html"):
            with self.subTest(rel):
                self.assertIsNone(stale.search(self.pages[rel]))

    def test_support_faq_and_llms_mention_google_analytics(self):
        for rel in ("support/index.html", "ko/support/index.html"):
            self.assertIn("Google Analytics", self.pages[rel])
        text = (bs.Path(__file__).resolve().parent.parent / "llms.txt").read_text(encoding="utf-8")
        self.assertIn("basic visit statistics through Google Analytics", text)

    def test_app_is_still_described_as_analytics_free(self):
        self.assertIn("no analytics", self.pages["privacy/index.html"].lower())


if __name__ == "__main__":
    unittest.main()
