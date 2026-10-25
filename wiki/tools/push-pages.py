"""Upload the page files in wiki/pages/ to the wiki, as the admin account.

wiki/pages/ holds the repo's copy of hand-built pages (the Main Page and its blurbs), so they
are versioned like the rest of the wiki setup. The folder decides the title:
  pages/Main/Main_Page.wiki          -> Main Page        ("Main" = no namespace)
  pages/SNAP/Featured/Rules/1.wiki   -> SNAP:Featured/Rules/1

Usage: python wiki/tools/push-pages.py [page files ...]     (no files = all of them)
Reads the admin password from wiki/.env and never prints it. Unchanged pages are left alone.
"""
import sys
from pathlib import Path

import requests

WIKI = Path(__file__).resolve().parent.parent
SITE = "https://snap.amburgey.dev"
API = SITE + "/w/api.php"


def title_for(path):
    namespace, *rest = path.relative_to(WIKI / "pages").with_suffix("").parts
    name = "/".join(rest).replace("_", " ")
    return name if namespace == "Main" else f"{namespace}:{name}"


def main(files):
    env = dict(line.strip().split("=", 1) for line in open(WIKI / ".env", encoding="utf-8")
               if "=" in line and not line.startswith("#"))
    s = requests.Session()

    def token(kind="csrf"):
        r = s.get(API, params={"action": "query", "meta": "tokens", "type": kind, "format": "json"}).json()
        return r["query"]["tokens"][f"{kind}token"]

    r = s.post(API, data={"action": "clientlogin", "username": "Captain Trips",
                          "password": env["MW_ADMIN_PASSWORD"], "logintoken": token("login"),
                          "loginreturnurl": SITE + "/", "format": "json"}).json()["clientlogin"]
    if r["status"] != "PASS":
        sys.exit(f"login failed: {r.get('message')}")

    for path in files:
        title = title_for(path)
        r = s.post(API, data={"action": "edit", "title": title, "text": path.read_text(encoding="utf-8"),
                              "summary": f"Update from repo file wiki/pages/{path.relative_to(WIKI / 'pages').as_posix()}",
                              "token": token(), "format": "json"}).json()
        edit = r.get("edit", {})
        status = "unchanged" if "nochange" in edit else edit.get("result") or r.get("error", {}).get("code")
        print(f"{title:32} {status}")


if __name__ == "__main__":
    picked = [Path(a).resolve() for a in sys.argv[1:]] or sorted((WIKI / "pages").rglob("*.wiki"))
    main(picked)
