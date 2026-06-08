# DreamHost File Manager Login — Detailed Steps

## URL
`https://files.dreamhost.com/`

## Credentials Needed
- **Host:** `iad1-shared-b8-42.dreamhost.com`
- **Username:** `dh_mwpxuu`
- **Initial Directory:** `/home/dh_mwpxuu/mifeco.com` (or `books.mifeco.com`)
- **Password:** SFTP-specific password (NOT the DreamHost panel password)

## Step-by-Step Login

1. Navigate to `https://files.dreamhost.com/`
2. Wait for page to load (snapshot should show Login dialog)
3. Fill text fields (use `browser_type` with fresh refs):
   - Host: `iad1-shared-b8-42.dreamhost.com`
   - Username: `dh_mwpxuu`
   - Initial Directory: `/home/dh_mwpxuu/mifeco.com`
4. **Select Password auth type** — this is the tricky part:
   - Click the Authentication Type combobox (ref varies)
   - Wait for dropdown to expand
   - Click "Password" option
   - Verify: snapshot should show "Password" selected
5. **Fill password fields** — two fields appear after selecting Password:
   - Use JS: `document.querySelectorAll('input[type="password"]')` to find them
   - Fill both with the SFTP password
   - Dispatch `input` and `change` events
6. Click "Connect" button
7. Wait 10-15 seconds for connection

## Error Messages

| Error | Cause | Fix |
|-------|-------|-----|
| "SFTPAuthenticationMode must be one of..." | Auth type not selected | Re-select Password from dropdown |
| "An unknown error occurred during authentication" | Wrong password | Ask user for SFTP-specific password |
| Page goes to `about:blank` | Popup blocked | Use panel's File Manager link instead |
| "Unknown ref" | Stale snapshot | Re-snapshot after navigation |

## Alternative: Panel File Manager Link

If files.dreamhost.com fails:
1. Log into https://panel.dreamhost.com
2. Navigate to Websites → SFTP Users & Files
3. Find the `dh_mwpxuu` row
4. Click "File Manager" link (opens in new tab with pre-filled creds)

## File Upload Workflow

Once connected in file manager:
1. Navigate to target directory (e.g., `/home/dh_mwpxuu/mifeco.com/images/`)
2. Use the upload button (⬆ icon in toolbar)
3. Select files from local system
4. Wait for upload to complete
5. Verify files appear in listing

## Troubleshooting

- **Connection timeout:** Server may be slow; wait 30+ seconds
- **"No space left on device" on local side:** Clean /tmp on root partition (see disk space management in main SKILL.md)
- **Files not appearing after upload:** Refresh (🔄 button) or re-connect
