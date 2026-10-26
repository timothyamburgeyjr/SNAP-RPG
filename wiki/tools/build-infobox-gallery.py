"""Build the infobox gallery: every listed Wikipedia infobox, each with the exact infobox source of a
real Wikipedia article, plus everything that source needs, imported unchanged.

Usage (wiki running): python wiki/tools/build-infobox-gallery.py

For each template it looks at articles that use it (Wikipedia's own list), extracts that article's
infobox call verbatim, and picks one: images available on Wikimedia Commons first (they display here
through InstantCommons), then an explicit name/title, then the most filled-in fields. Footnotes the
box only names (<ref name="x" />) are copied from the same article revision into the page's
reference list. The gallery source is written to wiki/pages/SNAP/Infobox_gallery.wiki and the
choices (article + revision) to wiki/infobox-gallery-sources.tsv.
"""
import csv
import importlib.util
import json
import re
import tempfile
import sys
from pathlib import Path

WIKI = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("importer", WIKI / "tools" / "import-wikipedia.py")
importer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(importer)
api, http = importer.api, importer.http

TEMPLATES = """person|officeholder|scientist|military person|royalty|writer|artist|musical artist|organization|
government agency|legislature|political party|military unit|company|university|school|religious group|
settlement|country|planet|space station|body of water|river|mountain|islands|building|protected area|
song|album|book|film|artwork|musical composition|language|religion|holiday|game|video game|sport|
military conflict|event|election|treaty|weather event|legislation|court case|physical quantity|concept|
spaceflight|ship|weapon|aircraft|automobile|mineral|medical condition|unit|star system|planetary system|
galaxy|nebula|constellation|poem|short story|play|musical|opera|dance|anthem|music genre|literary genre|
art movement|comic|historical era"""
# Not included: "Infobox star system" (no Wikipedia article uses it; star systems use the Starbox family)
# and "Graphical timeline" (articles only use it through timeline templates such as Nature timeline).
TEMPLATES = ["Template:Infobox " + t.strip() for t in TEMPLATES.split("|") if t.strip() != "star system"]
TEMPLATES += ["Template:Starbox begin", "Template:Speciesbox", "Template:Nature timeline", "Template:Horizontal timeline"]
FAMILY_END = {"Template:Starbox begin": "Starbox end"}     # multi-part boxes: copy begin ... end
CANDIDATES = 12
NAME_PARAMS = ("name", "title", "conventional_long_name", "common_name", "Name")


def aliases(template):
    """The template's name and every redirect to it, as they may be written in article source."""
    names = {template.split(":", 1)[1]}
    r = api(action="query", titles=template, prop="redirects", rdnamespace=10, rdlimit="max")
    for page in r["query"]["pages"]:
        names.update(x["title"].split(":", 1)[1] for x in page.get("redirects", []))
    return names


def call_at(text, start):
    """The full {{...}} call starting at text[start] (balanced braces)."""
    depth, i = 0, start
    while i < len(text):
        if text.startswith("{{", i):
            depth += 1
            i += 2
        elif text.startswith("}}", i):
            depth -= 1
            i += 2
            if depth == 0:
                return text[start:i]
        else:
            i += 1
    return None


def extract(text, names, end_name=None):
    # MediaWiki ignores the case of a template name's first letter, so match both
    alternatives = (f"[{n[0].upper()}{n[0].lower()}]" + re.escape(n[1:]) for n in sorted(names, key=len, reverse=True))
    pattern = r"\{\{\s*(?:[Tt]emplate:)?(" + "|".join(alternatives) + r")\s*(?=[|}\n])"
    flat = text.replace("_", " ")
    m = None
    for found in re.finditer(pattern, flat):
        # only a box standing on its own counts, not one nested inside another template
        before = flat[:found.start()]
        if before.count("{{") == before.count("}}"):
            m = found
            break
    if not m:
        return None
    if end_name:
        end = re.search(r"\{\{\s*" + re.escape(end_name) + r"\s*\}\}", text[m.start():])
        return text[m.start():m.start() + end.end()] if end else None
    return call_at(text, m.start())


def filled(call):
    return len(re.findall(r"\|\s*[\w ]+\s*=\s*[^|\s}]", call))


def has_name(call):
    return any(re.search(r"\|\s*" + p + r"\s*=\s*[^|\s}]", call) for p in NAME_PARAMS)


def parse(text, title, prop):
    """Wikipedia's parser on a piece of source (POST: long boxes don't fit in a URL)."""
    return importer.polite("POST", importer.API, data={"action": "parse", "text": text, "title": title, "prop": prop,
                           "contentmodel": "wikitext", "format": "json", "formatversion": 2}).json()["parse"]


def article(title):
    r = api(action="query", titles=title, prop="revisions", rvprop="ids|content", rvslots="main")
    rev = r["query"]["pages"][0]["revisions"][0]
    return rev["revid"], rev["slots"]["main"]["content"]


def images_on_commons(call, title):
    files = parse(call, title, "images")["images"]
    if not files:
        return True, []
    c = importer.polite("GET", "https://commons.wikimedia.org/w/api.php", params={"action": "query", "format": "json",
                        "formatversion": 2, "titles": "|".join("File:" + f for f in files[:50])}).json()["query"]["pages"]
    missing = [p["title"] for p in c if p.get("missing")]
    return not missing, missing


def dependencies(call, title):
    # Lua modules are listed among the templates (namespace 828); the parser's "modules" are browser scripts
    return {t["title"] for t in parse(call, title, "templates")["templates"] if t["ns"] in (10, 828)}


ATTR = r"""\b{0}\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'/>]+))"""


def attr(tag, key):
    m = re.search(ATTR.format(key), tag)
    return next((g for g in m.groups() if g is not None), None).strip() if m else None


EFN_GROUPS = {"efn": "lower-alpha", "efn-la": "lower-alpha", "efn-ua": "upper-alpha", "efn-lr": "lower-roman",
              "efn-ur": "upper-roman", "efn-lg": "lower-greek"}
NOTE_TEMPLATE = r"\{\{\s*(efn(?:-[a-z]+)?|refn)\s*\|"


def params(call):
    """Top-level parameters of a {{template|...}} call: (positional list, named dict)."""
    body = call[2:-2]
    parts, depth, cur, i = [], 0, "", 0
    while i < len(body):
        two = body[i:i + 2]
        if two in ("{{", "[["):
            depth += 1
            cur += two
            i += 2
            continue
        if two in ("}}", "]]"):
            depth -= 1
            cur += two
            i += 2
            continue
        if body[i] == "|" and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += body[i]
        i += 1
    parts.append(cur)
    positional, named = [], {}
    for part in parts[1:]:
        key, eq, value = part.partition("=")
        if eq and re.fullmatch(r"\s*[\w -]+\s*", key):
            named[key.strip()] = value.strip()
        else:
            positional.append(part.strip())
    return positional, named


def note_calls(source):
    """{{efn}}/{{refn}} calls: (group, footnote name, has content, full call)."""
    for m in re.finditer(NOTE_TEMPLATE, source, re.I):
        full = call_at(source, m.start())
        if not full:
            continue
        kind = m.group(1).lower()
        pos, named = params(full)
        group = EFN_GROUPS.get(kind, named.get("group", "").strip("\"'"))
        yield group, named.get("name", "").strip("\"'"), any(pos) or bool(named.get("1")), full


def ref_tags(source):
    """<ref> tags: (group, footnote name, has content, full tag or definition)."""
    for m in re.finditer(r"<ref\b[^>]*?/>|<ref\b[^>]*?>.*?</ref>", source, re.S | re.I):
        open_tag = m.group(0).split(">", 1)[0] + ">"
        yield attr(open_tag, "group") or "", attr(open_tag, "name"), not open_tag.endswith("/>"), m.group(0)


def footnote_defs(call, text):
    """Footnotes the box points to but defines elsewhere in the article: (group, definition) pairs,
    copied verbatim from the same article revision. Covers <ref name=x />, {{r|x}}, and named
    {{efn}}/{{refn}} notes; footnotes the box defines itself are left alone."""
    wanted, defined_here = set(), set()
    for _, name, content, _ in ref_tags(call):
        if name:
            (defined_here if content else wanted).add(name)
    for _, name, content, _ in note_calls(call):
        if name:
            (defined_here if content else wanted).add(name)
    for m in re.finditer(r"\{\{\s*[Rr]\s*\|", call):
        pos, _ = params(call_at(call, m.start()) or "{{r}}")
        wanted.update(p for p in pos if p)
    defs = []
    for name in sorted(wanted - defined_here):
        found = next(((g, d) for g, n, c, d in ref_tags(text) if n == name and c), None)
        if not found:
            found = next(((g, d) for g, n, c, d in note_calls(text) if n == name and c), None)
        if found:
            defs.append(found)
        else:
            print(f"   footnote '{name}' not found in the article")
    return defs


def choose(template):
    names = aliases(template)
    users = api(action="query", list="embeddedin", eititle=template, einamespace=0, eilimit=CANDIDATES * 3)["query"]["embeddedin"]
    best = None
    for i, u in enumerate(users):
        if i >= CANDIDATES and best:
            break
        revid, text = article(u["title"])
        call = extract(text, names, FAMILY_END.get(template))
        if not call:
            continue
        ok_images, missing = images_on_commons(call, u["title"])
        score = (ok_images, has_name(call), filled(call))
        if best is None or score > best[0]:
            best = (score, u["title"], revid, call, text, missing)
        if ok_images and has_name(call) and filled(call) >= 8:
            break
    return best


PICKS = Path(tempfile.gettempdir()) / "snap-infobox-gallery-picks.json"


def main():
    picks = json.loads(PICKS.read_text(encoding="utf-8")) if PICKS.exists() else {}
    sections, all_defs, rows, deps = [], [], [], set()
    for template in TEMPLATES:
        if template not in picks:
            best = choose(template)
            picks[template] = best and [list(best[0]), *best[1:]]
            PICKS.write_text(json.dumps(picks), encoding="utf-8")
        best = picks[template]
        if not best:
            print(f"{template}: no article found with a copyable call")
            continue
        (ok_images, named, n), title, revid, call, text, missing = best
        deps |= dependencies(call, title) | {template}
        all_defs += footnote_defs(call, text)
        rows.append({"template": template, "article": title, "revid": revid, "images_on_commons": ok_images,
                     "missing_images": ";".join(missing)})
        print(f"{template:42} {title}  (rev {revid}, {n} fields{'' if ok_images else ', images not on Commons: ' + str(len(missing))})")
        heading = template.split(":", 1)[1]
        sections.append(f"== {heading} ==\nFrom [[wikipedia:{title}|{title}]] on English Wikipedia, "
                        f"[https://en.wikipedia.org/w/index.php?oldid={revid} revision {revid}].\n\n{call}\n{{{{clear}}}}\n")

    if "--page-only" not in sys.argv:
        print(f"importing dependencies of {len(rows)} boxes ({len(deps)} pages)...")
        importer.main(sorted(deps | {"Template:Reflist", "Template:Notelist", "Template:Clear"}))

    text = "\n".join(sections)
    defs = []
    for group_and_def in all_defs:
        if group_and_def not in defs:
            defs.append(group_and_def)
    # The footnote groups the boxes and copied definitions use, and the list Wikipedia uses for each
    everything = text + "\n".join(d for _, d in defs)
    groups = {g for g, _, _, _ in ref_tags(everything)} | {g for g, _, _, _ in note_calls(everything)}
    if re.search(r"\{\{\s*NoteTag", everything, re.I):
        groups.add("note")                            # {{NoteTag}} notes are listed by {{NoteFoot}}
    lists = {"": "Reflist", "lower-alpha": "Notelist", "upper-alpha": "Notelist-ua", "lower-roman": "Notelist-lr",
             "upper-roman": "Notelist-ur", "lower-greek": "Notelist-lg", "note": "NoteFoot"}

    def ref_list(group):
        return f"{{{{{lists[group]}}}}}\n" if group in lists else f"{{{{Reflist|group={group}}}}}\n"

    # Definitions copied from the articles sit hidden in the page body: a note may itself contain a
    # footnote, which isn't allowed inside a list. Their text shows in the lists below, as on Wikipedia.
    hidden = ('<div style="display:none">\n' + "\n".join(d for _, d in defs) + "\n</div>\n") if defs else ""
    page = ("This test page shows every infobox type copied from English Wikipedia. Each box is the exact infobox "
            "source of the linked Wikipedia article and revision (CC BY-SA 4.0), unchanged.\n\n" + text + hidden +
            "\n== Notes ==\n" + "".join(ref_list(g) for g in sorted(groups) if g) +
            "\n== References ==\n" + ref_list(""))
    out = WIKI / "pages" / "SNAP" / "Infobox_gallery.wiki"
    out.write_text(page, encoding="utf-8", newline="\n")
    with open(WIKI / "infobox-gallery-sources.tsv", "w", encoding="utf-8", newline="\n") as f:
        w = csv.DictWriter(f, ["template", "article", "revid", "images_on_commons", "missing_images"], delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {out} ({len(rows)} boxes)")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")    # article names contain characters the Windows console can't show
    main()
