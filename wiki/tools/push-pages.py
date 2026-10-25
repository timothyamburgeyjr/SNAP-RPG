"""Upload the page files in wiki/pages/ to the wiki.

wiki/pages/ holds the repo's copy of hand-built pages (the Main Page and its blurbs), so they
are versioned like the rest of the wiki setup. The folder decides the title:
  pages/Main/Main_Page.wiki          -> Main Page        ("Main" = no namespace)
  pages/SNAP/Featured/Rules/1.wiki   -> SNAP:Featured/Rules/1

Usage (wiki running): python wiki/tools/push-pages.py [page files ...]   (no files = all of them)
Saves through MediaWiki's own edit script inside the container, credited to the admin account,
so no password is needed or sent anywhere. Unchanged pages are left alone.
"""
import subprocess
import sys
from pathlib import Path

WIKI = Path(__file__).resolve().parent.parent
EDITOR = "Captain Trips"


def title_for(path):
    namespace, *rest = path.relative_to(WIKI / "pages").with_suffix("").parts
    name = "/".join(rest).replace("_", " ")
    return name if namespace == "Main" else f"{namespace}:{name}"


def main(files):
    for path in files:
        title = title_for(path)
        summary = f"Update from repo file wiki/pages/{path.relative_to(WIKI / 'pages').as_posix()}"
        run = subprocess.run(
            ["docker", "compose", "exec", "-T", "mediawiki", "php", "/var/www/html/w/maintenance/run.php",
             "edit", "--user", EDITOR, "--summary", summary, title],
            cwd=WIKI, input=path.read_text(encoding="utf-8"), capture_output=True, text=True, encoding="utf-8")
        out = (run.stdout + run.stderr).strip().splitlines()
        print(f"{title:32} {out[-1] if out else run.returncode}")


if __name__ == "__main__":
    picked = [Path(a).resolve() for a in sys.argv[1:]] or sorted((WIKI / "pages").rglob("*.wiki"))
    main(picked)
