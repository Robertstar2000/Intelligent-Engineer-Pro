# DreamHost File Manager — Browser Interaction Notes

## Access Methods

### Web File Manager (files.dreamhost.com)
- URL: `https://files.dreamhost.com`
- Requires SFTP credentials (may differ from panel password)
- Uses a Java/JS-based UI with React-style form controls
- **Known issue**: The auth type `<select>` element requires native value setter to work properly with the browser tool:
  ```javascript
  var nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLSelectElement.prototype, 'value').set;
  nativeSetter.call(selectElement, 'Password');
  selectElement.dispatchEvent(new Event('change', {bubbles: true}));
  ```
- **Known issue**: Input fields may reset if filled too quickly. Use `setTimeout` chains to fill fields sequentially.
- **Known issue**: Password fields appear only AFTER selecting "Password" auth type from the dropdown.

### DreamHost Panel File Manager
- URL: `https://panel.dreamhost.com/index.cgi?tree=files.filemanager`
- Uses panel credentials (email + password)
- May redirect to a different file manager interface
- The "SFTP Users & Files" section shows per-domain SFTP accounts with "File Manager" links

### Chrome Installation for Browser Tool
When `npx agent-browser install` fails (slow/unreliable download):
```bash
# Download Chrome for Testing directly
wget --continue --timeout=600 --tries=5 \
  "https://storage.googleapis.com/chrome-for-testing-public/149.0.7827.54/linux64/chrome-linux64.zip" \
  -O /tmp/chrome-linux64.zip

# Extract
python3 -c "
import zipfile, os
with zipfile.ZipFile('/tmp/chrome-linux64.zip', 'r') as z:
    z.extractall('/tmp/chrome-install')
"

# Move to agent-browser browsers directory
mkdir -p /home/bob/.agent-browser/browsers
cp -r /tmp/chrome-install/chrome-linux64 /home/bob/.agent-browser/browsers/chrome-linux64
chmod -R 755 /home/bob/.agent-browser/browsers/chrome-linux64/chrome-linux64/

# Verify
/home/bob/.agent-browser/browsers/chrome-linux64/chrome-linux64/chrome --version
```

## Credentials

### DreamHost Panel
- URL: https://panel.dreamhost.com
- Email: mifecoinc@gmail.com
- Password: (stored in user's memory — ask if needed)

### SFTP (dh_mwpxuu)
- Host: iad1-shared-b8-42.dreamhost.com
- Username: dh_mwpxuu
- Web root (mifeco.com): /home/dh_mwpxuu/mifeco.com/
- SFTP password may differ from panel password

## Image Upload Workflow

1. Log in to DreamHost panel at https://panel.dreamhost.com
2. Navigate to Websites → SFTP Users & Files
3. Find the "File Manager" link for the target domain
4. Navigate to the `images/` directory
5. Upload new images (overwrite existing ones)
6. Verify images render correctly on the live website

## Troubleshooting

- **"Email or password is incorrect"**: The panel login uses email (mifecoinc@gmail.com), not the SFTP username (dh_mwpxuu)
- **"SFTPAuthenticationMode must be one of Password..."**: The auth type select wasn't set properly — use native setter approach above
- **"remoteUsername must be non zero-length string"**: Input fields were cleared — fill all fields in a single synchronous operation using native value setters
- **Blank page after login**: The file manager may have opened in a new window that was blocked — try navigating directly to the file manager URL
