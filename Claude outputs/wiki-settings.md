# Wiki settings

Two tiers. Tier (a) is done through the connector. Tier (b) only Claude Code in the repo can do: say what's
needed and give the prompt (`handoff-claude-code.md`). Never pretend a tier (b) change was made.

## (a) Through the connector

**Interface messages** (`MediaWiki:` pages, namespace 8: labels, tab names, notices):
1. Find the message name: open the page with `?uselang=qqx` (for example
   https://snap.amburgey.dev/wiki/Main_Page?uselang=qqx). Every label shows its message name in brackets,
   such as `(nstab-talk / talk)`. Confirm it with a preview of `{{int:name}}`.
2. `create-page` / `update-page` on `MediaWiki:Name`. Not `.css` or `.js` pages, those are tier (b).
3. Check by previewing `{{int:Name}}` again.
4. These edits live only in the wiki's database. The repo lists them in `wiki/interface-messages.md` so
   they can be rebuilt. **Every time**, hand off a one-line row for that table (page, set to, why).

**Protection:** `delete-protect.md`.

**Main Page boxes and featured blurbs** (`Main Page`, `SNAP:Featured/...`, `Template:Other areas of SNAP`)
are repo-owned: tier (b).

## (b) Claude Code only

| Change | Where |
|---|---|
| Main Page, its boxes, featured blurbs (`SNAP:Featured/Calador/N`, `SNAP:Featured/Rules/N`) | `wiki/pages/...` + `push-pages.py` |
| Add or remove someone from **writer** (or any group) | Maintenance script. The connector has no user-rights tool |
| Who may edit what, namespaces, upload rules | `wiki/LocalSettings.php` |
| Extensions | `wiki/LocalSettings.php`, `wiki/extensions.md`, rebuild |
| Site CSS/JS, skin, colours | `wiki/theme/` |
| Importing templates or modules | `wiki/tools/import-wikipedia.py` |
| The connector itself (sign-in, upload folder) | `wiki/compose.yaml`, `wiki/mcp/config.json` |

To check who's in a group without the repo: preview `{{Special:ListUsers/writer}}` ("No user found" means
the group is empty; on 2026-10-26 it was, and sysop held Captain Trips and SNAP Claude).
