# Read and search

Read-only, so no OK needed. Use this before every write, too: you can't edit well what you haven't read.

## Which tool

| Want | Call | Notes |
|---|---|---|
| One page's wikitext | `get-page` (`title`, `content: "source"`) | Over 75,000 bytes is cut off; the marker lists sections — read them one at a time with `section: N` |
| Revision number, size, section list | `get-page` (`content: "none"`, `metadata: true`) | `latestRevisionId` is what edits need as `latestId` |
| How it renders | `get-page` (`content: "html"`) | Use when checking a saved page |
| Up to 50 pages at once | `get-pages` (`titles: [...]`) | `content: "none"` only works with `metadata: true`. Missing pages are listed, not errors |
| Does a title exist? | `get-page` with `content: "none"`, `metadata: true` | `not_found` = free title |
| Full-text search | `search-page` (`query`, `namespaces`, `limit` ≤ 100) | **Searches only main articles unless you pass `namespaces`** |
| Titles starting with… | `search-page-by-prefix` (`prefix`, `namespace`, `limit` ≤ 500) | Prefix is the part after the colon; namespace is a number |
| What links here / what uses a template / a file | `get-links-here` (`type`: `wikilinks`, `transclusions`, `fileusage`) | Pages through `continueFrom` |
| What's in a category | `get-category-members` | See `categories.md` |

## Namespace numbers (from `get-site-info`)

0 main · 2 User · 4 SNAP · 6 File · 8 MediaWiki · 10 Template · 12 Help · 14 Category · 100 Portal ·
118 Draft · 828 Module. A namespace's talk pages are its number + 1 (1 Talk, 5 SNAP talk, …).
`Special:` pages can't be read with `get-page`; see `housekeeping.md`.

For a broad search, pass `namespaces: [0, 4, 10, 14, 100, 118]`.

## Reporting

Give the link (`https://snap.amburgey.dev/wiki/Title_with_underscores`), and quote only what's needed.
If a search finds nothing, say so. Don't guess what a page "probably" says.
