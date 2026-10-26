"""Sweep the wiki's error-tracking categories and compare each page with the same page on Wikipedia.

Usage (wiki running, job queue empty): python wiki/tools/error-sweep.py

For every page MediaWiki has filed in an error-tracking category here, checks whether the same page
on English Wikipedia is in the same category. "also on Wikipedia" means parity (Wikipedia's page shows
the same error); "only here" is a problem on this wiki to fix.
"""
import collections
import importlib.util
import sys
from pathlib import Path

import requests

WIKI = Path(__file__).resolve().parent.parent
OURS = "https://snap.amburgey.dev/w/api.php"
spec = importlib.util.spec_from_file_location("importer", WIKI / "tools" / "import-wikipedia.py")
importer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(importer)

TRACKING = [
    "Pages with script errors", "Pages with too many expensive parser function calls", "Pages with reference errors",
    "Pages with broken file links", "Pages with template loops", "Pages where template include size is exceeded",
    "Pages where expansion depth is exceeded", "Pages where node count is exceeded", "Pages with math errors",
    "Pages with math render errors", "Pages with broken reference names", "Pages with missing references list",
    "Pages with timeline errors", "Pages with syntax highlighting errors", "Pages with Kartographer errors",
    "Pages with incorrect ref formatting", "Pages using duplicate arguments in template calls",
]


def ours(**params):
    return requests.get(OURS, params={"format": "json", "formatversion": 2, **params}, timeout=120).json()


def members(category):
    out, cont = [], {}
    while True:
        r = ours(action="query", list="categorymembers", cmtitle="Category:" + category, cmlimit="max", **cont)
        out += [m["title"] for m in r["query"]["categorymembers"]]
        if "continue" not in r:
            return out
        cont = r["continue"]


def wikipedia_has(title, category):
    r = importer.api(action="query", titles=title, prop="categories", clcategories="Category:" + category)
    page = r["query"]["pages"][0]
    return bool(page.get("categories")), bool(page.get("missing"))


def main():
    totals = collections.Counter()
    only_here = []
    for category in TRACKING:
        pages = members(category)
        if not pages:
            continue
        for title in pages:
            same, missing = wikipedia_has(title, category)
            status = "also on Wikipedia" if same else ("not a Wikipedia page" if missing else "only here")
            totals[(category, status)] += 1
            if status != "also on Wikipedia":
                only_here.append((category, title, status))
    for (category, status), n in sorted(totals.items()):
        print(f"{n:5}  {status:22} {category}")
    print(f"\n{len(only_here)} pages to look at:")
    for category, title, status in only_here:
        print(f"   [{category}] {title} ({status})")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
