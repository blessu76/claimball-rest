"""All 11 languages are really built, linked to each other, and keep the privacy wording."""
import html
import json
import re
import unittest
from pathlib import Path

from helpers import REPO, bs

ALL = ("en", "ko", "ja", "zh", "es", "pt", "id", "ru", "vi", "fr", "de")
GAOPTOUT = "https://tools.google.com/dlpage/gaoptout"


def out(lang, *parts):
    base = REPO if lang == "en" else REPO / lang
    return base.joinpath(*parts, "index.html")


def text_of(lang, *parts):
    return html.unescape(out(lang, *parts).read_text(encoding="utf-8"))


class LanguageSet(unittest.TestCase):
    def test_the_registry_is_the_eleven_languages(self):
        self.assertEqual(tuple(bs.LANGS), ALL)
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

    def test_every_language_page_exists_in_the_output(self):
        for l in ALL:
            for parts in ((), ("about",), ("privacy",), ("support",), ("terms",), ("journal",),
                          ("journal", "starting-claimball"), ("releases",)):
                self.assertTrue(out(l, *parts).is_file(), (l, parts))

    def test_html_lang_matches(self):
        for l in ALL:
            self.assertIn('<html lang="%s"' % l, out(l).read_text(encoding="utf-8"), l)

    def test_hreflang_covers_all_languages_and_x_default(self):
        for l in ALL:
            page = out(l, "about").read_text(encoding="utf-8")
            tags = re.findall(r'<link rel="alternate" hreflang="([^"]+)"', page)
            self.assertEqual(sorted(tags), sorted(ALL + ("x-default",)), l)

    def test_sitemap_lists_every_language_home_and_releases(self):
        sm = (REPO / "sitemap.xml").read_text(encoding="utf-8")
        for l in ALL:
            if l == "en":
                continue
            self.assertIn("https://claimball.ipe.rest/%s/</loc>" % l, sm, l)
            self.assertIn("https://claimball.ipe.rest/%s/releases/</loc>" % l, sm, l)

    def test_english_releases_path_is_kept(self):
        self.assertTrue((REPO / "releases" / "index.html").is_file())


class ReleasesPages(unittest.TestCase):
    def test_each_language_releases_page_shows_the_empty_state(self):
        for l in ALL:
            d = json.loads((REPO / "content" / "i18n" / (l + ".json")).read_text(encoding="utf-8"))
            self.assertIn(d["releases_empty"], text_of(l, "releases"), l)

    def test_app_link_targets_resolve(self):
        for l in ALL:
            if l != "en":
                self.assertTrue((REPO / l / "releases" / "index.html").is_file(), l)


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
