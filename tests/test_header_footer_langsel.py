"""Header and footer of every generated page: no Privacy/Terms in the header nav, both in the footer, the language
switch is a <select> (current language selected, values are real pages) with a same-page link list for no-JS and crawlers,
and the hreflang alternates are unchanged (one per language that has the page, plus x-default)."""
import re
import unittest

from helpers import REPO, bs

SKIP_DIRS = ("tests", "scripts", "docs", "ops", "content", "assets", "vendor", ".github")
LANG_DIRS = [l for l in bs.LANGS if l != "en"]


def pages():
    out = []
    for p in sorted(REPO.rglob("*.html")):
        rel = p.relative_to(REPO)
        if rel.parts[0] in SKIP_DIRS:
            continue
        text = p.read_text(encoding="utf-8")
        if 'http-equiv="refresh"' in text:
            continue
        out.append((str(rel), text))
    return out


def lang_of(rel):
    first = rel.split("/")[0]
    return first if first in LANG_DIRS else "en"


def page_exists(value):
    path = value.split("?")[0].strip("/")
    return (REPO / path / "index.html" if path else REPO / "index.html").is_file()


def unprefixed_dir(f):
    parts = f.split("/")[:-1]
    if parts and parts[0] in LANG_DIRS:
        parts = parts[1:]
    return parts


class HeaderFooterLangSelect(unittest.TestCase):
    def test_header_nav_has_no_privacy_or_terms_and_footer_has_both_once(self):
        found = 0
        for f, h in pages():
            nav = re.search(r'<nav class="nav".*?</nav>', h, re.S)
            self.assertIsNotNone(nav, f)
            page_links = re.sub(r'<span class="langsw">.*?</span>', "", nav.group(0), flags=re.S)
            self.assertIsNone(re.search(r'href="[^"]*/(privacy|terms)/"', page_links), f)
            foot = re.search(r'<nav class="foot-links".*?</nav>', h, re.S)
            self.assertIsNotNone(foot, f)
            for name in ("privacy", "terms"):
                self.assertEqual(len(re.findall(r'href="[^"]*/%s/"' % name, foot.group(0))), 1, (f, name))
            found += 1
        self.assertGreater(found, 150)

    def test_select_has_twelve_options_one_selected_and_real_targets(self):
        for f, h in pages():
            lang = lang_of(f)
            sels = re.findall(r'<select id="langsel" class="langsel">(.*?)</select>', h, re.S)
            self.assertEqual(len(sels), 1, f)
            opts = re.findall(r'<option value="([^"]*)" lang="([\w-]+)"( selected)?>([^<]*)</option>', sels[0])
            self.assertEqual([o[1] for o in opts], list(bs.LISTED), f)
            self.assertEqual([o[3] for o in opts], [bs.LANGS[l][0] for l in bs.LISTED], f)
            self.assertEqual([o[1] for o in opts if o[2]], [lang] if lang in bs.LISTED else [], f)
            for value, _, _, _ in opts:
                self.assertTrue(value.startswith("/"), (f, value))
                self.assertTrue(page_exists(value), (f, value))

    def test_select_options_match_the_same_page_links_for_crawlers(self):
        for f, h in pages():
            header = re.search(r'<header.*?</header>', h, re.S).group(0)
            noscript = re.search(r'<noscript><style>\.langsel\{display:none\}</style>(.*?)</noscript>', header, re.S)
            self.assertIsNotNone(noscript, f)
            links = re.findall(r'<a href="([^"]*)" hreflang="([\w-]+)"', noscript.group(1))
            sel = re.search(r'<select id="langsel".*?</select>', header, re.S).group(0)
            options = re.findall(r'<option value="([^"]*)" lang="([\w-]+)"', sel)
            self.assertEqual([(v, l) for v, l in options], [(h_, l) for h_, l in links], f)

    def test_hreflang_alternates_are_unchanged(self):
        for f, h in pages():
            head = re.search(r"<head>.*?</head>", h, re.S).group(0)
            alts = re.findall(r'<link rel="alternate" hreflang="([\w-]+)" href="([^"]*)">', head)
            if f == "404.html" or re.search(r"/page/\d+/index\.html$", f):
                self.assertEqual(alts, [], f)
                continue
            page = unprefixed_dir(f)
            have = [l for l in bs.LISTED if (REPO.joinpath(*([] if l == "en" else [l]), *page, "index.html")).is_file()]
            if len(have) > 1:
                self.assertEqual(sorted(l for l, _ in alts), sorted(have + ["x-default"]), f)
            else:
                self.assertEqual(alts, [], f)
            self.assertNotIn("?lang=", "".join(href for _, href in alts), f)


if __name__ == "__main__":
    unittest.main()
