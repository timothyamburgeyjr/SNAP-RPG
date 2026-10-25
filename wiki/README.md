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
