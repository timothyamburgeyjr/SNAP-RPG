# The contract with content skills

Content skills (SNAP rules, Calador worldbuilding, others later) decide **what** goes on the wiki. They call
snap-wiki for **how**, and never use the connector directly, so the know-how stays in one place.

## What the caller hands over

| Item | Notes |
|---|---|
| **Job** | create · edit · move · redirect · disambiguate · categorise · upload · … |
| **Title** | The exact page title, including namespace (`Draft:`, `SNAP:`, …) |
| **Subject type** | What the thing is (a person, a ship, an organisation, a rule…). Used to choose the template |
| **Framing** | In-universe or real-world, when a template has both kinds |
| **Facts** | Field-ready values and prose. snap-wiki adds nothing |
| **Sources** | Citations for `<ref>`s, as the caller wants them cited |
| **Links** | Pages to link to; categories; parent categories |
| **Files** | Commons file names, or names in the repo's `files\` folder |

If something needed is missing, ask the caller (or Tim). Don't fill it in.

## What snap-wiki hands back

1. **Link** to the saved page (and revision number).
2. **Templates used**, and why that infobox, navbox or sidebar.
3. **Differences from Wikipedia**, each with its reason (for example "empty: Wikipedia fills it from Wikidata").
4. **Red links created**, and red categories created or still red.
5. **Not done**: anything refused, waiting for Tim's OK, or handed to Claude Code (with the prompt).

## Questions for the content skills to settle (not here)

- Whether new pages start in `Draft:` or go straight to main, and any "not canon / draft" notice.
- What counts as canon, and who signs off on it.
- Mixing Wikipedia text (CC BY-SA 4.0) into SNAP's own articles, and the licence of SNAP's own text and files.
- In-universe vs real-world framing for Calador articles.
