# Delete, undelete, protect

## Delete: Tim's OK every time, for every page

1. Read the page, `get-page-history` (who wrote what) and `get-links-here` (wikilinks and transclusions:
   what breaks).
2. Ask Tim in one line: the page link, why, what links to it, whose edits go with it. Wait for a yes
   that names this page. A yes for one page doesn't cover the next one, and "clean up" isn't a yes to
   delete.
3. `delete-page` (`title`, `comment`). Give a plain reason, the way Wikipedia's deletion log does
   ("Test page, no longer needed").
4. Check: `get-page` returns `not_found`. Report what was deleted and any links that are now red.

It's a soft delete: `undelete-page` (`title`, `comment`) brings back the page and its whole history.
Only Tim (in the repo, as server admin) can purge a page for good. The connector can't, and shouldn't.

Talk pages: deleting a page doesn't delete its talk page. Ask about that separately.

## Protect

`protect-page` (`title`, `protections`, `expiry`, `comment`):
- `protections`: `{"edit": LEVEL, "move": LEVEL}`, plus `upload` for File pages; just `create` for a title
  that doesn't exist. LEVEL is one the wiki accepts: MediaWiki's are `autoconfirmed` and `sysop`, and
  `"all"` removes protection. If the wiki refuses a level, the error says so. Report it; don't guess another.
- `expiry`: `infinite` or a period such as `"1 week"`.
- `cascade` also protects everything the page embeds. Use it only when Tim asks (on Wikipedia it's for
  the Main Page and similar).
- Protecting a page Tim didn't ask about needs his OK first, because it changes who can edit.
- A visible notice: `{{pp}}` is on the wiki (a redirect to `Template:Protected page`). Use it as its
  `/doc` page says, only if Tim wants a notice.
- Check: the tool's reply lists the protection now in force. Report the level and expiry.

Note: anyone not in the admin or "writer" groups can already only post on talk pages (server setting).
Protection is for pages even writers shouldn't touch.
