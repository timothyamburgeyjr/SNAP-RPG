# Move, redirect, disambiguate

The preview (`parse-wikitext`) shows whether every template below is on the wiki. If one is missing, hand
off the import (`handoff-claude-code.md`). Don't write something that only looks like it. (Imported
2026-10-26: the redirect category shell, `{{R from move}}`, `{{R to section}}`, `{{R from alternative name}}`,
`{{Disambiguation}}` and `{{Other uses}}`.)

## Move (rename)

1. Read the page and its history (repo-owned → hand off). Check the new title is free.
2. `get-links-here` (`title`: old, `filter: "redirects"`) lists the redirects that point at the old title.
   After the move they become double redirects.
3. `move-page` (`fromTitle`, `toTitle`, `comment`). Keep the defaults: `leaveRedirect: true` and
   `moveTalk: true`. Use `moveSubpages: true` only if the subpages belong with it.
4. The redirect the move leaves behind is a bare `#REDIRECT` line. Add the category shell with
   `{{R from move}}` (see Redirect below) with `update-page` `replace` and `latestId`.
5. Point each redirect from step 2 straight at the new title (`update-page` `find-replace` on the
   `#REDIRECT` line). Wikipedia expects the person who moved the page to clean these up.
6. Check: `get-page` of the old title has `#REDIRECT [[New]]`, and the new title reads as before. Report
   both links. Links in articles that now go through the redirect still work. Leave them unless Tim
   asks, because changing them would be a mass edit.

## Redirect

Source, as on Wikipedia:
```
#REDIRECT [[Target]]

{{Redirect category shell|
{{R from alternative name}}
}}
```
- Point to a section with `[[Target#Section]]` (and `{{R to section}}`).
- The shell files each redirect into categories such as "Redirects from moves". If those category
  pages don't exist yet, create them (`categories.md`).
- Check: `get-page` with `get-pages` `followRedirects: true` lands on the target.

## Disambiguation page

Only when two or more pages could use the same title. This wiki has no copy of Wikipedia's
disambiguation style guide, so copy a real Wikipedia disambiguation page (for example
https://en.wikipedia.org/wiki/Mercury, which opens "Mercury most commonly refers to:"):
```
'''Title''' may refer to:          <- take the exact opening wording from the Wikipedia page you copy

* [[Title (thing)]], one-line description
* [[Other title]], one-line description

== See also ==
* ...

{{Disambiguation}}
```
- One link per line, no references, no pictures. Don't add `{{Short description}}`: `{{Disambiguation}}`
  sets "Topics referred to by the same term" itself (seen in a preview on 2026-10-26).
- If one topic is the main one, it keeps the plain title, the list goes at `Title (disambiguation)`, and
  the main article gets a hatnote: `{{About|the thing|other uses|Title (disambiguation)}}`.
- `{{Disambiguation}}` is required: it categorises the page and marks it as a disambiguation page.
