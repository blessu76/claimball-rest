"""Language picker: on every built page of every language the picker shows that page's own language
(aria-current, <html lang>), and a saved choice ("cb-lang") sends "/" to that language."""
import json
import re
import shutil
import subprocess
import unittest

from helpers import REPO, bs

LANG_DIRS = [l for l in bs.LANGS if l != "en"]


def pages():
    out = []
    for p in REPO.rglob("index.html"):
        rel = p.relative_to(REPO).parts
        if rel[0] in ("tests", "scripts", "docs", "ops", "content", "assets"):
            continue
        lang = rel[0] if rel[0] in LANG_DIRS else "en"
        out.append((lang, str(p.relative_to(REPO)), p.read_text(encoding="utf-8")))
    return out


class Picker(unittest.TestCase):
    def test_both_languages_have_pages(self):
        self.assertEqual({l for l, _, _ in pages()}, set(bs.LANGS))

    def test_picker_shows_the_pages_own_language(self):
        for lang, f, h in pages():
            name = bs.LANGS[lang][0]
            self.assertEqual(re.search(r'<html lang="([\w-]+)"', h).group(1), lang, f)
            menu = re.search(r'<span class="langsw".*?</span>', h, re.S).group(0)
            cur = re.findall(r'<a href="[^"]*" hreflang="(\w+)"[^>]*aria-current', menu)
            self.assertEqual(cur, [lang], f)
            self.assertEqual(len(re.findall(r'<a ', menu)), len(bs.LANGS), f)

    def test_picker_links_stay_on_the_same_page(self):
        for lang, f, h in pages():
            menu = re.search(r'<span class="langsw".*?</span>', h, re.S).group(0)
            for href, l in re.findall(r'<a href="([^"]*)" hreflang="(\w+)"', menu):
                self.assertEqual(href.startswith("/" + l + "/") or (l == "en" and not href.startswith(tuple("/" + x + "/" for x in LANG_DIRS))), True, (f, href))

    @unittest.skipUnless(shutil.which("node"), "node required")
    def test_choice_is_remembered_for_each_language(self):
        """click a language -> claimball.js stores it -> langpick.js on '/' goes to it (en + ko)."""
        js = (REPO / "assets" / "claimball.js").read_text(encoding="utf-8")
        pick = (REPO / "assets" / "langpick.js").read_text(encoding="utf-8").replace("/*SUPPORTED*/[]", json.dumps(list(bs.LANGS)))
        prog = r"""
const store={};let hrefs=[];
function run(src,pathname,navLangs){
  let listener=null,to=null;
  const ctx={localStorage:{getItem:k=>store[k]===undefined?null:store[k],setItem:(k,v)=>{store[k]=String(v)}},
    navigator:{languages:navLangs,language:navLangs[0]},
    location:{pathname,search:'',hash:'',replace:u=>{to=u}},
    document:{querySelector:()=>null,addEventListener:(t,f)=>{if(t==='click'&&!listener)listener=f}},window:{}};
  new Function('localStorage','navigator','location','document','window',src)(ctx.localStorage,ctx.navigator,ctx.location,ctx.document,ctx.window);
  return {listener,to};
}
const out=[];
for(const l of %s){
  for(const k in store)delete store[k];
  const a={getAttribute:n=>n==='hreflang'?l:null};
  const {listener}=run(%s,'/%s/',['en-US']);
  listener({target:{closest:()=>a}});
  const r=run(%s,'/',['en-US']);
  out.push([l,store['cb-lang'],r.to]);
}
console.log(JSON.stringify(out));
""" % (json.dumps(list(bs.LANGS)), json.dumps(js), "x", json.dumps(pick))
        res = subprocess.run(["node", "-e", prog], capture_output=True, text=True, timeout=30)
        self.assertEqual(res.returncode, 0, res.stderr)
        for l, saved, to in json.loads(res.stdout):
            self.assertEqual(saved, l)
            self.assertEqual(to, None if l == "en" else "/%s/" % l, l)


@unittest.skipUnless(shutil.which("node"), "node required")
class RootLangParam(unittest.TestCase):
    """The company-wide order on "/": ?lang=xx > saved choice ("cb-lang") > browser language > English root."""

    KEY = "cb-lang"

    @classmethod
    def run_root(cls, search="", saved=None, nav=("en-US",), hash_="", pathname="/", langs=None):
        pick = (REPO / "assets" / "langpick.js").read_text(encoding="utf-8").replace("/*SUPPORTED*/[]", json.dumps(list(langs or bs.LANGS)))
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
        r = self.run_root("?lang=th", nav=("ko-KR", "en"))
        self.assertEqual((r["to"], self.KEY in r["store"]), ("/ko/", False))

    def test_lang_unsupported_falls_back_to_english(self):
        r = self.run_root("?lang=th", nav=("it-IT",))
        self.assertEqual((r["to"], r["store"], r["replaced"]), (None, {}, None))

    def test_lang_unsupported_does_not_overwrite_saved(self):
        r = self.run_root("?lang=th", saved="ko", nav=("en-US",))
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
        r = self.run_root(nav=("th-TH", "it"))
        self.assertEqual((r["to"], r["store"]), (None, {}))

    def test_only_the_root_is_handled(self):
        self.assertIsNone(self.run_root("?lang=ko", pathname="/about/")["to"])

    def test_adding_a_language_needs_only_the_list(self):
        self.assertEqual(self.run_root("?lang=th", langs=["en", "ko", "th"])["to"], "/th/")

    def test_inlined_on_the_root_page_only(self):
        root = (REPO / "index.html").read_text(encoding="utf-8")
        self.assertIn("lang", root.split("</head>")[0])
        self.assertIn("history.replaceState", root.split("</head>")[0])
        self.assertNotIn("history.replaceState", (REPO / "ko" / "index.html").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
