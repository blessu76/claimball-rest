"""Shared fixtures: a tiny repo-shaped folder (en + ko, one or two posts) in a temp dir."""
import datetime as dt
import json
import shutil
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
import build_site as bs  # noqa: E402

NOW = dt.datetime(2026, 11, 12, 20, 0, tzinfo=bs.KST)


def post_text(slug, lang, title, published=None, extra=""):
    pub = ("published: %s\n" % published) if published else ""
    tr = "translation_of: en\n" if lang not in bs.MAIN_LANGS else ""
    return ("---\ntitle: %s\ndescription: Desc of %s in %s.\nslug: %s\nlang: %s\ncategory: devlog\n%s%s%s---\n"
            "## Heading\n\nBody of **%s** with a [link](https://ipe.rest/) and `code`.\n") % (title, slug, lang, slug, lang, tr, pub, extra, slug)


def make_site(langs=("en", "ko"), posts=(("alpha-post", "2026-11-01T18:00+09:00"), ("beta-post", "2026-11-02T18:00+09:00")), queue=()):
    root = Path(tempfile.mkdtemp(prefix="claimball-test-"))
    for l in langs:
        (root / "content" / "i18n").mkdir(parents=True, exist_ok=True)
        shutil.copy(REPO / "content" / "i18n" / ("en.json" if l not in ("ko",) else "ko.json"), root / "content" / "i18n" / (l + ".json"))
        (root / "content" / "pages" / l).mkdir(parents=True, exist_ok=True)
        for slug in bs.PAGE_SLUGS:
            src = REPO / "content" / "pages" / ("ko" if l == "ko" else "en") / (slug + ".md")
            text = src.read_text(encoding="utf-8")
            if l not in bs.MAIN_LANGS:
                text = text.replace("description:", "translation_of: en\ndescription:", 1)
            (root / "content" / "pages" / l / (slug + ".md")).write_text(text, encoding="utf-8")
    for slug, pub in posts:
        d = root / "content" / "journal" / slug
        d.mkdir(parents=True)
        for l in langs:
            (d / (l + ".md")).write_text(post_text(slug, l, "Title %s %s" % (slug, l), pub), encoding="utf-8")
    for i, slug in enumerate(queue, start=1):
        d = root / "content" / "queue" / ("%02d-%s" % (i, slug))
        d.mkdir(parents=True)
        for l in ("en", "ko"):
            (d / (l + ".md")).write_text(post_text(slug, l, "Queued %s %s" % (slug, l)), encoding="utf-8")
    shutil.copytree(REPO / "assets", root / "assets")
    shutil.copytree(REPO / "vendor" / "ipe_web_kit", root / "vendor" / "ipe_web_kit")
    return root


def build(root, now=NOW):
    ctx, errs = bs.make_ctx(root, now)
    assert not errs, errs
    for rel, text in bs.build_all(ctx).items():
        f = Path(root) / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(text, encoding="utf-8")
    return ctx


def jsonld(html_text):
    import re
    out = []
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html_text, re.S):
        out.append(json.loads(m.group(1)))
    return out
