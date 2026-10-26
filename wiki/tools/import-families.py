"""Import Wikipedia's general-purpose template families, as Wikipedia itself groups them.

Usage (wiki running): python wiki/tools/import-families.py

The families are Wikipedia's own: the templates in the Wikipedia categories listed below (direct
members), plus a few real navboxes/sidebars kept as examples. Each one
comes with its dependencies and documentation through import-wikipedia.py, which skips anything
already imported. The full list used is written to wiki/template-families.tsv.
"""
import csv
import importlib.util
import sys
from pathlib import Path

WIKI = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("importer", WIKI / "tools" / "import-wikipedia.py")
importer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(importer)

# Infoboxes are NOT imported wholesale: Wikipedia's index (Wikipedia:List of infoboxes, 1,389) is mostly
# real-world-specific (sports seasons, places in one country...). The gallery set plus on-demand imports
# cover SNAP (Tim, 2026-10-25). Index pages whose linked templates should all come in go here.
INDEX_PAGES = []
# Real navboxes and sidebars, imported as reference examples for the design kit.
EXAMPLES = ["Template:Solar System", "Template:Quantum mechanics"]
CATEGORIES = [
    "Navigational box metatemplates", "Sidebar metatemplates", "Hatnote templates", "Citation Style 1 templates",
    "Footnote templates", "Mbox and messagebox templates", "Cleanup templates", "Inline cleanup templates",
    "Quotation templates", "Collapse templates", "List formatting and function templates", "Table cell templates",
    "Talk header templates", "Template namespace templates", "Documentation shared content templates",
    "Internal link templates", "Image formatting and function templates", "Graphics templates",
]


def from_index(page):
    links = importer.api(action="parse", page=page, prop="links")["parse"]["links"]
    return {l["title"] for l in links if l["ns"] == 10 and l.get("exists")}


def from_category(category):
    titles, cont = set(), {}
    while True:
        r = importer.api(action="query", list="categorymembers", cmtitle="Category:" + category,
                         cmnamespace=10, cmlimit="max", **cont)
        titles.update(m["title"] for m in r["query"]["categorymembers"])
        if "continue" not in r:
            return titles
        cont = r["continue"]


def main():
    families = {}
    for page in INDEX_PAGES:
        families[page] = from_index(page)
    for category in CATEGORIES:
        families["Category:" + category] = from_category(category)
    families["Examples"] = set(EXAMPLES)
    wanted = sorted({t for ts in families.values() for t in ts if not importer.SKIP.search(t) and not t.endswith("/doc")})
    with open(WIKI / "template-families.tsv", "w", encoding="utf-8", newline="\n") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["family", "template"])
        for family, titles in families.items():
            for t in sorted(titles):
                w.writerow([family, t])
    print(f"{len(wanted)} templates across {len(families)} families")
    importer.main(wanted)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
