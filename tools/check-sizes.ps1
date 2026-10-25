# Lists files in the repo over 50 MiB (GitHub warns at 50, blocks at 100). Read-only.
$root = Split-Path $PSScriptRoot -Parent
$big = Get-ChildItem $root -Recurse -File -Force |
    Where-Object { $_.FullName -notmatch '\\\.git\\' -and $_.Length -gt 50MB }
if (-not $big) { 'Nothing over 50 MiB.' }
$big | ForEach-Object { '{0,8:N1} MiB  {1}' -f ($_.Length / 1MB), $_.FullName.Substring($root.Length + 1) }
