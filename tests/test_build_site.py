"""build_site: structure, policy rules (banned words, emoji, no price / ratings), SEO output, content swap-in from iltonggi."""
import datetime as dt
import re
import shutil
import unittest
from pathlib import Path

from helpers import NOW, REPO, bs, build, jsonld, make_site

PAGES = ["", "about/", "privacy/", "support/", "terms/", "journal/"]


class Built(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = make_site()
        cls.ctx = build(cls.root)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.root, True)

    def read(self, rel):
        return (self.root / rel).read_text(encoding="utf-8")

    def test_every_required_page_exists_in_both_languages(self):
        for lang_dir in ("", "ko/"):
            for p in PAGES:
                self.assertTrue((self.root / (lang_dir + p) / "index.html").is_file(), lang_dir + p)
        self.assertTrue((self.root / "404.html").is_file())

    def test_only_fully_translated_languages_are_built(self):
        self.assertEqual(self.ctx.langs, ["en", "ko"])

    def test_real_content_builds_every_listed_language(self):
        ctx, errs = bs.make_ctx(REPO)
        self.assertEqual(errs, [])
        self.assertEqual(ctx.langs, list(bs.LISTED))

    def test_last_updated_on_every_page(self):
        for lang_dir in ("", "ko/"):
            for p in PAGES:
                h = self.read(lang_dir + p + "index.html")
                self.assertRegex(h, r'<p class="updated">[^<]+: <time datetime="\d{4}-\d{2}-\d{2}">\d{4}-\d{2}-\d{2}</time></p>', lang_dir + p)
        self.assertIn('class="updated"', self.read("404.html"))

    def test_hreflang_and_canonical(self):
        h = self.read("index.html")
        self.assertIn('<link rel="canonical" href="https://claimball.ipe.rest/">', h)
        for l, pth in (("en", "/"), ("ko", "/ko/"), ("x-default", "/")):
            self.assertIn('hreflang="%s" href="https://claimball.ipe.rest%s"' % (l, pth), h)
        self.assertIn('<html lang="ko"', self.read("ko/index.html"))

    def test_404_is_noindex_without_canonical(self):
        h = self.read("404.html")
        self.assertIn("noindex", h)
        self.assertNotIn('rel="canonical"', h)

    def test_cache_busting_and_design_tokens(self):
        h = self.read("index.html")
        self.assertIn("/assets/claimball.css?v=%s" % bs.ASSET_V, h)
        self.assertIn("/assets/claimball.js?v=%s" % bs.ASSET_V, h)
        css = (REPO / "assets" / "claimball.css").read_text(encoding="utf-8")
        for token in ("--paper:#FBF8EE", "--ink:#1B2540", "--blue:#2B5FD9", "--orange:#FFA726", "--chalk:#1F2B27", "--font-head", "--font-body"):
            self.assertIn(token, css)
        self.assertIn("Caveat+Brush", h)
        self.assertIn("Nunito", h)

    def test_language_picker_on_every_prefixless_page_but_not_under_a_language_or_404(self):
        for rel in ("index.html", "about/index.html", "journal/index.html"):
            self.assertIn("cb-lang", self.read(rel), rel)
        for rel in ("ko/index.html", "ko/about/index.html", "404.html"):
            self.assertNotIn("cb-lang", self.read(rel), rel)

    def test_store_badges_are_not_links(self):
        for lang_dir in ("", "ko/"):
            h = self.read(lang_dir + "index.html")
            badges = re.findall(r'<span class="store">.*?</b></span>', h, re.S)
            self.assertEqual(len(badges), 4, lang_dir)  # hero + cta, two stores each
            for b in badges:
                self.assertNotIn("<a ", b)
        self.assertNotIn("apps.apple.com", self.read("index.html"))
        self.assertNotIn("play.google.com", self.read("index.html"))

    def test_json_ld_game_has_no_offers_or_ratings(self):
        for graph in jsonld(self.read("index.html")):
            for node in graph["@graph"]:
                if node.get("@type") == "VideoGame":
                    for bad in ("offers", "aggregateRating", "review", "datePublished"):
                        self.assertNotIn(bad, node)
        self.assertNotIn("aggregateRating", "".join(str(jsonld(self.read(p + "index.html"))) for p in PAGES))

    def test_post_page(self):
        h = self.read("journal/alpha-post/index.html")
        self.assertIn("BlogPosting", h)
        self.assertIn('hreflang="ko" href="https://claimball.ipe.rest/ko/journal/alpha-post/"', h)

    def test_sitemap_robots_llms_feed(self):
        sm = self.read("sitemap.xml")
        for pth in ("/", "/ko/", "/about/", "/ko/terms/", "/support/", "/journal/", "/journal/beta-post/"):
            self.assertIn("<loc>https://claimball.ipe.rest%s</loc>" % pth, sm)
        self.assertNotIn("/404", sm)
        self.assertIn("Sitemap: https://claimball.ipe.rest/sitemap.xml", self.read("robots.txt"))
        for bot in ("GPTBot", "ClaudeBot", "PerplexityBot"):
            self.assertIn("User-agent: %s" % bot, self.read("robots.txt"))
        llms = self.read("llms.txt")
        self.assertIn("NOT been released", llms)
        self.assertIn("https://claimball.ipe.rest/journal/beta-post/", llms)
        self.assertIn("<rss", self.read("journal/feed.xml"))
        self.assertIn("<rss", self.read("ko/journal/feed.xml"))

    def test_policy_pages_are_claimball_with_iltonggi_contact(self):
        for lang_dir in ("", "ko/"):
            for slug in ("privacy", "terms", "support"):
                h = self.read("%s%s/index.html" % (lang_dir, slug))
                self.assertNotRegex(h.lower(), r"iltonggi|일통기|inkisle|weather|날씨")
                self.assertIn("ipe.haven@gmail.com", h)
        self.assertIn("Davy Kim (ipe Studio)", self.read("privacy/index.html"))
        self.assertIn("Claimball", self.read("terms/index.html"))

    def test_no_price_rating_or_banned_words_anywhere(self):
        for f in self.root.rglob("*.html"):
            if "assets" in f.parts:
                continue
            h = f.read_text(encoding="utf-8")
            text = re.sub(r"<script.*?</script>|<style.*?</style>", "", h, flags=re.S)
            self.assertIsNone(bs.BANNED_WORDS.search(text), f)
            self.assertIsNone(bs.EMOJI.search(text), f)
            self.assertNotRegex(text, r"[$€₩]\s?\d|\d\s?(?:USD|KRW|원)\b", str(f))
            self.assertNotRegex(text.lower(), r"\d+\+? (?:downloads|reviews|ratings)|(?:다운로드|리뷰|평점)\s?\d", str(f))

    def test_pricing_model_wording(self):
        # owner decision 2026-10-31: free to try + one purchase, no ads, no subscription, amount unannounced
        en, ko = self.read("index.html"), self.read("ko/index.html")
        self.assertEqual(en.count("Free to try. One purchase unlocks everything. No ads, no subscription."), 2)
        self.assertEqual(ko.count("무료로 해 보고, 한 번 결제하면 전부 열려요. 광고도 구독도 없어요."), 2)
        for p in ("about/", "support/"):
            self.assertIn("a single purchase unlocks the full game", self.read(p + "index.html"))
            self.assertIn("The price will be announced closer to launch.", self.read(p + "index.html"))
        for p in ("ko/about/", "ko/support/"):
            self.assertIn("한 번 결제하면 게임 전체가 열려요", self.read(p + "index.html"))
        self.assertIn("No ads, no subscription.", self.read("llms.txt"))
        for p in ("index.html", "ko/index.html", "llms.txt"):
            self.assertNotIn("Pricing will be announced", self.read(p))
            self.assertNotIn("가격은 출시가 가까워지면", self.read(p))

    def test_rival_names_are_not_on_the_site(self):
        # tentative names must never leak: the i18n/page sources only say "6 AI rivals, 2 leagues"
        for f in (REPO / "content").rglob("*"):
            if f.is_file() and f.suffix in (".json", ".md"):
                self.assertNotRegex(f.read_text(encoding="utf-8").lower(), r"league names|rival names", str(f))

    def test_board_is_six_by_ten(self):
        self.assertEqual(len(bs.BOARD), 10)
        self.assertTrue(all(len(r) == 6 for r in bs.BOARD))
        self.assertEqual(self.read("index.html").count('<i class="t'), 60)

    def test_no_horizontal_layout_hazards_in_markup(self):
        for f in self.root.rglob("*.html"):
            if "assets" in f.parts:
                continue
            self.assertIn('<meta name="viewport" content="width=device-width,initial-scale=1">', f.read_text(encoding="utf-8"))


class Rules(unittest.TestCase):
    def setUp(self):
        self.root = make_site()
        self.addCleanup(shutil.rmtree, self.root, True)

    def errs(self, now=NOW):
        return bs.make_ctx(self.root, now)[1]

    def test_clean_site_has_no_errors(self):
        self.assertEqual(self.errs(), [])

    def test_banned_word_rejected(self):
        for word in ("Pong", "핑퐁", "탁구"):
            f = self.root / "content" / "pages" / "en" / "about.md"
            f.write_text(f.read_text(encoding="utf-8") + "\nLike %s.\n" % word, encoding="utf-8")
            self.assertTrue(any("banned word" in e for e in self.errs()), word)
            f.write_text(f.read_text(encoding="utf-8").replace("\nLike %s.\n" % word, ""), encoding="utf-8")
        self.assertEqual(self.errs(), [])

    def test_emoji_rejected(self):
        f = self.root / "content" / "journal" / "alpha-post" / "en.md"
        f.write_text(f.read_text(encoding="utf-8") + "\nHooray \U0001F389\n", encoding="utf-8")
        self.assertTrue(any("emoji" in e for e in self.errs()))

    def test_secret_or_local_path_rejected(self):
        f = self.root / "content" / "pages" / "en" / "about.md"
        f.write_text(f.read_text(encoding="utf-8") + "\n/Users/someone/x\n", encoding="utf-8")
        self.assertTrue(any("forbidden text" in e for e in self.errs()))

    def test_future_post_rejected(self):
        self.assertTrue(any("future" in e for e in self.errs(dt.datetime(2026, 10, 1, tzinfo=bs.KST))))

    def test_missing_page_or_key_rejected(self):
        (self.root / "content" / "pages" / "ko" / "terms.md").unlink()
        self.assertTrue(any("en and ko must both be complete" in e for e in self.errs()))

    def test_page_needs_updated_date(self):
        f = self.root / "content" / "pages" / "en" / "privacy.md"
        f.write_text(re.sub(r"updated:.*\n", "", f.read_text(encoding="utf-8")), encoding="utf-8")
        self.assertTrue(any("missing updated" in e for e in self.errs()))

class Repo(unittest.TestCase):
    def test_cname_and_indexnow_key(self):
        self.assertEqual((REPO / "CNAME").read_text().strip(), "claimball.ipe.rest")
        keys = [p for p in REPO.glob("*.txt") if re.fullmatch(r"[0-9a-f]{32}\.txt", p.name) and p.name not in ("llms.txt",)]
        self.assertEqual(len(keys), 1)
        self.assertEqual(keys[0].read_text().strip(), keys[0].stem)
        self.assertNotEqual(keys[0].stem, "0f3a1c5e7b9d2a4c6e8f0b1d3a5c7e9f")  # placeholder guard; must never be inkisle's key

    def test_repo_has_no_planning_docs_or_inkisle_leftovers(self):
        self.assertFalse((REPO / "docs").exists())
        for p in (REPO / "scripts").glob("*"):
            if p.is_file():
                self.assertNotIn("inkisle", p.read_text(encoding="utf-8", errors="ignore").lower(), p.name)

    def test_publish_hour_is_18(self):
        self.assertIn("<integer>18</integer>", (REPO / "ops" / "rest.ipe.claimball-publish.plist.template").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
