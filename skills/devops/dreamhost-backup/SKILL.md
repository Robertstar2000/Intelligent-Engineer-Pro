---
name: dreamhost-backup
description: Backup mifeco.com from DreamHost to USB backup drive using rsync via pexpect
---

# DreamHost Backup to USB

Backs up the entire mifeco.com web root (PHP, images, CSS, JS, WordPress, books, consult, admin) from DreamHost to the USB 4TB drive.

## Files

- `scripts/backup_dreamhost.py` — the actual backup script

## Usage

```bash
cd /home/bob/.hermes/pipeline-engine
python3 scripts/backup_dreamhost.py
```

## What it backs up

All of `dh_mwpxuu@iad1-shared-b8-42.dreamhost.com:/home/dh_mwpxuu/mifeco.com/` → `/mnt/usb_4tb/Mifeco_Web_Backup/`

Includes:
- Admin dashboard (`.php`, `.html`)
- Consulting app (`.php`, Stripe vendor, config)
- Books site (SPA, images, books)
- WordPress (`wp-content/`, `wp-admin/`, `wp-includes/`)
- Custom images, assets, scripts
- All custom PHP files

## Verification

After backup completes, check:
```bash
du -sh /mnt/usb_4tb/Mifeco_Web_Backup/
find /mnt/usb_4tb/Mifeco_Web_Backup/ -type f | wc -l
```

Expected: ~332 MB, ~17,000 files

## Pitfalls

- Requires `pexpect` (available in Hermes venv, not system Python)
- Password read from `~/.hermes/.env` (`DREAMHOST_PASSWORD` variable)
- rsync uses compression (`-z --compress-level=6`) to reduce transfer size
- Full backup takes ~2 minutes for 326 MB site
- **rsync is additive** — it won't delete files on DreamHost that are no longer local. Run `scripts/cleanup_dreamhost.py` after major file removals to clean up orphaned files.
- **Always sync dashboard + JSON + SVGs together** — the HTML fetches JSON at runtime, so mismatched versions cause display errors.
- **DreamHost credentials**: host `IAD1-SHARED-B8-42.DREAMHOST.COM`, username `dh_mwpxuu`, password env var `DREAMHOST_PASSWORD` in `~/.hermes/.env`.
- **Use `cleanup_dreamhost.py`** to SSH in and delete old files after SVGs/pipelines change. The script deletes files listed in its `old_files` array — update that array when removing files locally.
