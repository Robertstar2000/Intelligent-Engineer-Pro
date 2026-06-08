# USB Data Migration Pattern

## When to Use
When relocating large directories (books, backups, project dirs) to external storage while keeping the original paths working via symlinks. Also covers migrating backup destinations (cron jobs, scripts) to write directly to external storage.

## Pattern

```bash
# 1. Ensure mount point exists and is writable
sudo mkdir -p /mnt/usb_4tb
sudo chown $(whoami):$(whoami) /mnt/usb_4tb

# 2. Ensure fstab entry for boot persistence
# Add to /etc/fstab:
# UUID=<uuid>  /mnt/usb_4tb  ext4  defaults,nofail  0  2
# The 'nofail' option prevents boot hang if drive is unplugged.

# 3. Mount
sudo mount -a
df -h /mnt/usb_4tb  # verify

# 4. Create target directory structure
mkdir -p /mnt/usb_4tb/{backups,archives,books,project-dirs}

# 5. rsync each directory, then replace with symlink
for dir in ~/big_dir1 ~/big_dir2; do
  name=$(basename "$dir")
  rsync -aHAX "$dir/" "/mnt/usb_4tb/project-dirs/$name/" \
    && rm -rf "$dir" \
    && ln -s "/mnt/usb_4tb/project-dirs/$name" "$dir" \
    && echo "MOVED: $name"
done

# 6. Verify symlinks work
ls -la ~/big_dir1   # should show ->
ls ~/big_dir1/      # should list contents

# 7. Update any skills/cron jobs that reference old absolute paths
grep -rl "/home/bob/old_path/" ~/.hermes/skills/ | head -5
```

## Key Points
- Always `rsync -aHAX` (preserves permissions, symlinks, timestamps, ACLs, xattrs) before `rm -rf`
- Use `ln -s <target> <link_name>` — the symlink path comes SECOND
- Symlinks are transparent to most tools and scripts
- Update backup skills, cron jobs, and config files to reference new paths
- The `nofail` fstab option is critical for removable drives — prevents boot hang
- **Verify file sizes match** after rsync before removing the original: `du -sb /original` vs `du -sb /new`

## Migrating Backup Destinations

When moving backup output to external storage:

1. **Update cron job prompts** to set `HERMES_BACKUP_DIR=/mnt/usb_4tb/backups` (for hermes-backup skill)
2. **Update backup scripts** to write logs to the USB drive too (not just data)
3. **Add mount verification** at the start of backup scripts: `mountpoint -q /mnt/usb_4tb || exit 1`
4. **Update the hermes-backup skill procedure** to auto-detect USB via `mountpoint` and prefer it as default

## Session Example (2026-05-25)
Moved ~20 GB of backups + archives + books + project dirs from ~/ to /mnt/usb_4tb (4TB ext4 USB drive). All original paths maintained via symlinks. Updated hermes-backup skill to write to /mnt/usb_4tb/backups/.

## Session Example (2026-06-04)
Freed 74GB on 128GB SSD (99% → 32%) by moving: backups (73GB), google-cloud-sdk (847MB), Desktop (85MB), hermes-backup files (79MB), cindy-lou-series (28MB), books-section (14MB), .codex (71MB), .config/browseruse (66MB), series-infographics (2.2MB), cindy-lou-scripts. All replaced with verified symlinks. Updated both backup cron jobs (nightly-backup + weekly home backup) to write directly to /mnt/usb_4tb/backups/ with logs also on USB. Updated hermes-backup skill to auto-detect USB drive as default destination.
