# files/: master copies

Every file that appears on the wiki is uploaded through the wiki (Special:Upload).
Its master copy also lives here, so it is versioned and the wiki's upload folder can be rebuilt.

| Folder | For |
|---|---|
| `maps/` | Maps, including large topo maps |
| `schematics/` | Ship and technology schematics (SVG) |
| `art/` | Illustrations, portraits, banners |
| `pdfs/` | Rulebooks and handouts |
| `sources/` | Source documents (drafts, charters, notes) |

## Naming
Give the master the same name as the wiki file: `File:Bybrook_topo.png` on the wiki is `maps/Bybrook_topo.png` here.

## Size
- Under 50 MiB: commit normally.
- 50–100 MiB: GitHub warns. Use Git LFS (see `.gitattributes`).
- Over 100 MiB: GitHub blocks it. Use Git LFS or attach it to a GitHub Release.
Run `tools/check-sizes.ps1` to see anything over 50 MiB.

## Rebuilding the wiki's uploads
MediaWiki's `importImages` maintenance script can bulk-load a folder of files. The exact command will be added to `wiki/README.md` once it has been tested.
