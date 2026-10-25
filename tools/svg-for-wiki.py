"""Make an SVG uploadable to the wiki by removing its C2PA content-credentials block.

MediaWiki refuses SVGs that declare the c2pa namespace. The master file is left untouched
(it keeps its provenance); a cleaned copy is written next to it as NAME.wiki.svg (gitignored).

Usage: python tools/svg-for-wiki.py FILE.svg [FILE2.svg ...]
"""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

C2PA_METADATA = re.compile(r"<metadata>\s*<c2pa:manifest>.*?</c2pa:manifest>\s*</metadata>", re.S)
C2PA_ELEMENT = re.compile(r"<c2pa:(\w+)[^>]*>.*?</c2pa:\1>|<c2pa:\w+[^>]*/>", re.S)
C2PA_XMLNS = re.compile(r'\s+xmlns:c2pa="[^"]*"')

for name in sys.argv[1:]:
    src = Path(name)
    text = src.read_text(encoding="utf-8")
    clean = C2PA_XMLNS.sub("", C2PA_ELEMENT.sub("", C2PA_METADATA.sub("", text)))
    if "c2pa" in clean:
        sys.exit(f"{src}: c2pa content left after cleaning; not written")
    ET.fromstring(clean)  # stops with an error if the result is not valid XML
    out = src.with_name(src.stem + ".wiki.svg")
    out.write_text(clean, encoding="utf-8", newline="")
    print(f"{out}  ({len(text.encode())} -> {len(clean.encode())} bytes)")
