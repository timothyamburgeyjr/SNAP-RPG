# Hand-off to Claude Code

Use this when a job needs the repo (`D:\SNAP RPG`) rather than the connector. Say in one line why the
connector can't do it, then give Tim the prompt below in **one code block** so he can paste it into a
Claude Code session opened in `D:\SNAP RPG`. Then stop on that part and carry on with whatever the
connector *can* do.

## What goes to Claude Code

| Need | Why not the connector | What Claude Code does |
|---|---|---|
| A Wikipedia template/module that isn't on the wiki | Connector can't import | `python wiki/tools/import-wikipedia.py "Template:Name"` |
| Editing a repo-owned page (history says `Update from repo file wiki/pages/...`) | Next push would overwrite a wiki edit | Edit `wiki/pages/<NS>/<Title>.wiki`, then `python wiki/tools/push-pages.py <that file>` |
| A new page that should be repo-owned (Main Page parts, featured blurbs) | Same | Create the file under `wiki/pages/`, push it |
| Adding/removing someone from a user group (e.g. "writer") | No user-rights tool | Maintenance script in the container |
| LocalSettings.php, extensions, namespaces, skins | Server config | Edit the repo files, rebuild |
| Site CSS/JS (`MediaWiki:*.css`/`.js`), theme | Kept in the repo, out of the connector's job | Edit `wiki/theme/`, push |
| Uploading a file that isn't in the repo's `files\` folder yet | Connector only reads `files\` | Copy the master into `files\<subfolder>\` |

## The prompt (fill the brackets, keep the rest)

```
Working in D:\SNAP RPG (the SNAP wiki repo). Read wiki\README.md first.

Task: [one sentence: what needs doing]
Why it's here and not the connector: [one line]
Details: [titles, file paths, template names, exact wikitext if any]
Check when done: [how to confirm — e.g. "the template shows at https://snap.amburgey.dev/wiki/Template:Name
and renders on <page>", or "Special:ListUsers/writer lists <user>"]

Rules: never run git commands — I commit with GitKraken; at the end give me one commit block (files to
stage by path, what NOT to stage: .env, wiki\secrets\, wiki\backups\, and a commit message: imperative
subject under 72 characters, then 2-4 plain lines). Never print or commit secrets. Don't stop Docker for a
commit. Never `docker compose down -v`. Plain language, short status updates.
```

After Tim says it's done, verify from this side with the connector (read the page or `parse-wikitext`)
before continuing.
