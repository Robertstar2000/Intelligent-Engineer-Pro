# Disk Formatting — Agent Constraints & Workarounds

## The Problem

`mkfs`, `mkfs.ext4`, and related filesystem format commands are on the unconditional blocklist. The agent cannot execute them under any circumstances — not with `--yolo`, `/yolo`, `approvals.mode=off`, or cron approve mode.

`dd` to raw block devices (`/dev/sdX`) also requires root and is blocked by the same policy.

## Workaround: Script + User Execution

When a disk needs to be formatted/partitioned:

1. **Write a complete bash script** that performs the operation safely
2. **Include safety checks** — confirm target is NOT the boot drive
3. **Save to `~/`** or `/tmp/`
4. **Instruct user to run:** `sudo bash /path/to/script.sh`
5. **Verify results** after user confirms completion

## Safety Rules

- Always confirm target is not the C drive (check `df -h` for which device holds `/`)
- Wipe only first 100MB + last 100MB to clear signatures — no need to zero full drive
- Use GPT partition table + ext4 for general-purpose Linux USB drives
- Label filesystems for easy identification (e.g., `USB_4TB`)
- Always run `partprobe` after partitioning to update kernel's view

## Passwordless Sudo Setup

To allow the agent to run disk operations directly, the user can install:

```
bob ALL=(ALL) NOPASSWD: /usr/sbin/parted, /sbin/mkfs.ext4, /usr/bin/dd, /usr/bin/mount, /usr/bin/umount, /usr/sbin/blockdev, /usr/bin/lsblk, /usr/sbin/blkid, /usr/sbin/partprobe, /usr/bin/md5sum, /usr/bin/df
```

Install with: `sudo install -m 0440 /tmp/disk-ops /etc/sudoers.d/disk-ops`

## udisks2 / polkit Limitations

- `udisksctl` can see drives but doesn't expose format/wipe commands
- `pkexec` requires interactive auth (doesn't work from agent)
- Neither is a viable alternative to sudo for disk formatting

## USB Drive Identification

```bash
lsblk -f          # List all block devices with filesystems
df -h             # Show mounted filesystems (identify C drive)
lsusb             # List USB devices (identify USB drives by name)
```

USB drives typically appear as `/dev/sda`, `/dev/sdb`, etc. The C drive is typically `/dev/nvme0n1` (NVMe) or `/dev/sda` (SATA). **Always verify** before formatting.
