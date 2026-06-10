# DreamHost 403 Forbidden — Troubleshooting

## Symptom
A static file (`.html`, `.js`, `.css`, `.svg`, `.jpg`) returns **403 Forbidden** even though it exists on the server. PHP files work fine.

## Root Cause — File Permissions
DreamHost web server runs under a different user than the SSH user. Files uploaded via SCP/rsync with restrictive permissions (`600` = owner read/write only) are **not readable** by the web server.

**Files with `-rw-------` (600) cause 403.**
**Files need `-rw-r--r--` (644) for the web server to read them.**

## Diagnosis
```bash
ls -la /home/dh_mwpxuu/mifeco.com/admin/kanban-dashboard.html
# -rw------- = 600 = 403
```

## Fix
```bash
chmod 644 /home/dh_mwpxuu/mifeco.com/admin/kanban-dashboard.html
```

Apply to all static files:
```bash
find /home/dh_mwpxuu/mifeco.com/admin/ -type f \( -name "*.html" -o -name "*.js" -o -name "*.css" -o -name "*.svg" \) -exec chmod 644 {} \;
```

## Prevention
Add `--chmod=Fu=rw,Fog=r` to rsync commands:
```bash
rsync -avz --chmod=Fu=rw,Fog=r --delete ...
```

## Corrupted Files
A `.js.corrupted` file indicates an interrupted SCP upload. Delete it and re-upload.

## Quick Test
```bash
curl -s -o /dev/null -w "%{http_code}" https://mifeco.com/admin/kanban-dashboard.html
# 403 = permissions, 200 = working
```