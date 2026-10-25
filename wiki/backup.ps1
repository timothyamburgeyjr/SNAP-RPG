# Backs up the wiki's database and uploads to wiki\backups\ (gitignored). The wiki must be running.
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$stamp = Get-Date -Format 'yyyy-MM-dd_HHmm'
New-Item -ItemType Directory -Force backups | Out-Null

docker compose exec -T db sh -c 'MYSQL_PWD="$MARIADB_ROOT_PASSWORD" mariadb-dump -u root --single-transaction --default-character-set=binary snapwiki > /tmp/snapwiki.sql'
docker compose cp db:/tmp/snapwiki.sql "backups\snapwiki-$stamp.sql"
docker compose exec -T db rm /tmp/snapwiki.sql

docker compose exec -T mediawiki tar -czf /tmp/images.tgz -C /var/www/html/w images
docker compose cp mediawiki:/tmp/images.tgz "backups\images-$stamp.tgz"
docker compose exec -T mediawiki rm /tmp/images.tgz

"Backup written: backups\snapwiki-$stamp.sql and backups\images-$stamp.tgz"
