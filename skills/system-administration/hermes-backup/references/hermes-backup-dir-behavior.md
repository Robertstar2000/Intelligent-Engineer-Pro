# HERMES_BACKUP_DIR Environment Variable Behavior

## Overview
The HERMES_BACKUP_DIR environment variable controls where Hermes backups are stored. Understanding its behavior is crucial for ensuring backups go to the intended location (especially external USB drives).

## Behavior Specification
1. **When HERMES_BACKUP_DIR is explicitly set (non-empty)**:
   - The value is used directly as the backup directory
   - No auto-detection of USB drives occurs
   - Example: `HERMES_BACKUP_DIR=/mnt/usb_4tb/backups hermes backup`

2. **When HERMES_BACKUP_DIR is unset or empty**:
   - Auto-detection runs: checks if `/mnt/usb_4tb` is a mountpoint
   - If USB is mounted: uses `/mnt/usb_4tb/backups`
   - If USB is not mounted: falls back to `$HOME/backups`

## Best Practices
- For cron jobs or automated backups targeting USB: explicitly set `HERMES_BACKUP_DIR` to avoid surprises if USB becomes unmounted
- For interactive use: rely on auto-detection unless you have a specific override need
- Always verify the USB is mounted before relying on auto-detection: `mountpoint -q /mnt/usb_4tb`

## Session Lesson
During the June 6, 2026 backup session, it was observed that:
- Setting `HERMES_BACKUP_DIR=/mnt/usb_4tb/backups` before running the backup procedure ensures the backup goes directly to the USB drive
- Without explicit setting, the skill's auto-detection logic works but requires the USB to be mounted at the time of execution
- The skill was updated to clarify this behavior and prevent accidental SSD backups when USB is intended