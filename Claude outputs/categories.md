# Categories

## Put a page in a category

`[[Category:Name]]` lines at the very end of the page (`article-skeleton.md`). Sort key:
`[[Category:Name|Key]]` for one category, or `{{DEFAULTSORT:Key}}` once for all of them (people:
`Surname, Given`). Use only when the title as written would sort wrongly.
After saving, check the categories in the preview or the saved page. List any red ones and create them (below).

## Create a category page

1. `get-page` the category. If it already exists, edit it instead.
2. Content, the Wikipedia way: a short plain sentence on what belongs in it; the main article, if
   there is one (Wikipedia uses `{{Cat main}}`, which isn't on the wiki yet → hand off its import); and
   the parent categories as `[[Category:Parent]]` lines. Every category except the top one has at least one parent.
3. `create-page`, then `get-category-members` on the parent to confirm it shows up as a `subcat`.

## Hidden and maintenance categories

Many arrive automatically from imported templates (for example "Pages with short description",
"Redirects from moves", "Disambiguation pages"). If their pages are red, create them with Wikipedia's
own templates for category pages: `{{Hidden category}}` and `{{Maintenance category}}` are on the wiki
(read their `/doc` first). `{{Tracking category}}` isn't yet (hand off its import if a doc calls for it).

The few category pages already on the wiki were hand-written with a bare `__HIDDENCAT__` and a SNAP
sentence (for example Category:Pages with short description). Bringing them in line is a separate
clean-up, and needs Tim's OK.

## Trees and browsing

- `get-category-members` lists pages, files and subcategories (`types`), 500 per call, with `continueFrom`.
- On a page: `<categorytree>Name</categorytree>` (the CategoryTree extension is installed).
  Preview it before saving.

## Finding uncategorised pages

`Special:UncategorizedPages` and `Special:WantedCategories` can't be read through the connector. Give
Tim the links: https://snap.amburgey.dev/wiki/Special:UncategorizedPages and
https://snap.amburgey.dev/wiki/Special:WantedCategories. For a known set of pages, a preview of each one
lists its categories.
