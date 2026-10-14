#!/usr/bin/env python3
"""Sprawdza zbudowaną stronę (strona/public):
1. czy każdy link wewnętrzny (href/src) prowadzi do istniejącego pliku,
2. czy kotwice (#id) istnieją na stronie docelowej,
3. (opcjonalnie) błędy parsowania HTML5 – jeśli zainstalowano html5lib.

Użycie: python3 strona/narzedzia/sprawdz.py [katalog_public] [--base /]
Kod wyjścia 1, gdy są błędy linków.
"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
pub = Path(sys.argv[1]) if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else ROOT / "public"
site = json.loads((ROOT / "dane" / "site.json").read_text(encoding="utf-8"))
import os
for k in ("DOMENA", "BASE_PATH"):
    if os.environ.get("SITE_" + k):
        site[k] = os.environ["SITE_" + k]
base = site["BASE_PATH"]
if "--base" in sys.argv:
    base = sys.argv[sys.argv.index("--base") + 1]
base = "/" + base.strip("/") + "/" if base.strip("/") else "/"
domena = site["DOMENA"].rstrip("/")


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids = [], set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        for k in ("href", "src", "action"):
            if a.get(k):
                self.links.append((tag, k, a[k]))


pages = {}
for f in pub.rglob("*.html"):
    p = P()
    p.feed(f.read_text(encoding="utf-8"))
    pages[f.resolve()] = p


def resolve(src: Path, url: str):
    parts = urlsplit(url)
    path = unquote(parts.path)
    if not path:
        return src, parts.fragment
    if path.startswith("/"):
        if not path.startswith(base):
            return None, None
        rel = path[len(base):]
        target = pub / rel
    else:
        target = (src.parent / path)
    if str(target).endswith("/") or target.is_dir():
        target = target / "index.html"
    return target.resolve(), parts.fragment


bledy, sprawdzone, zewn = [], 0, set()
for src, p in pages.items():
    for tag, attr, url in p.links:
        if url.startswith(("mailto:", "tel:", "javascript:", "data:")):
            continue
        if url.startswith(domena):
            url = url[len(domena):] or "/"
        if re.match(r"^[a-z]+://", url):
            zewn.add(url)
            continue
        if attr == "action":
            continue
        sprawdzone += 1
        target, frag = resolve(src, url)
        rel = src.relative_to(pub.resolve())
        if target is None:
            bledy.append(f"{rel}: link poza BASE_PATH: {url}")
        elif not target.exists():
            bledy.append(f"{rel}: brak pliku dla {url}")
        elif frag and target.suffix == ".html" and frag not in pages[target].ids:
            bledy.append(f"{rel}: brak kotwicy #{frag} w {target.relative_to(pub.resolve())}")

# sitemap
sm = (pub / "sitemap.xml").read_text(encoding="utf-8")
for loc in re.findall(r"<loc>(.*?)</loc>", sm):
    t, _ = resolve(pub / "index.html", loc[len(domena):])
    sprawdzone += 1
    if not t or not t.exists():
        bledy.append(f"sitemap.xml: brak pliku dla {loc}")

print(f"Stron HTML: {len(pages)}, sprawdzonych linków wewnętrznych: {sprawdzone}, unikalnych zewnętrznych: {len(zewn)}")
if bledy:
    print(f"BŁĘDY LINKÓW ({len(bledy)}):")
    for b in bledy:
        print("  - " + b)
else:
    print("Linki wewnętrzne: OK (0 błędów)")

try:
    import html5lib
except ImportError:
    html5lib = None
    print("html5lib niedostępny – pomijam walidację HTML5 (pip install html5lib)")
if html5lib:
    nbl = 0
    for f in sorted(pages):
        parser = html5lib.HTMLParser(strict=False)
        parser.parse(f.read_bytes(), transport_encoding="utf-8")
        errs = [e for e in parser.errors]
        if errs:
            nbl += len(errs)
            print(f"  HTML5 {f.relative_to(pub.resolve())}: {len(errs)} błędów parsowania, np. {errs[0]}")
    print(f"Walidacja HTML5 (html5lib): {'OK (0 błędów parsowania)' if nbl == 0 else str(nbl) + ' błędów'}")

sys.exit(1 if bledy else 0)
