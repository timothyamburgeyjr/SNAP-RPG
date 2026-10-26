# Wiki extensions

Every extension is pinned to an exact version or commit in the Dockerfile. Bundled ones ship with MediaWiki 1.43.11.

| Extension | Source | Pinned at | Added for |
|---|---|---|---|
| Vector (skin) | bundled | 1.43.11 | Vector 2022 skin |
| ConfirmEdit + QuestyCaptcha | bundled | 1.43.11 | Sign-up question; question on talk edits that add links (item 4) |
| OAuth 1.1.0 | ExtensionDistributor bundle `OAuth-REL1_43-ce3cc80.tar.gz` | sha256 `a404374a…94e5` (full value in Dockerfile) | Sign-in for the MCP connector (item 12) |
| VisualEditor | bundled | 1.43.11 | "Edit" tab with the visual editor (item 13) |
| ParserFunctions, Scribunto (LuaSandbox), TemplateData, Cite, WikiEditor, CodeEditor | bundled | 1.43.11 | Wikipedia's article toolkit: infoboxes, sidebars, navboxes, citations (item 13) |
| TemplateStyles 1.0 | ExtensionDistributor bundle `TemplateStyles-REL1_43-e74200b.tar.gz` | sha256 `8df19ca4…d6f7` (full value in Dockerfile) | Stylesheets inside Wikipedia's templates (item 13) |
| ShortDescription 4.0.2 | GitHub StarCitizenTools/mediawiki-extensions-ShortDescription (no release tags) | commit `8d348a84a2e337b777525daeea2ff01707785171`, sha256 `4370ea69…bb6d` | `{{SHORTDESC:}}` for Wikipedia's short descriptions (item 13) |
| GeoData | ExtensionDistributor bundle `GeoData-REL1_43-fe2da93.tar.gz` | sha256 `d906a47c…c5f1` (full value in Dockerfile) | `{{#coordinates:}}` for Wikipedia's coordinate templates (item 13) |
| WikibaseStub | ours, `local-extensions/WikibaseStub` | in repo | `mw.wikibase`, `{{#property:}}`, `{{#statements:}}` for Wikipedia's templates; every lookup answers "no Wikidata item" (item 13) |
| Math | bundled | 1.43.11 | `<math>`, rendered as on Wikipedia (MathML + SVG from Wikimedia's math service) (item 13) |
| TimedMediaHandler 0.6.0 | ExtensionDistributor bundle `TimedMediaHandler-REL1_43-768731a.tar.gz` | sha256 `144cc434…0825` (full value in Dockerfile) | Audio/video player, as on Wikipedia; no transcoding here (item 13) |
| Phonos 0.1.0 | ExtensionDistributor bundle `Phonos-REL1_43-d1d5069.tar.gz` | sha256 `7cc8c4b9…3168` (full value in Dockerfile) | Pronunciation buttons that play recorded files (item 13) |
| RandomSelection 2.3.0 | Gerrit, REL1_43 branch | commit `d559bf2f49f1b39fd407a56ceeabbb3845ea0364` | Main Page "a new pick each visit" boxes, via `<choose uncached>` (item 10) |
