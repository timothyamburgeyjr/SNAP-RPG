# History, comparing, reverting

## Read the history

- `get-page-history` (`title`) gives 20 revisions per call, newest first. Go further back with
  `olderThan: <oldest revisionId shown>`. Each row: revision, time, user, summary, size.
- `get-revision` (`revisionId`, `metadata: true`) gives one old version's source (cut off at 75,000 bytes).
- `compare-pages` gives a diff. Each side is a revision number (`fromRevision`/`toRevision`), a title
  (latest version) or wikitext (`fromText`/`toText`). Identical text = no `diff` in the answer.
  The `changed` flag isn't reliable for that.
- Link for Tim: `https://snap.amburgey.dev/w/index.php?title=Page&diff=NEW&oldid=OLD`.

## Revert

The connector has no rollback or undo button. A revert means reading the good version and saving it again.

1. Find the version to go back to (`get-page-history`) and diff it against now:
   `compare-pages` `fromRevision: GOOD`, `toTitle: Page`. Show Tim the diff link.
2. **Tim's OK first** if the revert removes anyone else's edit or more than one edit.
3. `get-revision` `GOOD` for the source. If it was cut off (over 75,000 bytes), stop: the connector can't
   restore it whole. Give Tim the history link to undo it himself, or hand it off.
4. `get-page` `metadata: true` for the current `latestRevisionId`.
5. `update-page` `operation: "replace"`, `source` = the good revision's text, `latestId` = current,
   `comment: "Revert to revision GOOD by USER: reason"` (Wikipedia's wording).
6. Check: `compare-pages` `fromRevision: GOOD`, `toTitle: Page` (with the diff) must come back with **no
   `diff` and `sizeDelta: 0`**. Don't trust the `changed` flag: tested 2026-10-26, it says `true` for two
   revisions with identical text. Report the link.

**Undoing one edit in the middle** while keeping later ones: if the diff is small, reverse it with
`update-page` `find-replace`, then check the diff. If the edits are tangled, stop and give Tim the
history link.
