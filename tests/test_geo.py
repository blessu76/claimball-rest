"""GEO: every journal page carries valid JSON-LD (BlogPosting + VideoGame + FAQPage), social meta, a short answer; sitemap/feed/llms/robots serve AI crawlers."""
import json
import re
import shutil
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from helpers import NOW, REPO, bs, build, make_site

LD = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)


def graph_of(html):
    blocks = LD.findall(html)
    assert len(blocks) == 1, "expected exactly one JSON-LD block"
    return json.loads(blocks[0].replace("<\\/", "</"))["@graph"]


class Fixture(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = make_site()
        cls.ctx = build(cls.root)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.root, True)

    def read(self, rel):
        return (self.root / rel).read_text(encoding="utf-8")

    def test_post_graph(self):
        g = {n["@type"]: n for n in graph_of(self.read("journal/alpha-post/index.html"))}
        post = g["BlogPosting"]
        for k in ("headline", "author", "datePublished", "dateModified", "inLanguage", "image", "mainEntityOfPage", "about", "abstract"):
            self.assertIn(k, post)
        self.assertEqual(g["VideoGame"]["genre"], ["Sports", "Casual"])
        self.assertIn("iOS", g["VideoGame"]["gamePlatform"])
        faq = g["FAQPage"]["mainEntity"]
        self.assertEqual([q["name"] for q in faq], ["Is it a question?", "And another?"])
        self.assertEqual(faq[1]["acceptedAnswer"]["text"], "Yes, really.")

    def test_korean_faq_uses_korean_heading(self):
        g = {n["@type"]: n for n in graph_of(self.read("ko/journal/alpha-post/index.html"))}
        self.assertEqual(len(g["FAQPage"]["mainEntity"]), 2)

    def test_visible_summary_and_meta(self):
        h = self.read("journal/alpha-post/index.html")
        self.assertIn('<p class="summary"><strong>In short:</strong> Short answer', h)
        self.assertIn('<h2>FAQ</h2>', h)
        self.assertIn('class="about-game"', h)
        for needle in ('property="article:published_time"', 'property="article:modified_time"', 'name="twitter:card"', 'property="og:image"',
                       'rel="canonical"', 'hreflang="x-default"', 'rel="alternate" type="application/rss+xml"'):
            self.assertIn(needle, h)

    def test_original_without_summary_or_faq_is_rejected(self):
        d = self.root / "content" / "journal" / "alpha-post"
        en = d / "en.md"
        orig = en.read_text(encoding="utf-8")
        try:
            en.write_text(re.sub(r"^summary:.*\n", "", orig, flags=re.M), encoding="utf-8")
            _, errs = bs.make_ctx(self.root, NOW)
            self.assertTrue(any("summary" in e for e in errs), errs)
            en.write_text(orig.split("## FAQ")[0], encoding="utf-8")
            _, errs = bs.make_ctx(self.root, NOW)
            self.assertTrue(any("FAQ" in e for e in errs), errs)
        finally:
            en.write_text(orig, encoding="utf-8")

    def test_faq_items_parser(self):
        body = "## Intro\n\ntext\n\n## FAQ\n\n### Q1?\n\nA1 **bold**.\n\n### Q2?\n\nA2 [x](http://a).\n\n## After\n\n### not faq\n\nno"
        self.assertEqual(bs.faq_items(body, "FAQ"), [("Q1?", "A1 bold."), ("Q2?", "A2 x.")])


class RealSite(unittest.TestCase):
    """The committed site (generated files in the repo root)."""

    def listing_pages(self):
        return [f for f in REPO.glob("**/journal/index.html") if "vendor" not in f.parts and f.parts[len(REPO.parts)] != "pt"]  # pt/ = legacy redirect stubs

    def post_pages(self):
        return [f for f in REPO.glob("**/journal/*/index.html") if f.parent.name != "page" and "vendor" not in f.parts and f.parts[len(REPO.parts)] != "pt"]  # pt/ = legacy redirect stubs

    def test_every_journal_page_json_ld_parses(self):
        files = self.listing_pages() + self.post_pages() + [f for f in REPO.glob("**/journal/page/*/index.html") if f.parts[len(REPO.parts)] != "pt"]
        self.assertGreater(len(files), 20)
        for f in files:
            self.assertTrue(graph_of(f.read_text(encoding="utf-8")), f)

    def test_every_post_page_has_blogposting_game_and_og(self):
        posts = self.post_pages()
        self.assertGreater(len(posts), 11)
        for f in posts:
            h = f.read_text(encoding="utf-8")
            self.assertTrue({"BlogPosting", "VideoGame"} <= {n["@type"] for n in graph_of(h)}, f)
            for needle in ("og:title", "twitter:card", 'rel="canonical"'):
                self.assertIn(needle, h, f)

    def test_en_ko_posts_have_faqpage_and_summary(self):
        for lang_dir in ("journal", "ko/journal"):
            for f in (REPO / lang_dir).glob("*/index.html"):
                if f.parent.name == "page":
                    continue
                h = f.read_text(encoding="utf-8")
                self.assertIn('class="summary"', h, f)
                self.assertIn("FAQPage", [n["@type"] for n in graph_of(h)], f)

    def test_sitemap_has_journal_and_every_post(self):
        sm = (REPO / "sitemap.xml").read_text(encoding="utf-8")
        ET.fromstring(sm)
        self.assertIn("<loc>https://claimball.ipe.rest/journal/</loc>", sm)
        for d in (REPO / "content" / "journal").iterdir():
            self.assertIn("<loc>https://claimball.ipe.rest/journal/%s/</loc>" % d.name, sm)
        self.assertRegex(sm, r"<loc>https://claimball.ipe.rest/journal/[a-z0-9-]+/</loc><lastmod>\d{4}-\d{2}-\d{2}</lastmod>")

    def test_feeds_are_valid_and_linked(self):
        for rel, lang in (("journal/feed.xml", "en"), ("ko/journal/feed.xml", "ko")):
            root = ET.fromstring((REPO / rel).read_text(encoding="utf-8"))
            self.assertEqual(root.tag, "rss")
            items = root.findall("./channel/item")
            self.assertGreaterEqual(len(items), 11)
            for it in items:
                self.assertTrue(it.findtext("link") and it.findtext("pubDate") and it.findtext("description"))
            html = (REPO / rel.replace("feed.xml", "index.html")).read_text(encoding="utf-8")
            self.assertIn('type="application/rss+xml"', html)

    def test_llms_txt_lists_journal(self):
        t = (REPO / "llms.txt").read_text(encoding="utf-8")
        self.assertIn("/journal/", t)
        self.assertIn("/journal/feed.xml", t)
        for d in (REPO / "content" / "journal").iterdir():
            self.assertIn("/journal/%s/" % d.name, t)

    def test_robots_does_not_block_ai_crawlers(self):
        t = (REPO / "robots.txt").read_text(encoding="utf-8")
        blocks = re.split(r"\n\s*\n", t)
        for bot in ("GPTBot", "ClaudeBot", "PerplexityBot", "Google-Extended", "OAI-SearchBot"):
            b = [x for x in blocks if "User-agent: %s" % bot in x]
            self.assertTrue(b, bot)
            self.assertNotIn("Disallow", b[0])
        self.assertNotRegex(t, r"(?m)^Disallow:\s*/\s*$")

    def test_home_links_to_journal(self):
        for p in ("index.html", "ko/index.html"):
            h = (REPO / p).read_text(encoding="utf-8")
            self.assertRegex(h, r'href="(/ko)?/journal/"')
            self.assertRegex(h, r'href="(/ko)?/journal/[a-z0-9-]+/"')


if __name__ == "__main__":
    unittest.main()
