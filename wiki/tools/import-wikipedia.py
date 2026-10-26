"""Import templates and modules from English Wikipedia, with everything they depend on.

Usage (wiki running):  python wiki/tools/import-wikipedia.py "Template:Infobox" "Template:Navbox" ...
                       python wiki/tools/import-wikipedia.py --list   (show what has been imported)

For each requested page this asks Wikipedia which templates and Lua modules it uses (directly or
indirectly, including its documentation, which holds the visual editor's form data), exports the
current revision of all of them, and imports them with MediaWiki's importDump script. Authors show
as "wikipedia>Name" and keep their edit summaries. Every imported page and the Wikipedia revision
it came from is recorded in wiki/wikipedia-imports.tsv: that file is the attribution record
(Wikipedia text is CC BY-SA 4.0) and lets the same versions be re-imported later.

Pages already listed in the TSV are skipped, so local changes are never overwritten.
"""
import csv
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import requests

WIKI = Path(__file__).resolve().parent.parent
RECORD = WIKI / "wikipedia-imports.tsv"
API = "https://en.wikipedia.org/w/api.php"
KEEP_NS = {10, 828}                 # Template:, Module:
SKIP = re.compile(r"/(sandbox|testcases)(/|$)", re.I)
BATCH = 50

http = requests.Session()
http.headers["User-Agent"] = "SNAP-wiki-importer/1.0 (https://snap.amburgey.dev; tim.amburgey@emsar.com)"


def polite(method, url, **kw):
    """One request to Wikipedia, paced, retrying when it says to slow down (429) or is busy (5xx)."""
    for attempt in range(8):
        time.sleep(0.5)
        r = http.request(method, url, timeout=120, **kw)
        if r.status_code == 429 or r.status_code >= 500:
            time.sleep(int(r.headers.get("Retry-After", 0)) or 10 * (attempt + 1))
            continue
        r.raise_for_status()
        return r
    r.raise_for_status()
    return r


def api(**params):
    params.update(format="json", formatversion=2)
    return polite("GET", API, params=params).json()


def dependencies(title):
    """The page itself (after redirects) plus every Template:/Module: page it transcludes."""
    found, cont = set(), {}
    while True:
        r = api(action="query", titles=title, redirects=1, prop="templates",
                tlnamespace="10|828", tllimit="max", **cont)
        for redirect in r["query"].get("redirects", []):
            found.add(redirect["from"])
        for page in r["query"]["pages"]:
            if page.get("missing"):
                sys.exit(f"Not found on Wikipedia: {title}")
            found.add(page["title"])
            found.update(t["title"] for t in page.get("templates", []) if t["ns"] in KEEP_NS)
        if "continue" not in r:
            return {t for t in found if not SKIP.search(t)}
        cont = r["continue"]


def export(titles):
    return polite("POST", API, data={"action": "query", "titles": "|".join(titles), "export": 1,
                                     "exportnowrap": 1}).text


def recorded():
    if not RECORD.exists():
        return {}
    with open(RECORD, encoding="utf-8", newline="") as f:
        return {row["title"]: row for row in csv.DictReader(f, delimiter="\t")}


def save_record(rows):
    with open(RECORD, "w", encoding="utf-8", newline="\n") as f:
        w = csv.DictWriter(f, ["title", "wikipedia_revid", "wikipedia_timestamp"], delimiter="\t",
                           lineterminator="\n")
        w.writeheader()
        for title in sorted(rows):
            w.writerow(rows[title])


def docker(*args, **kw):
    return subprocess.run(["docker", "compose", *args], cwd=WIKI, capture_output=True, text=True,
                          encoding="utf-8", **kw)


def main(requested):
    done = recorded()
    wanted = set()
    for title in requested:
        deps = dependencies(title)
        print(f"{title}: {len(deps)} pages incl. dependencies")
        wanted |= deps
    todo = sorted(wanted - done.keys())
    print(f"{len(wanted)} pages needed, {len(wanted) - len(todo)} already imported, {len(todo)} to import")

    for i in range(0, len(todo), BATCH):
        chunk = todo[i:i + BATCH]
        xml = export(chunk)
        with tempfile.NamedTemporaryFile("w", suffix=".xml", delete=False, encoding="utf-8") as f:
            f.write(xml)
        cp = docker("cp", f.name, "mediawiki:/tmp/wp-import.xml")
        Path(f.name).unlink()
        if cp.returncode:
            sys.exit(cp.stderr)
        run = docker("exec", "-T", "mediawiki", "php", "/var/www/html/w/maintenance/run.php", "importDump",
                     "--username-prefix=wikipedia", "/tmp/wp-import.xml")
        if run.returncode:
            sys.exit(run.stdout + run.stderr)
        for page in re.finditer(r"<page>.*?<title>(.*?)</title>.*?<revision>\s*<id>(\d+)</id>.*?"
                                r"<timestamp>(.*?)</timestamp>", xml, re.S):
            title = page.group(1).replace("&amp;", "&").replace("&quot;", '"').replace("&#039;", "'")
            done[title] = {"title": title, "wikipedia_revid": page.group(2), "wikipedia_timestamp": page.group(3)}
        save_record(done)
        print(f"  imported {min(i + BATCH, len(todo))}/{len(todo)}")

    if todo:
        docker("exec", "-T", "mediawiki", "php", "/var/www/html/w/maintenance/run.php", "runJobs", "--quiet")
    print("done")


if __name__ == "__main__":
    if sys.argv[1:] == ["--list"]:
        for t in sorted(recorded()):
            print(t)
    elif sys.argv[1:]:
        main(sys.argv[1:])
    else:
        sys.exit(__doc__)
