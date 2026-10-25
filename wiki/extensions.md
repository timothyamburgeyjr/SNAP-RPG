# Wiki extensions

Every extension is pinned to an exact version or commit in the Dockerfile. Bundled ones ship with MediaWiki 1.43.11.

| Extension | Source | Pinned at | Added for |
|---|---|---|---|
| Vector (skin) | bundled | 1.43.11 | Vector 2022 skin |
| ConfirmEdit + QuestyCaptcha | bundled | 1.43.11 | Sign-up question; question on talk edits that add links (item 4) |
| OAuth 1.1.0 | ExtensionDistributor bundle `OAuth-REL1_43-ce3cc80.tar.gz` | sha256 `a404374a…94e5` (full value in Dockerfile) | Sign-in for the MCP connector (item 12) |
| RandomSelection 2.3.0 | Gerrit, REL1_43 branch | commit `d559bf2f49f1b39fd407a56ceeabbb3845ea0364` | Main Page "a new pick each visit" boxes, via `<choose uncached>` (item 10) |
