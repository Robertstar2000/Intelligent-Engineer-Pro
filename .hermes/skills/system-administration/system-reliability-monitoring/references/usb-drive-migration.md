# USB Drive Migration — Mount, Move Data, Symlink

## Pattern: Migrate large directories to a USB/data drive with symlinks

### 1. Add fstab entry for automount

```bash
# Get the UUID
sudo blkid /dev/sdX1

# Add to fstab (nofail = don't hang boot if drive unplugged)
echo 'UUID=XXXX-XXXX  /mnt/usb_4tb  ext4  defaults,nofail  0  2' | sudo tee -a /etc/fstab

# Create mount point and mount
sudo mkdir -p /mnt/usb_4tb
sudo mount -a
df -h /mnt/usb_4tb
```

### 2. Fix ownership so the agent can write

```bash
sudo chown $(whoami):$(whoami) /mnt/usb_4tb
```

### 3. Move data with rsync, then symlink

For each directory to migrate:

```bash
# Move data
rsync -a --info=progress2 /home/bob/old-dir/ /mnt/usb_4tb/new-dir/

# Verify sizes match
du -sh /home/bob/old-dir/ /mnt/usb_4tb/new-dir/

# Remove original and create symlink
rm -rf /home/bob/old-dir
ln -s /mnt/usb_4tb/new-dir /home/bob/old-dir
```

### 4. Verify symlinks work

```bash
ls -la /home/bob/old-dir        # should show symlink target
ls /home/bob/old-dir/ | head   # should list contents
```

### 5. Update any skills/cron that reference old paths

Skills that reference `~/backups/` or other moved paths need patching. Check:
- `hermes-backup` skill (BACKUP_DIR, tar -C, prune loop, verification)
- Cron job prompts that reference moved directories
- Memory entries with old paths

### Key pitfalls

- **USB drive root-owned**: After mounting, `chown` it to the user or rsync will fail with "Permission denied"
- **lost+found**: USB drives have a root-owned `lost+found` dir — `chmod 700` it or `du -sh` will error
- **Symlinks are transparent**: Skills and cron jobs that reference `~/books` will automatically follow the symlink — no changes needed for consumers
- **Backup skill**: Must update BACKUP_DIR, tar -C, prune loop, AND verification paths — all four references
- **Memory**: Update memory entries that store absolute paths to moved directories
