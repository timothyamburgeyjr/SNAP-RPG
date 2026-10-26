"""Build the design kit page: a full inventory of the Wikipedia templates on this wiki.

Usage (wiki running): python wiki/tools/build-design-kit.py
Writes wiki/pages/SNAP/Design_kit.wiki; upload it with tools/push-pages.py.

Sources, none of them written by hand:
  wiki/infobox-sets.json            the chosen infoboxes, by group
  wiki/template-families.tsv        Wikipedia's template families (its own categories)
  wiki/infobox-gallery-sources.tsv  which infoboxes have a live example in SNAP:Infobox gallery
  wiki/wikipedia-imports.tsv        what has actually been imported
Descriptions are each template's own TemplateData description, or else the first sentence of its
documentation page (both Wikipedia's text), shown as plain text.
Infoboxes without a gallery example link a real Wikipedia article that uses them.
"""
import csv
import importlib.util
import json
import re
import sys
from pathlib import Path

import requests

WIKI = Path(__file__).resolve().parent.parent
OURS = "https://snap.amburgey.dev/w/api.php"
spec = importlib.util.spec_from_file_location("importer", WIKI / "tools" / "import-wikipedia.py")
importer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(importer)

FAMILY_NAMES = {
    "Category:Navigational box metatemplates": "Navboxes (navigation boxes at the foot of articles)",
    "Category:Sidebar metatemplates": "Sidebars (topic panels beside the text)",
    "Category:Hatnote templates": "Hatnotes",
    "Category:Citation Style 1 templates": "Citations (Citation Style 1)",
    "Category:Footnote templates": "Footnotes",
    "Category:Mbox and messagebox templates": "Message boxes",
    "Category:Cleanup templates": "Cleanup notices",
    "Category:Inline cleanup templates": "Inline cleanup tags",
    "Category:Quotation templates": "Quotations",
    "Category:Collapse templates": "Collapsing content",
    "Category:List formatting and function templates": "Lists",
    "Category:Table cell templates": "Table cells",
    "Category:Talk header templates": "Talk page headers",
    "Category:Template namespace templates": "Template links and documentation tools",
    "Category:Documentation shared content templates": "Shared documentation",
    "Category:Internal link templates": "Link helpers",
    "Category:Image formatting and function templates": "Image layout",
    "Category:Graphics templates": "Graphics",
}


def descriptions(titles):
    """TemplateData descriptions from this wiki (the imported documentation), by title."""
    out = {}
    for i in range(0, len(titles), 50):
        r = requests.get(OURS, params={"action": "templatedata", "titles": "|".join(titles[i:i + 50]), "lang": "en",
                                       "redirects": 1, "format": "json", "formatversion": 2}).json()
        for page in r.get("pages", {}).values():
            d = page.get("description")
            if isinstance(d, dict):
                d = d.get("en")
            if d:
                out[page["title"]] = re.sub(r"\s+", " ", d).strip()
    return out


def first_sentences(titles):
    """First sentence of each template's documentation page (Wikipedia's text, same as the imported copy),
    for templates whose TemplateData has no description."""
    out = {}
    docs = {t + "/doc": t for t in titles}
    names = list(docs)
    for i in range(0, len(names), 20):
        r = importer.api(action="query", titles="|".join(names[i:i + 20]), prop="extracts", exintro=1,
                         explaintext=1, exsentences=1, exlimit=20)
        for page in r["query"]["pages"]:
            text = re.sub(r"\s+", " ", page.get("extract", "")).strip()
            if text and page["title"] in docs:
                out[docs[page["title"]]] = text
    return out


def example_article(template):
    r = importer.api(action="query", list="embeddedin", eititle=template, einamespace=0, eilimit=1)
    used = r["query"]["embeddedin"]
    return used[0]["title"] if used else None


def cell(text):
    """Descriptions are plain text: shown as written, never interpreted as wiki markup."""
    return f"<nowiki>{text}</nowiki>" if text else ""


def name_of(title):
    return title.split(":", 1)[1]


def main():
    imported = {row["title"] for row in csv.DictReader(open(WIKI / "wikipedia-imports.tsv", encoding="utf-8"), delimiter="\t")}
    sets = json.load(open(WIKI / "infobox-sets.json", encoding="utf-8"))
    gallery = {row["template"]: row["article"] for row in
               csv.DictReader(open(WIKI / "infobox-gallery-sources.tsv", encoding="utf-8"), delimiter="\t")}
    families = {}
    for row in csv.DictReader(open(WIKI / "template-families.tsv", encoding="utf-8"), delimiter="\t"):
        families.setdefault(row["family"], []).append(row["template"])

    all_infoboxes = sorted({t for ts in sets.values() for t in ts})
    family_templates = sorted({t for f, ts in families.items() if f in FAMILY_NAMES for t in ts})
    desc = descriptions(all_infoboxes + family_templates)
    desc.update(first_sentences([t for t in all_infoboxes + family_templates if t not in desc]))

    out = ["{{Short description|Inventory of the Wikipedia templates available on this wiki}}",
           "The '''design kit''' lists every Wikipedia template family available on this wiki: what it is for, where its "
           "documentation is, and a live example. The templates are Wikipedia's own, copied unchanged with their "
           "documentation (CC BY-SA 4.0; each template's history credits its Wikipedia authors). Descriptions below are "
           "the templates' own documentation text.",
           "",
           "* '''See every infobox filled in:''' [[SNAP:Infobox gallery]] (each box is the exact source of a real Wikipedia article).",
           "* '''Documentation:''' open any template link below; its page shows Wikipedia's full documentation, and the "
           "visual editor's Insert → Template form uses the same data.",
           "* '''Need a template that isn't here?''' Ask; any Wikipedia template can be copied in with its documentation.",
           ""]

    count_ok = sum(t in imported for t in all_infoboxes)
    out += ["== Infoboxes ==",
            f"{count_ok} infobox types, grouped by subject. An infobox summarises the key facts of a subject in a box at "
            "the top right of its article.", ""]
    for group, titles in sets.items():
        out += [f"=== {group} ===",
                '{| class="wikitable sortable" style="width:100%"',
                "! Template !! What it is for !! Live example"]
        for t in sorted(titles):
            if t not in imported:
                continue
            if t in gallery:
                example = f"[[SNAP:Infobox gallery#{name_of(t)}|In the gallery]] (from [[wikipedia:{gallery[t]}|{gallery[t]}]])"
            else:
                art = example_article(t)
                example = f"[[wikipedia:{art}|{art}]] (Wikipedia)" if art else ""
            out += ["|-", f"| {{{{tl|{name_of(t)}}}}} || {cell(desc.get(t, ''))} || {example}"]
        out += ["|}", ""]

    out += ["== Navigation ==",
            "Navboxes are the collapsible link panels at the foot of related articles; sidebars are the topic panels "
            "beside the text. Each one on Wikipedia is a page built with these builders. Examples copied from Wikipedia:",
            "* Navbox: [[Template:Solar System]] (shown at the end of this page)",
            "* Sidebar: [[Template:Quantum mechanics]]",
            ""]

    out += ["== Template families ==",
            "Wikipedia's general-purpose template families, as Wikipedia itself groups them (its own categories).", ""]
    for family, label in FAMILY_NAMES.items():
        titles = [t for t in sorted(families.get(family, [])) if t in imported]
        if not titles:
            continue
        out += [f"=== {label} ===",
                f"Wikipedia category: [[wikipedia:{family}|{family}]]. {len(titles)} templates.",
                '{| class="wikitable sortable mw-collapsible' + (" mw-collapsed" if len(titles) > 25 else "") + '" style="width:100%"',
                "! Template !! What it is for"]
        for t in titles:
            out += ["|-", f"| {{{{tl|{name_of(t)}}}}} || {cell(desc.get(t, ''))}"]
        out += ["|}", ""]

    # Every other infobox in Wikipedia's own index, so it's clear what exists and can be copied on request
    index = importer.api(action="parse", page="Wikipedia:List of infoboxes", prop="links")["parse"]["links"]
    others = sorted({l["title"] for l in index if l["ns"] == 10 and l.get("exists") and l["title"].startswith("Template:Infobox ")
                     and "/" not in l["title"]} - set(all_infoboxes) - imported)
    out += ["== Not included ==",
            f"The other {len(others)} infoboxes in Wikipedia's index ([[wikipedia:Wikipedia:List of infoboxes|Wikipedia:List of "
            "infoboxes]]). Most are tied to real-world topics (particular sports, countries or franchises). Any of them can be "
            "copied in with its documentation on request; the links go to Wikipedia.",
            '{| class="wikitable sortable mw-collapsible mw-collapsed" style="width:100%"',
            "! Infobox on Wikipedia"]
    for t in others:
        out += ["|-", f"| [[wikipedia:{t}|{name_of(t)}]]"]
    out += ["|}", ""]

    out += ["== Wikipedia features on this wiki ==",
            "The extensions Wikipedia's templates need are installed; see [[Special:Version]] for the full list.",
            "* Timelines (<code>&lt;timeline&gt;</code>), formulas (<code>&lt;math&gt;</code>), audio and video players, "
            "pronunciation buttons, poems, image maps, hieroglyphs, section transclusion, category trees.",
            "* Maps (<code>&lt;mapframe&gt;</code>) draw OpenStreetMap tiles: Wikimedia's own map tiles may only be used on Wikimedia sites.",
            "* Sheet music (<code>&lt;score&gt;</code>) is switched off, as it currently is on Wikipedia.",
            "* There is no Wikidata here: template fields Wikipedia fills from Wikidata stay empty unless the page gives the value.",
            "",
            "== Example navbox ==",
            "{{Solar System}}"]
    page = "\n".join(out) + "\n"
    path = WIKI / "pages" / "SNAP" / "Design_kit.wiki"
    path.write_text(page, encoding="utf-8", newline="\n")
    print(f"wrote {path}: {count_ok} infoboxes, {len(family_templates)} family templates")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
