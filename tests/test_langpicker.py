"""Language picker: on every built page of every language the picker shows that page's own language
(aria-current, <html lang>), and a saved choice ("cb-lang") sends "/" to that language."""
import json
import re
import shutil
import subprocess
import unittest

from helpers import REPO, bs

LANG_DIRS = [l for l in bs.LANGS if l != "en"]
AVAILABLE = [l for l in bs.LISTED if l != "en"]
SKIP_DIRS = ("tests", "scripts", "docs", "ops", "content", "assets") + tuple(bs.LEGACY_REDIRECTS)


def pages():
    out = []
    for p in REPO.rglob("index.html"):
        rel = p.relative_to(REPO).parts
        if rel[0] in SKIP_DIRS:
            continue
        lang = rel[0] if rel[0] in LANG_DIRS else "en"
        text = p.read_text(encoding="utf-8")
        if 'http-equiv="refresh"' in text:
            continue
        out.append((lang, str(p.relative_to(REPO)), text))
    return out


def switch(h):
    return re.search(r'<select id="langsel" class="langsel">(.*?)</select>', h, re.S).group(1)


def switch_options(h):
    return re.findall(r'<option value="([^"]*)" lang="([\w-]+)"( selected)?>', switch(h))


class Picker(unittest.TestCase):
    def test_every_language_folder_has_pages(self):
        self.assertEqual({l for l, _, _ in pages()}, set(bs.LANGS))

    def test_picker_shows_the_pages_own_language(self):
        for lang, f, h in pages():
            name = bs.LANGS[lang][0]
            self.assertEqual(re.search(r'<html lang="([\w-]+)"', h).group(1), lang, f)
            opts = switch_options(h)
            self.assertEqual([l for _, l, _ in opts], list(bs.LISTED), f)
            self.assertEqual([l for _, l, sel in opts if sel], [lang] if lang in bs.LISTED else [], f)

    def test_picker_links_stay_on_the_same_page(self):
        for lang, f, h in pages():
            for href, l, _ in switch_options(h):
                self.assertEqual(href.startswith("/" + l + "/") or (l == "en" and not href.startswith(tuple("/" + x + "/" for x in LANG_DIRS))), True, (f, href))

    @unittest.skipUnless(shutil.which("node"), "node required")
    def test_choice_is_remembered_for_each_language(self):
        """pick a language in the switch -> claimball.js stores it -> langpick.js on '/' goes to it (en + ko)."""
        js = (REPO / "assets" / "claimball.js").read_text(encoding="utf-8")
        pick = (REPO / "assets" / "langpick.js").read_text(encoding="utf-8").replace("/*SUPPORTED*/[]", json.dumps(list(bs.LISTED))).replace("/*AVAILABLE*/[]", json.dumps(AVAILABLE))
        prog = r"""
const store={};
function run(src,pathname,navLangs){
  const listeners={};let to=null;
  const ctx={localStorage:{getItem:k=>store[k]===undefined?null:store[k],setItem:(k,v)=>{store[k]=String(v)}},
    navigator:{languages:navLangs,language:navLangs[0]},
    location:{pathname,search:'',hash:'',replace:u=>{to=u}},
    document:{querySelector:()=>null,addEventListener:(t,f)=>{if(!listeners[t])listeners[t]=f}},window:{}};
  new Function('localStorage','navigator','location','document','window',src)(ctx.localStorage,ctx.navigator,ctx.location,ctx.document,ctx.window);
  return {listeners,to};
}
const out=[];
for(const l of %s){
  for(const k in store)delete store[k];
  const sel={classList:{contains:c=>c==='langsel'},value:'/'+l+'/',options:[{getAttribute:n=>n==='lang'?l:null}],selectedIndex:0};
  const {listeners}=run(%s,'/%s/',['en-US']);
  listeners.change({target:sel});
  const r=run(%s,'/',['en-US']);
  out.push([l,store['cb-lang'],r.to]);
}
console.log(JSON.stringify(out));
""" % (json.dumps(list(bs.LISTED)), json.dumps(js), "x", json.dumps(pick))
        res = subprocess.run(["node", "-e", prog], capture_output=True, text=True, timeout=30)
        self.assertEqual(res.returncode, 0, res.stderr)
        for l, saved, to in json.loads(res.stdout):
            self.assertEqual(saved, l)
            self.assertEqual(to, None if l == "en" else "/%s/" % l, l)


    def test_english_user_links_carry_lang_en_but_metadata_does_not(self):
        """From a non-English page every user link to the English root pins ?lang=en (blocked storage / middle click would otherwise bounce
        back to the browser language); on English pages nothing changes; hreflang / canonical / og:url / x-default never carry it."""
        seen = 0
        for lang, f, h in pages():
            head = re.search(r"<head>.*?</head>", h, re.S).group(0)
            self.assertNotIn("?lang=", head, f)
            others = re.search(r'<aside class="langs">.*?</aside>', h, re.S)
            links = [(href, l) for href, l, _ in switch_options(h)]
            links += re.findall(r'<a href="([^"]*)" hreflang="(\w+)"', re.search(r'<header.*?</header>', h, re.S).group(0))
            links += re.findall(r'<a href="([^"]*)" hreflang="(\w+)"', others.group(0) if others else "")
            for href, l in links:
                if l == "en" and lang != "en":
                    seen += 1
                    self.assertTrue(href.endswith("?lang=en"), (f, href))
                    self.assertEqual(href.count("?"), 1, (f, href))
                else:
                    self.assertNotIn("?lang=", href, (f, href))
            # AI-translation "read the original" link: only the English original needs the pin
            note = re.search(r'<p class="ai-note">.*?<a href="([^"]*)"', h, re.S)
            if note:
                self.assertEqual("?lang=en" in note.group(1), not note.group(1).startswith("/ko/"), (f, note.group(1)))
            # no other link on any page may carry ?lang= except the English pin
            for href in re.findall(r'href="([^"]*\?lang=[^"]*)"', h):
                self.assertTrue(href.endswith("?lang=en") and lang != "en", (f, href))
        self.assertGreater(seen, 100)

    def test_sitemap_and_llms_have_no_lang_param(self):
        for name in ("sitemap.xml", "llms.txt"):
            self.assertNotIn("?lang=", (REPO / name).read_text(encoding="utf-8"), name)

    @unittest.skipUnless(shutil.which("node"), "node required")
    def test_en_link_from_ja_stays_english_without_storage(self):
        """/ja/about/ -> EN link -> langpick.js on /about/?lang=en with navigator.languages=['ja'] and localStorage throwing: no redirect."""
        h = (REPO / "ja/about/index.html").read_text(encoding="utf-8")
        href = re.search(r'<a href="([^"]*)" hreflang="en"', re.search(r'<header.*?</header>', h, re.S).group(0)).group(1)
        self.assertEqual(href, "/about/?lang=en")
        pick = (REPO / "assets" / "langpick.js").read_text(encoding="utf-8").replace("/*SUPPORTED*/[]", json.dumps(list(bs.LISTED))).replace("/*AVAILABLE*/[]", json.dumps(AVAILABLE))
        prog = r"""
let to=null,hist=null;
const loc={pathname:'/about/',search:'?lang=en',hash:'',replace:u=>{to=u}};
const ls={getItem:()=>{throw new Error('blocked')},setItem:()=>{throw new Error('blocked')}};
new Function('localStorage','navigator','location','history',%s)(ls,{languages:['ja'],language:'ja'},loc,{replaceState:(a,b,u)=>{hist=u}});
console.log(JSON.stringify({to,hist}));
""" % json.dumps(pick)
        res = subprocess.run(["node", "-e", prog], capture_output=True, text=True, timeout=30)
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertEqual(json.loads(res.stdout), {"to": None, "hist": "/about/"})
        # the bare link is what bounced back: same page without ?lang=en goes to /ja/
        res = subprocess.run(["node", "-e", prog.replace("search:'?lang=en'", "search:''")], capture_output=True, text=True, timeout=30)
        self.assertEqual(json.loads(res.stdout)["to"], "/ja/about/")


@unittest.skipUnless(shutil.which("node"), "node required")
class RootLangParam(unittest.TestCase):
    """The company-wide order on "/": ?lang=xx > saved choice ("cb-lang") > browser language > English root."""

    KEY = "cb-lang"

    @classmethod
    def run_root(cls, search="", saved=None, nav=("en-US",), hash_="", pathname="/", langs=None, available=None, script=None):
        langs = list(langs or bs.LISTED)
        avail = [l for l in langs if l != "en"] if available is None else list(available)
        pick = script or (REPO / "assets" / "langpick.js").read_text(encoding="utf-8").replace("/*SUPPORTED*/[]", json.dumps(langs)).replace(
            "/*AVAILABLE*/[]", json.dumps(avail))
        prog = r"""
const store=%s;let to=null,replaced=null;const nav=%s;
const ctx={localStorage:{getItem:k=>store[k]===undefined?null:store[k],setItem:(k,v)=>{store[k]=String(v)}},
  navigator:{languages:nav,language:nav[0]},
  location:{pathname:%s,search:%s,hash:%s,replace:u=>{to=u}},
  history:{replaceState:(a,b,u)=>{replaced=u}}};
new Function('localStorage','navigator','location','history',%s)(ctx.localStorage,ctx.navigator,ctx.location,ctx.history);
console.log(JSON.stringify({to,replaced,store}));
""" % (json.dumps({} if saved is None else {cls.KEY: saved}), json.dumps(list(nav)), json.dumps(pathname), json.dumps(search), json.dumps(hash_), json.dumps(pick))
        res = subprocess.run(["node", "-e", prog], capture_output=True, text=True, timeout=30)
        assert res.returncode == 0, res.stderr
        return json.loads(res.stdout)

    def test_lang_ko_goes_to_ko_and_is_saved(self):
        r = self.run_root("?lang=ko")
        self.assertEqual((r["to"], r["store"].get(self.KEY)), ("/ko/", "ko"))

    def test_lang_ko_beats_saved_en_and_browser(self):
        r = self.run_root("?lang=ko", saved="en", nav=("en-US",))
        self.assertEqual((r["to"], r["store"][self.KEY]), ("/ko/", "ko"))

    def test_lang_en_stays_on_root_saved_and_query_cleaned(self):
        r = self.run_root("?lang=en", saved="ko", nav=("ko-KR",))
        self.assertIsNone(r["to"])
        self.assertEqual((r["store"][self.KEY], r["replaced"]), ("en", "/"))

    def test_lang_unsupported_is_ignored_then_browser_language(self):
        r = self.run_root("?lang=ru", nav=("ko-KR", "en"))
        self.assertEqual((r["to"], self.KEY in r["store"]), ("/ko/", False))

    def test_lang_unsupported_falls_back_to_english(self):
        r = self.run_root("?lang=ru", nav=("it-IT",))
        self.assertEqual((r["to"], r["store"], r["replaced"]), (None, {}, None))

    def test_lang_unsupported_does_not_overwrite_saved(self):
        r = self.run_root("?lang=ru", saved="ko", nav=("en-US",))
        self.assertEqual((r["to"], r["store"][self.KEY]), ("/ko/", "ko"))

    def test_lang_param_is_normalised(self):
        for q in ("?lang=KO", "?lang=ko-KR", "?lang=ko_KR"):
            self.assertEqual(self.run_root(q)["to"], "/ko/", q)

    def test_lang_is_removed_but_other_query_and_hash_survive(self):
        r = self.run_root("?utm_source=play&lang=ko&x=1", hash_="#how")
        self.assertEqual(r["to"], "/ko/?utm_source=play&x=1#how")
        r = self.run_root("?utm_source=play&lang=en", hash_="#how")
        self.assertEqual((r["to"], r["replaced"]), (None, "/?utm_source=play#how"))

    def test_saved_choice_beats_browser_language(self):
        self.assertEqual(self.run_root(saved="ko", nav=("en-US",))["to"], "/ko/")
        self.assertIsNone(self.run_root(saved="en", nav=("ko-KR",))["to"])

    def test_browser_language_in_order_and_region_stripped(self):
        self.assertEqual(self.run_root(nav=("ko-KR", "en-US"))["to"], "/ko/")
        self.assertIsNone(self.run_root(nav=("en-US", "ko-KR"))["to"])
        self.assertEqual(self.run_root(nav=("it-IT", "ko"))["to"], "/ko/")

    def test_unsupported_browser_language_stays_english(self):
        r = self.run_root(nav=("ru-RU", "it"))
        self.assertEqual((r["to"], r["store"]), (None, {}))

    def test_inner_pages_move_to_the_same_page(self):
        self.assertEqual(self.run_root("?lang=ko", pathname="/about/")["to"], "/ko/about/")
        r = self.run_root("?x=1&lang=ja", pathname="/journal/", hash_="#h")
        self.assertEqual(r["to"], "/ja/journal/?x=1#h")
        self.assertEqual(self.run_root(saved="de", pathname="/about/")["to"], "/de/about/")
        self.assertEqual(self.run_root(nav=("vi-VN",), pathname="/support/")["to"], "/vi/support/")

    def test_ended_languages_never_redirect(self):
        self.assertIsNone(self.run_root(nav=("ar-SA", "en"))["to"])
        self.assertIsNone(self.run_root(nav=("hi-IN",), pathname="/about/")["to"])
        self.assertIsNone(self.run_root(nav=("ru-RU",))["to"])
        self.assertIsNone(self.run_root(nav=("zh-CN",))["to"])
        r = self.run_root("?lang=HI")
        self.assertIsNone(r["to"])
        self.assertNotIn(self.KEY, r["store"])
        self.assertEqual(self.run_root(saved="ar", nav=("en-US",), pathname="/about/")["to"], None)

    def test_chinese_and_portuguese_map_to_kit_tags(self):
        self.assertEqual(self.run_root(nav=("zh-TW",))["to"], "/zh-Hant/")
        self.assertEqual(self.run_root(nav=("zh-HK", "en"), pathname="/about/")["to"], "/zh-Hant/about/")
        self.assertEqual(self.run_root(nav=("zh-Hant-TW",))["to"], "/zh-Hant/")
        self.assertIsNone(self.run_root(nav=("zh-CN",))["to"])
        self.assertEqual(self.run_root(nav=("pt-PT",))["to"], "/pt-BR/")
        self.assertEqual(self.run_root("?lang=pt", pathname="/journal/", hash_="#x")["to"], "/pt-BR/journal/#x")
        self.assertEqual(self.run_root(nav=("in-ID",))["to"], "/id/")

    def test_never_runs_under_a_language_prefix(self):
        for path in ("/ko/", "/ko/about/", "/en/", "/KO/journal/", "/zh-Hant/", "/pt-BR/about/"):
            r = self.run_root("?lang=de", saved="ja", nav=("fr-FR",), pathname=path)
            self.assertEqual((r["to"], r["store"], r["replaced"]), (None, {"cb-lang": "ja"}, None), path)

    def test_stays_when_the_page_has_no_counterpart(self):
        # /journal/post/ has only ko and ja: de is a supported language but the visitor stays (no fallback to the next browser language)
        kw = dict(pathname="/journal/post/", available=["ko", "ja"])
        self.assertEqual(self.run_root(nav=("ko-KR",), **kw)["to"], "/ko/journal/post/")
        self.assertIsNone(self.run_root(nav=("de-DE", "ko"), **kw)["to"])
        r = self.run_root("?lang=de&a=1", **kw)
        self.assertEqual((r["to"], r["store"][self.KEY], r["replaced"]), (None, "de", "/journal/post/?a=1"))
        self.assertIsNone(self.run_root(saved="de", nav=("ko-KR",), **kw)["to"])

    def test_adding_a_language_needs_only_the_list(self):
        self.assertEqual(self.run_root("?lang=th", langs=["en", "ko", "th"])["to"], "/th/")

    @staticmethod
    def built_script(f):
        m = re.search(r"<script>(\(function\(\)\{var S=.*?)</script>", f.read_text(encoding="utf-8"), re.S)
        return m.group(1) if m else None

    def test_inlined_on_every_prefixless_page_and_nowhere_else(self):
        for f in REPO.rglob("*.html"):
            rel = f.relative_to(REPO).parts
            if rel[0] in SKIP_DIRS:
                continue
            has = self.built_script(f) is not None
            self.assertEqual(has, rel[0] not in LANG_DIRS and rel[0] != "404.html", str(f.relative_to(REPO)))
        root = self.built_script(REPO / "index.html")
        self.assertIn("history.replaceState", root)
        self.assertNotIn("/*AVAILABLE*/", root)
        self.assertNotIn(bs.LANGPICK_MARK, "".join(f.read_text(encoding="utf-8") for f in REPO.rglob("*.html") if "tests" not in f.parts))

    def test_each_page_lists_exactly_the_languages_that_have_it(self):
        for f in REPO.rglob("index.html"):
            rel = f.relative_to(REPO)
            if rel.parts[0] in LANG_DIRS + list(SKIP_DIRS):
                continue
            have = [l for l in AVAILABLE if (REPO / l / rel).exists()]
            a = json.loads(re.search(r"A=(\[[^\]]*\])", self.built_script(f)).group(1))
            self.assertEqual(a, have, str(rel))

    def test_built_script_on_an_inner_page_redirects(self):
        for rel, path in (("about/index.html", "/about/"), ("journal/index.html", "/journal/")):
            script = self.built_script(REPO / rel)
            self.assertEqual(self.run_root(nav=("ko-KR",), pathname=path, script=script)["to"], "/ko%s" % path, rel)
            self.assertIsNone(self.run_root(nav=("en-US",), pathname=path, script=script)["to"], rel)


if __name__ == "__main__":
    unittest.main()
