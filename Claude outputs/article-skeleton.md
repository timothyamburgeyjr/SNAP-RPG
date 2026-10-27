# Article skeleton: the Wikipedia order

The rule is [SNAP:Manual of Style/Layout § Order of article elements](https://snap.amburgey.dev/wiki/SNAP:Manual_of_Style/Layout#Order_of_article_elements)
(Wikipedia's text). Read that section with `get-page` `section: 1` if anything below is unclear. The
lead: [SNAP:Manual of Style/Lead section](https://snap.amburgey.dev/wiki/SNAP:Manual_of_Style/Lead_section).
Citations: [SNAP:Citing sources](https://snap.amburgey.dev/wiki/SNAP:Citing_sources).

Use only the parts the content needs. A minimal article is a lead and references.

```
{{Short description|...}}             <- wording rules: Template:Short description/doc on this wiki
{{About|...}}                         <- hatnotes, only if a confusable page exists
                                       (maintenance/cleanup tags, then date/variety tags like {{Use dmy dates}}, go here)
{{Infobox xxx                          <- see templates.md
| field = value
}}
{{Sidebar ...}}                        <- only if a sidebar exists for the topic
'''Title''' is ...                     <- lead: bold title in the first sentence; sums up the body;
                                          no heading
== First body section ==
{{Main|Sub-article}}                   <- section hatnotes go right under the heading
...
== Works ==                            <- biographies only
== See also ==                         <- internal links not already in the body
== Notes ==                            <- only if {{efn}} is used
{{Notelist}}
== References ==
{{Reflist}}
== Further reading ==
== External links ==                   <- always the last section
{{Navbox name}}                        <- navboxes
{{DEFAULTSORT:Surname, Given}}         <- only when the sort isn't the title as written
[[Category:...]]                       <- see categories.md
```

Wikipedia habits to keep:
- Headings: `==` level for main sections, `===` under them. Rules for wording them are in
  SNAP:Manual of Style § Section headings. Read it there rather than going from memory.
- Section names are Wikipedia's own: "See also", "Notes", "References", "Further reading",
  "External links". Don't rename them.
- Citation markers go after full stops and commas with no space before them (SNAP:Citing sources),
  `<ref>...</ref>` with `{{Cite book}}`/`{{Cite web}}`; reuse with
  `<ref name="x" />`. Every `<ref>` needs a `{{Reflist}}`, or the preview shows an error.
- Leave fields empty rather than guessing. This wiki has no Wikidata, so fields Wikipedia fills from it
  stay empty unless the caller gives a value.
- Don't hand-build boxes, banners or styled `<div>`s. If the caller wants a notice, use the real Wikipedia
  message-box template for it (`templates.md`).
- Draft articles go in the `Draft:` namespace, the way Wikipedia does it, if the caller asks for a draft.
  Whether something is a draft is the caller's decision.

Check after saving (`create-edit.md` step 4): compare the section order with a real Wikipedia article of
the same type. Report any part that's missing or out of place.
