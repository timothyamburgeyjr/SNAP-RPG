# wiki/: the SNAP wiki

MediaWiki 1.43.11 (LTS) in Docker with MariaDB 11.4.13 and the Vector 2022 skin.
Public address: https://snap.amburgey.dev/wiki/Main_Page. On this machine: http://localhost:8180.

| Path | What |
|---|---|
| `compose.yaml`, `Dockerfile`, `apache-snap.conf`, `php-snap.ini` | How the containers are built and run |
| `LocalSettings.php` | Wiki settings (no secrets) |
| `extensions.md` | Every extension and the version it's pinned to |
| `branding/`, `theme/` | Logos, favicons, cream theme, paper skin |
| `mockups/` | The approved target look |
| `.env` | Secrets. Never in git. Copy `.env.example` to make one. |

## Public access (Cloudflare Tunnel)
The wiki listens on 127.0.0.1:8180 only. The public address comes from Tim's existing Cloudflare tunnel:
the route is the `snap.amburgey.dev` entry in `C:\Users\Timothy\.cloudflared\config.yml` (outside this repo;
backup from before the change: `config.yml.bak-presnap`), and DNS is a proxied CNAME made with
`cloudflared tunnel route dns`. cloudflared does not reload its config on its own: restarting the
"Cloudflared Vault Tunnel" scheduled task applies changes, and briefly interrupts every site on that tunnel.

## Claude connector (MCP)
The `mcp` service is the MediaWiki MCP Server (pinned in `compose.yaml`), settings in `mcp/config.json`.
claude.ai custom connector URL: `https://snap-mcp.amburgey.dev/mcp` (second route in the same tunnel, to 127.0.0.1:8181).
- Nothing works without signing in through the wiki (`"private": true`); edits are made as the account that signed in.
  The connector signs in as **SNAP Claude** (administrator; not bureaucrat or interface admin).
- The OAuth app is "SNAP MCP connector" (Special:OAuthListConsumers). Its ID and secret are in `.env`;
  the wiki's OAuth signing keys are in `secrets/` (both gitignored).
- To cut Claude off: remove the connector in claude.ai, or as Captain Trips disable the app at
  Special:OAuthManageConsumers, or take SNAP Claude out of the administrator group.
- Claude can upload files only from the repo's `files/` folder (mounted read-only) or from a web address.

## Start and stop (in this folder)
    docker compose up -d --build
    docker compose down

`docker compose down` keeps the data. Never add `-v`: that deletes the database and uploads.

## Backup
Run `.\backup.ps1` while the wiki is running. It writes a database dump and a copy of all uploads to `backups\` (not in git).
Copy that folder somewhere off this machine now and then.

## Restore (onto an empty wiki)
    docker compose cp backups\snapwiki-<stamp>.sql db:/tmp/r.sql
    docker compose exec db sh -c 'MYSQL_PWD="$MARIADB_ROOT_PASSWORD" mariadb -u root snapwiki < /tmp/r.sql'
    docker compose cp backups\images-<stamp>.tgz mediawiki:/tmp/i.tgz
    docker compose exec mediawiki tar -xzf /tmp/i.tgz -C /var/www/html/w
