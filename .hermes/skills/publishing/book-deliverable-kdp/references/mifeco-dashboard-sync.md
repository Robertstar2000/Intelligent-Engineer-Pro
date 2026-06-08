# MIFECO Dashboard Book Catalog Sync

## Problem
The MIFECO Pipeline Command Center (https://www.mifeco.com/admin/) shows "0 Books in Catalog" — hardcoded data that doesn't auto-populate from actual book files.

## Solution
A sync script reads all book directories on the USB drive and pushes data to WordPress REST API.

### Sync Script
Location: `/mnt/usb_4tb/books/sync_mifeco_catalog.py`

```bash
# Scan and save catalog (dry run)
python3 sync_mifeco_catalog.py --dry-run

# Push to MIFECO WordPress (requires app password)
python3 sync_mifeco_catalog.py --wp-user bobmills --wp-pass "xxxx xxxx xxxx xxxx xxxx"
```

### WordPress Setup Required
1. Log into MIFECO.com Admin
2. Go to Users > Your Profile > Application Passwords
3. Create a new application password for "Hermes Agent"
4. Use that password with `--wp-pass`

### Catalog JSON
Auto-generated at: `/mnt/usb_4tb/books/book_catalog.json`

### Desktop Shortcuts
- KDP_Packages → `/home/bob/books/KDP_Packages/` (symlinks to all book dirs)
- MIFESCO_Dashboard → `https://www.mifeco.com/admin/`
- USB_4TB → `/mnt/usb_4tb`
