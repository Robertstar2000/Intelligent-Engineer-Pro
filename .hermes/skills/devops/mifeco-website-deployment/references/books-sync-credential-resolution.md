# Books Sync Script — Credential Resolution (2026-06-15)

## Script Location

`/home/bob/Desktop/hermesfiles/cindy-lou-scripts/sync-books-site.py`

Runs weekly as a cron job (Monday 9 AM). Scans for new/changed book files, deploys them to `books.mifeco.com` via SFTP.

## Credential Resolution Chain

The script's `get_dreamhost_password()` function tries two sources in order:

1. **Primary:** `~/.hermes/.env` — looks for `DREAMHOST_PASSWORD=...`
2. **Fallback:** `~/.hermes/secrets/mifeco-dreamhost.env` — looks for `DREAMHOST_PASS=...`

## The Placeholder Bug (Fixed 2026-06-15)

The `.env` file had `DREAMHOST_PASSWORD=***` — a placeholder, not the real password. The function returned `***` which failed auth silently. The real credentials lived only in the secrets file under a different key name (`DREAMHOST_PASS=`).

**Fix applied:** Added fallback logic — if the `.env` value is a placeholder (`***`) or missing, try the secrets file. This way the script doesn't break when `.env` has dummy values.

```python
# Pattern used in the fix:
def get_dreamhost_password():
    pw_file = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(pw_file):
        with open(pw_file) as f:
            for line in f:
                if "DREAMHOST_PASSWORD=" in line:
                    val = line.split("=", 1)[1].strip()
                    if val and val != "***":
                        return val
    # Fallback
    secrets_file = os.path.expanduser("~/.hermes/secrets/mifeco-dreamhost.env")
    if os.path.exists(secrets_file):
        with open(secrets_file) as f:
            for line in f:
                if "DREAMHOST_PASS=" in line:
                    return line.split("=", 1)[1].strip()
    return None
```

## Prerequisites

The script uses `paramiko` for password-based SFTP. Install if missing:

```bash
pip3 install paramiko
```

Without paramiko, the script falls back to a subprocess `sftp` call that tries to pipe the password via stdin — this **does not work** because `sftp` doesn't accept passwords from stdin. The subprocess fallback is broken by design; paramiko is required.

## What Gets Synced

Scanned directories:
- `/home/bob/Desktop/hermesfiles/cindy-lou-series/book-*/chapters/*.md`
- `/home/bob/Desktop/hermesfiles/cindy-lou-series/book-*/Marketing_and_Compliance/*`
- `/home/bob/Desktop/hermesfiles/cindy-lou-series/covers/*`
- `/home/bob/Desktop/hermesfiles/cindy-lou-series/kdp-packages/*.zip`
- `/home/bob/Desktop/hermesfiles/cindy-lou-series/reader-magnet/*.md`
- `/home/bob/Desktop/hermesfiles/cindy-lou-series/books-mifeco-website/**/*`
- `/mnt/usb_4tb/books/*/chapters/*.md`
- `/mnt/usb_4tb/books/*/Marketing_and_Compliance/*`
- `/mnt/usb_4tb/books/*/*.epub`
- `/mnt/usb_4tb/books/*/*.pdf`

## State Tracking

Sync state persists at `~/.hermes/cron/books-site-sync-state.json`. The script uses MD5 hashes to detect changed files, only deploying files whose hashes differ from the last run.