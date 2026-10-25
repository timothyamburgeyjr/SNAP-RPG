# SNAP RPG

SNAP is a free tabletop RPG. This repo holds everything that runs or documents it, one part per folder.

| Folder | What it is |
|---|---|
| `wiki/` | The SNAP wiki (MediaWiki in Docker), served at https://snap.amburgey.dev |
| `files/` | Master copies of maps, schematics, art, PDFs and source documents |
| `shared/` | Things several parts use, such as the master branding files |
| `survey-db/` | Reserved for the survey database. Not designed yet. |

## Rules for this repo
- No secrets in git. Passwords and tokens go in a `.env` file next to the part that uses them (gitignored). Each part has a `.env.example` listing the names.
- Database volumes and the wiki's upload folder are not in git. See `wiki/README.md` for the backup step.
- Files over 50 MiB: run `tools/check-sizes.ps1` before committing. GitHub warns at 50 MiB and blocks at 100 MiB; use Git LFS or a GitHub Release for those.
