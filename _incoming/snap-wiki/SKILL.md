---
name: snap-wiki
description: How to RUN the SNAP wiki (https://snap.amburgey.dev) through the "SNAP wiki" connector — create, edit, preview, move, redirect, revert, delete, protect, categorise, upload, template and housekeep pages the Wikipedia way. A mechanics toolbox, not a content source; content skills (SNAP rules, Calador worldbuilding) call it to put their material on the wiki. Use whenever anything is read from or written to the SNAP wiki — "put this on the wiki", "make a wiki page for", "add an infobox", "fix the category", "rename that page", "what links here", "red links", "upload this map", "revert that edit", "snap wiki", "snap.amburgey.dev" — even if the wiki isn't named but a SNAP or Calador page is being made or changed.
---

# snap-wiki

> **Stick to the record.** Represent what's actually on the wiki, in the connector's answers and on
> Wikipedia — cite what you read. If it isn't there, say so. Never invent what a page, template or
> field contains.

**Sharpening for this skill:** "it looks right" is not done. Done = saved, read back, and compared with
the matching real Wikipedia page, with every difference named plainly.

This skill decides **how**, never **what**. It holds no SNAP rules and no Calador lore. Content comes from
the calling skill or from Tim; if content is missing, ask for it — don't fill it in.

## Before anything: the connector

Every action goes through the **SNAP wiki** connector's tools (`mcp__SNAP_wiki__*`). Nothing else —
no browser editing, no curl, no "paste this wikitext yourself".
1. Call `whoami`. If the tools aren't there or it fails on sign-in, stop and say:
   *"Turn on 'SNAP wiki' in claude.ai Settings > Connectors and sign in, then ask again."*
2. Note the username it reports; edits are credited to it. Tim's choice (2026-10-26): the connector
   signs in as **Captain Trips**, his own account, so the work is credited to him. If it reports
   anything else, mention it once in your status line.

## Tim's four rules (break none)

1. **Copy Wikipedia exactly.** Real templates, real documented fields, filled the way real Wikipedia
   articles fill them. No look-alikes, no invented fields, no "improvements". Unsure → find a real
   Wikipedia article that does it and copy that.
2. **Check before saying done** — read the saved page back, compare with Wikipedia, say what differs.
3. **Destructive actions need Tim's OK first** — delete, mass edits, overwriting text someone else wrote.
4. **Plain language, links not screenshots, short status lines.**

## Two things that apply to every write

- **Repo-owned pages.** Some pages are mastered in the repo (`wiki/pages/`) and pushed by
  `wiki/tools/push-pages.py`; a wiki-side edit to them is overwritten on the next push. Before writing an
  existing page, check `get-page-history`: if any edit summary reads `Update from repo file wiki/pages/...`,
  don't edit it on the wiki — hand it off (next point).
- **Claude Code hand-offs.** Anything the connector can't do goes to a Claude Code session in the repo.
  Don't half-do it or work around it: read `references/handoff-claude-code.md` and give Tim the
  ready-to-paste prompt. Everything else, just do.

## Routing — read only the leaf for the job

| Job | Leaf |
|---|---|
| Read a page, search, find titles | `references/read-search.md` |
| Create or edit a page (whole or one section); preview first | `references/create-edit.md` |
| History, compare revisions, revert | `references/history-revert.md` |
| Move/rename, redirects, disambiguation pages | `references/move-redirect.md` |
| Delete, undelete, protect | `references/delete-protect.md` |
| Lay out a new article the Wikipedia way | `references/article-skeleton.md` |
| Infoboxes, navboxes, sidebars, SNAP-own templates | `references/templates.md` |
| Category pages, trees, sort keys, hidden categories | `references/categories.md` |
| Commons files, uploads, File: description pages | `references/files.md` |
| Red links, orphans, broken/double redirects, recent changes, talk replies | `references/housekeeping.md` |
| Interface messages, Main Page boxes, featured blurbs, user groups, server settings | `references/wiki-settings.md` |
| What a content skill hands over and gets back | `references/contract.md` |
| Anything that needs the repo | `references/handoff-claude-code.md` |

## Reference pages on the wiki (point to them; don't restate them)

- Layout and lead: [SNAP:Manual of Style](https://snap.amburgey.dev/wiki/SNAP:Manual_of_Style) and its
  /Layout, /Lead section, /Infoboxes subpages; [SNAP:Citing sources](https://snap.amburgey.dev/wiki/SNAP:Citing_sources).
  These are Wikipedia's text unchanged. Where they're silent, use Wikipedia's live Manual of Style.
- Which template: [SNAP:Design kit](https://snap.amburgey.dev/wiki/SNAP:Design_kit). Real filled examples:
  [SNAP:Infobox gallery](https://snap.amburgey.dev/wiki/SNAP:Infobox_gallery).

## Capability manifest

> **Capability manifest:** an entry for this skill is *pending* — the manifest note
> (`07 - System/capability-manifest.md`) does not exist yet (Phase 6.5). Do not fabricate one.
