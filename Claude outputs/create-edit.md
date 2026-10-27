# Create or edit a page

What to write comes from the caller (`contract.md`). How a new article is laid out: `article-skeleton.md`.
Templates and their fields: `templates.md`. This leaf is the save-and-check routine every write uses.

## 1. Look before you write

- **New page:** `get-page` (`content: "none"`, `metadata: true`). It should come back `not_found`. If the
  page already exists, stop and report it. Don't overwrite.
- **Existing page:** `get-page` with `metadata: true` to get the source, the `latestRevisionId` and the
  sections. Then `get-page-history`:
  - an edit summary `Update from repo file wiki/pages/...` means the repo owns the page → hand it off
    (`handoff-claude-code.md`). Don't edit it here.
  - text written by someone other than you or Tim that you'd remove or rewrite → **Tim's OK first**.

## 2. Preview

`parse-wikitext` with the wikitext **and the real `title`** (so `{{PAGENAME}}` and namespace checks work).
Read the result before saving:
- `templates`: any `exists: false` means the template is missing → hand off the import. **Never build a
  stand-in.**
- `categories`: are these the ones you meant? A hidden maintenance category in the output (for example
  one about unknown parameters) is the wiki pointing at a mistake. Fix it.
- `links`: list the red ones (`exists: false`). They go back to the caller.
- `html`: look for `class="error"` or "Script error". Fix anything you find before saving.

## 3. Save

| Job | Call |
|---|---|
| New page | `create-page` (`title`, `source`, `comment`) |
| Change part of a page | `update-page` `operation: "find-replace"` (`find` = exact existing text, `replaceWith`). Best choice: nothing else can be lost |
| Rewrite one section | `update-page` `operation: "replace"`, `section: N`, `latestId`; the source includes the heading. Dropping subsections needs `removeSubsections: true` (Tim's OK if they hold text) |
| Add a new section at the end | `update-page` `operation: "append"`, source starts `"\n\n== Heading ==\n"` |
| Rewrite the whole page | `update-page` `operation: "replace"` with `latestId`. The source must contain everything that should stay |
| Very large new page | `create-page` with the first part, then `append` calls in order |

- Always pass `latestId` where you can, so a change someone made in between isn't overwritten.
- Always write an edit summary, plain and specific ("Add infobox and lead"), the way Wikipedia editors do.
- Don't set `bot`. Normal edits should show in recent changes.
- If an `append` result never came back, read the page before resending, or the text gets added twice.

## 4. Check, then report

1. `get-page` the saved source and confirm it matches what you meant to save.
2. `get-page` `content: "html"` (or `parse-wikitext` the saved source) and repeat the step 2 checks on
   the live page.
3. Compare with Wikipedia: open a real Wikipedia article of the same kind (raw source:
   `https://en.wikipedia.org/w/index.php?title=Article&action=raw`) and check the order of the parts,
   the template fields and how they're filled. That's only reading Wikipedia, as the model to copy.
   The edit itself always goes through the connector.
4. Report in a few lines: the page link, what was done, what differs from the Wikipedia model and why
   (for example "field empty: Wikipedia fills it from Wikidata, which this wiki doesn't have"), the red
   links made, and anything handed off.
