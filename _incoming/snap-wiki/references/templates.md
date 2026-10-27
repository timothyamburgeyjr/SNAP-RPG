# Templates: infoboxes, navboxes, sidebars, SNAP-own boxes

Every template here is Wikipedia's own, imported unchanged with its documentation. Use them exactly as
Wikipedia does. If you're unsure, find the real Wikipedia article and copy what it does.

## 1. Pick the template

[SNAP:Design kit](https://snap.amburgey.dev/wiki/SNAP:Design_kit) lists them, with Wikipedia's own one-line
purpose for each. The page is about 280 KB, so **read only the section you need** (`get-page` `section: N`):

| Need | Section |
|---|---|
| Infoboxes: people and beings 2 · life and medicine 3 · science 4 · space 5 · technology and vehicles 6 · places 7 · organisations and politics 8 · culture and arts 9 · events and history 10 | 2–10 |
| Navboxes 13 · sidebars 14 · hatnotes 15 · citations 16 · footnotes 17 · message boxes 18 · cleanup 19–20 · quotations 21 · and so on | 12–30 |
| Wikipedia infoboxes **not** on the wiki (can be imported) | 31 |

Or `search-page` with `namespaces: [4, 10]` for the template name. Section numbers can change when the
page is rebuilt. Check them against the outline from `get-page` `metadata: true`.

Match the subject type the caller gives to Wikipedia's description, and say which template you chose and
why. Whether an article uses an in-universe template (`Infobox fictional location`, `Infobox character`, …)
or a real-world one (`Infobox settlement`, `Infobox person`, …) is the **caller's** decision. Ask if they
haven't said.

## 2. Fill it with its real fields

1. Read `Template:Name/doc` with `get-page` (large docs: read by section). Its blank copy-and-paste block
   lists the fields. Use only fields that appear there.
2. See how a real article fills it: the box's section in
   [SNAP:Infobox gallery](https://snap.amburgey.dev/wiki/SNAP:Infobox_gallery) is the exact source of a real
   Wikipedia article (76 boxes). For boxes not in the gallery, the Design kit row names a live example
   article. Read it with WebFetch (`https://en.wikipedia.org/wiki/Article`). That gives the rendered page,
   so it shows which fields appear and how they read.
3. Fill only from the caller's facts. Leave the rest empty. Fields Wikipedia fills from Wikidata stay empty here.
4. Preview (`create-edit.md` step 2). A `Preview warning ... unknown parameter "x"` means a field name is
   wrong. Fix it before saving: the warning doesn't show on the saved page.

## 3. A new navbox or sidebar

- Build it only with `{{Navbox}}` or `{{Sidebar}}`, following `Template:Navbox/doc` / `Template:Sidebar/doc`
  (read them first; they cover `name`, `title`, `groupN`/`listN`, and the `v·t·e` links that need
  `name` to match the template's own page name). Example on the wiki: SNAP:Design kit § Example navbox.
- Save it at `Template:Name` (`create-edit.md`), preview it on its own, then add it to the articles it
  lists (navboxes go at the foot, `article-skeleton.md`). Adding it to many pages is a mass edit: Tim's OK.

## 4. A SNAP-own template (only when nothing on Wikipedia fits)

- First check section 31 (not yet imported). If a Wikipedia template fits, import it (hand-off). Don't build one.
- A new template is a design decision: **Tim's OK first**, naming the template and its fields.
- Build it on `{{Infobox}}` (or `{{Navbox}}`/`{{Sidebar}}`) following `Template:Infobox/doc`. Take the field
  names and order from the closest Wikipedia infobox, so it reads like one. No hand-made tables, colours or CSS.
- Give it a `/doc` page shown through `{{Documentation}}`, with a blank copy-and-paste block, like every
  imported template.

## Missing templates

If a template isn't on the wiki (the preview shows `exists: false`, or there's a Lua "does not exist" error),
hand off `import-wikipedia.py` for that exact title (`handoff-claude-code.md`). **Never imitate a missing
template**, not even as a stopgap.
