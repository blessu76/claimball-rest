"""All 12 kit languages are really built, linked to each other, and keep the privacy wording."""
import html
import json
import re
import unittest
from pathlib import Path

from helpers import REPO, bs

ALL = ("en", "ko", "ja", "zh-Hant", "es", "pt-BR", "fr", "de", "id", "th", "vi", "tr")
GAOPTOUT = "https://tools.google.com/dlpage/gaoptout"


def out(lang, *parts):
    base = REPO if lang == "en" else REPO / lang
    return base.joinpath(*parts, "index.html")


def text_of(lang, *parts):
    return html.unescape(out(lang, *parts).read_text(encoding="utf-8"))


class LanguageSet(unittest.TestCase):
    def test_the_registry_is_the_twelve_languages(self):
        self.assertEqual(tuple(bs.LISTED), ALL)
        self.assertEqual(bs.MAIN_LANGS, ("en", "ko"))

    def test_every_language_has_source_files(self):
        for l in ALL:
            self.assertTrue((REPO / "content" / "i18n" / (l + ".json")).is_file(), l)
            for slug in bs.PAGE_SLUGS:
                self.assertTrue((REPO / "content" / "pages" / l / (slug + ".md")).is_file(), (l, slug))
            self.assertTrue((REPO / "content" / "journal" / "starting-claimball" / (l + ".md")).is_file(), l)

    def test_i18n_keys_match_english(self):
        en = json.loads((REPO / "content" / "i18n" / "en.json").read_text(encoding="utf-8"))
        for l in ALL:
            d = json.loads((REPO / "content" / "i18n" / (l + ".json")).read_text(encoding="utf-8"))
            self.assertEqual(set(d), set(en), l)
            self.assertTrue(all(isinstance(v, str) and v.strip() for v in d.values()), l)
            self.assertEqual(d["hero_h1"].count("|"), 1, l)

    def test_landmark_aria_labels_are_translated(self):
        """main / footer / breadcrumb / pagination / posts navs take their aria-label from i18n, not from English literals."""
        en = json.loads((REPO / "content" / "i18n" / "en.json").read_text(encoding="utf-8"))
        keys = ("aria_main", "aria_footer", "aria_breadcrumb", "aria_pagination", "aria_posts")
        for l in ALL:
            d = json.loads((REPO / "content" / "i18n" / (l + ".json")).read_text(encoding="utf-8"))
            self.assertEqual(len({d[k] for k in keys}), len(keys), l)
            if l != "en":
                self.assertGreaterEqual(sum(d[k] != en[k] for k in keys), 4, l)  # fr "Pagination" may coincide with English
            page = text_of(l, "journal", "starting-claimball")
            for k, cls in (("aria_main", 'class="nav"'), ("aria_footer", 'class="foot-links"'), ("aria_breadcrumb", 'class="crumbs"')):
                self.assertIn('<nav %s aria-label="%s"' % (cls, d[k]), page, (l, k))
            if l != "en":
                for lit in ("main", "footer", "breadcrumb", "pagination", "posts"):
                    self.assertNotIn('aria-label="%s"' % lit, page, (l, lit))

    def test_every_language_page_exists_in_the_output(self):
        for l in ALL:
            for parts in ((), ("about",), ("privacy",), ("support",), ("terms",), ("journal",),
                          ("journal", "starting-claimball")):
                self.assertTrue(out(l, *parts).is_file(), (l, parts))

    def test_html_lang_matches(self):
        for l in ALL:
            self.assertIn('<html lang="%s"' % l, out(l).read_text(encoding="utf-8"), l)

    def test_every_language_is_left_to_right(self):
        for l in ALL:
            for parts in ((), ("about",), ("privacy",), ("journal", "starting-claimball")):
                self.assertIn('<html lang="%s" dir="ltr"' % l, out(l, *parts).read_text(encoding="utf-8"), (l, parts))

    def test_hreflang_covers_all_languages_and_x_default(self):
        for l in ALL:
            page = out(l, "about").read_text(encoding="utf-8")
            tags = re.findall(r'<link rel="alternate" hreflang="([^"]+)"', page)
            self.assertEqual(sorted(tags), sorted(ALL + ("x-default",)), l)

    def test_sitemap_lists_every_language_home(self):
        sm = (REPO / "sitemap.xml").read_text(encoding="utf-8")
        for l in ALL:
            if l == "en":
                continue
            self.assertIn("https://claimball.ipe.rest/%s/</loc>" % l, sm, l)

class RightToLeft(unittest.TestCase):
    CSS = (REPO / "assets" / "claimball.css").read_text(encoding="utf-8")

    def test_no_physical_left_right_in_the_text_layout(self):
        # the illustration (.board / .net / .paddle / .ball) is positioned physically on purpose and sits in a direction:ltr box
        text_part = self.CSS.split("/* phone mock-up")[0] + self.CSS.split("/* sections + cards */")[1]
        for bad in ("padding-left", "padding-right", "margin-left", "margin-right", "border-left", "border-right", "text-align:left", "text-align:right", "left:-999px"):
            self.assertNotIn(bad, text_part, bad)
        self.assertRegex(self.CSS, r"\.phone\{direction:ltr;")

    def test_back_arrows_point_left_in_english(self):
        self.assertEqual((bs.arrow("en", False), bs.arrow("en", True)), ("\u2190", "\u2192"))
        self.assertIn("\u2190 " + json.loads((REPO / "content" / "i18n" / "en.json").read_text(encoding="utf-8"))["back_journal"],
                      text_of("en", "journal", "starting-claimball"))

    def test_the_language_switcher_lists_every_language(self):
        page = text_of("ja", "about")
        for l in ALL:
            self.assertIn('hreflang="%s"' % l, page)


class PrivacyWording(unittest.TestCase):
    def test_privacy_keeps_ga4_and_icloud_text(self):
        for l in ALL:
            t = text_of(l, "privacy")
            self.assertIn("Google Analytics", t, l)
            self.assertIn("_ga", t, l)
            self.assertIn(GAOPTOUT, t, l)
            self.assertIn("iCloud", t, l)
            self.assertIn("claimball.ipe.rest", t, l)

    def test_support_keeps_the_ga_and_icloud_faq(self):
        for l in ALL:
            t = text_of(l, "support")
            self.assertIn("Google Analytics", t, l)
            self.assertIn("iCloud", t, l)
            self.assertIn("/privacy/", out(l, "support").read_text(encoding="utf-8"), l)

    def test_brand_name_is_never_translated(self):
        for l in ALL:
            self.assertIn("Claimball", text_of(l, "about"), l)

    def test_translations_point_to_the_original(self):
        for l in ALL:
            if l in bs.MAIN_LANGS:
                continue
            for slug in bs.PAGE_SLUGS:
                src = (REPO / "content" / "pages" / l / (slug + ".md")).read_text(encoding="utf-8")
                self.assertIn("translation_of: en", src, (l, slug))


class InternalLinks(unittest.TestCase):
    def test_markdown_links_keep_the_language_prefix(self):
        for l in ALL:
            if l == "en":
                continue
            files = list((REPO / "content" / "pages" / l).glob("*.md")) + [REPO / "content" / "journal" / "starting-claimball" / (l + ".md")]
            for f in files:
                for href in re.findall(r"\]\((/[^)]*)\)", f.read_text(encoding="utf-8")):
                    self.assertTrue(href.startswith("/%s/" % l), (f.name, href))


if __name__ == "__main__":
    unittest.main()
