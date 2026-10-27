# Files and images

## Commons files: use by name, no upload

The wiki reads Wikimedia Commons directly. Write `[[File:Name.jpg|thumb|Caption]]` (or the infobox's
`image =` field) exactly as on Wikipedia.
- Check with a preview (`parse-wikitext`): the `<img>` comes from `upload.wikimedia.org`.
- `get-file` **can't see Commons files** (it answers `not_found`). That doesn't mean the file is missing.
  The preview is the check.

## SNAP's own files

The master copy lives in the repo's `files\` folder (`art`, `maps`, `pdfs`, `schematics`, `sources`).
The connector can read only that folder, which it sees as `/uploads`.

1. Ask Tim or the caller for the file's name in `files\`. If it isn't there yet, hand off copying it in
   (`handoff-claude-code.md`).
2. `get-file` for the title you want. It should be `not_found`, or the upload is refused.
3. Upload:
   - from the repo: `upload-file` with `filepath: "/uploads/<subfolder>/<name>"`, plus `title` and `text`
   - from a web address: `upload-file-from-url` (`url`, `title`, `text`). Only for files Tim has the
     right to put here.
4. `text` is the File: description page. Wikipedia's is `{{Information}}` plus a licence template.
   **Neither is on the wiki yet, and which licence SNAP's own files carry is Tim's decision.** Until both
   are settled, stop before the first upload and ask. Don't write a stand-in description box.
5. Check: `get-file` (size, type, link) and `get-file-data` (look at the image). Report the File: page link.

## A new version of a file

`update-file` (`filepath` in `/uploads/...`) or `update-file-from-url`. The old version stays in the file
history. Replacing a file someone else uploaded needs Tim's OK. To edit only the description page, use
`update-page` on the `File:` title.

## Moving or deleting files

`move-page` works on `File:` titles. Deleting follows `delete-protect.md` (Tim's OK every time), and check
`get-links-here` `type: "fileusage"` first, so you know which pages will show a broken image.
