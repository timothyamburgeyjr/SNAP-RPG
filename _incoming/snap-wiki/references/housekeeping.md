# Housekeeping

Reports are read-only, so just do them. Fixes follow the other leaves. Fixing many pages in one go is
a mass edit, so list them and get Tim's OK first.

## The maintenance lists

Some special pages can be embedded in a preview: `parse-wikitext` with `{{Special:Name|limit=N}}`, then read
the list out of the HTML. Others can't be. Give Tim the link
(`https://snap.amburgey.dev/wiki/Special:Name`). Tested 2026-10-26:

| List | Through the connector? |
|---|---|
| WantedPages (red links, most-linked first) | ✅ embed |
| NewPages, AllPages/`Prefix`, PrefixIndex/`Prefix`, ListUsers(/`group`) | ✅ embed |
| UncategorizedPages, LonelyPages (orphans), DeadendPages, BrokenRedirects, DoubleRedirects, WantedCategories, WantedTemplates | ❌ link only |

- For red links to one page or template: `get-links-here` on the missing title.
- Orphan check for one page: `get-links-here` (`type: "wikilinks"`, `filter: "nonredirects"`, namespace 0) comes back empty.
- These lists are cached and can be out of date. Say so if a result looks stale.

**Known noise in WantedPages, not worth chasing:** `Help:` pages and `/sandbox` modules linked from
imported Wikipedia documentation, `wp:` shortcuts, and `Template:PENDINGCHANGELEVEL` (on Wikipedia that's
a word from the FlaggedRevs extension, which this wiki doesn't run). Report SNAP-content red links separately.

## Recent changes review

`get-recent-changes`. Add `types: ["edit", "new", "log"]` to include moves, deletions, uploads and user
rights. Filter with `since`/`until`, `user` or `excludeUser`, `namespace`. Edits made through the
connector carry the tag `OAuth CID: 1`. Edits pushed from the repo say `Update from repo file ...`. Report
what changed and by whom, with diff links. Patrolling (marking edits as checked) isn't possible through the connector.

## Talk pages

- Read the thread first (`get-page` on `Talk:Title`, `section: N`).
- Reply: `update-page` `operation: "append"` with `section: N` and `latestId`. Indent one level deeper
  than the post you're answering, matching the colons the thread already uses. End with ` ~~~~` (it
  expands to your user name and the time when saved).
- New topic: `update-page` `operation: "append"`, source starting `"\n\n== Topic ==\n"`, signed. If the talk
  page doesn't exist yet, `create-page`.
- Never edit or remove someone else's comment.
- Registered readers can post only on talk pages (server setting), so this is where public feedback lands.
