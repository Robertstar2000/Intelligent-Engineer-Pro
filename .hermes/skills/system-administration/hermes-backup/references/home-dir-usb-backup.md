# Home Directory Backup to USB Drive

## When to Use
Use this pattern when the user wants to back up their entire home directory (or all home directories) to an external/mounted USB drive, separate from the Hermes-internal backup (which only covers `~/.hermes`).

## Pattern

### 1. Identify the USB mount point
```bash
lsblk -o NAME,FSTYPE,SIZE,MOUNTPOINT
# Look for the USB drive (e.g. /mnt/usb_4tb)
```

### 2. Create the backup directory ON the USB drive
```bash
mkdir -p /mnt/usb_4tb/backups/home-backup
```
**Never create the backup directory on the system drive** — defeats the purpose of an off-system backup.

### 3. Verify the USB is mounted before running
```bash
mountpoint /mnt/usb_4tb 2>/dev/null || echo "NOT MOUNTED — abort"
```

### 4. rsync command
```bash
rsync -avh --delete \
  --exclude '.cache' \
  --exclude '.local/share/Trash' \
  --exclude 'node_modules' \
  --exclude '__pycache__' \
  --exclude '*.pyc' \
  --exclude '.npm' \
  --exclude '.yarn' \
  --exclude 'Downloads' \
  "$HOME/" /mnt/usb_4tb/backups/home-backup/
```
Trailing slash on `$HOME/` is required — without it, rsync creates a nested `bob/` inside the backup dir.

### 5. Cron setup
Schedule via `cronjob(action='create')` with:
- `schedule: '0 2 * * 0'` — every Sunday at 2:00 AM
- Set `model` + `provider` explicitly so cron doesn't fall through the resolution chain
- Use `no_agent=True` with `script` for fire-and-forget log-only jobs, or `no_agent=False` if delivery reporting is needed
- The script should write a timestamped log to `~/.hermes/cron/output/backup-TIMESTAMP.log`

### 6. Save the script for reproducibility
Save a copy to `~/.hermes/scripts/home-backup.sh` so the job can be recreated if the cron entry is lost.

## Pitfalls
- **USB not mounted at boot time**: If the USB drive isn't auto-mounted when the cron fires, the backup silently creates files on the system drive under `/mnt/usb_4tb/` (a stale mount point). Add a mountpoint check at the top of the script.
- **`rsync --delete` with trailing slash**: The source must have a trailing `/` or rsync behavior changes and `--delete` can remove unintended files.
- **Cron model resolution**: Cron jobs need model/provider set explicitly. Without it, they fall through to config.yaml default, which may be empty.
- **Large backups take time**: A first-time home directory rsync can take 5–15 minutes. Set adequate timeout. Subsequent runs with `--delete` are incremental and fast.
