# DreamHost React SPA Navigation (Verified 2026-06-05)

The DreamHost panel (`panel.dreamhost.com`) is a React SPA (MUI-based). The accessibility tree returned by browser snapshots is often empty — you must use the browser console to navigate.

## Navigation Technique

```javascript
// Expand the Websites sidebar menu
var allBtns = document.querySelectorAll('button');
var wsBtn = null;
allBtns.forEach(function(b) {
  if (b.textContent.trim() === 'Websites') wsBtn = b;
});
wsBtn.click();

// Click submenu item
var links = document.querySelectorAll('#panel-navigation-app a, #panel-navigation-app button');
links.forEach(function(l) {
  if (l.textContent.trim() === 'Manage Websites') l.click();
});

// Find mifeco.com, click "Manage"
var main = document.querySelector('main');
var manageBtns = main.querySelectorAll('a, button');
manageBtns.forEach(function(el) {
  if (el.textContent.trim() === 'Manage') el.click();
});

// Then "Manage Files" for the file manager
main = document.querySelector('main');
main.querySelectorAll('a, button, span, div').forEach(function(el) {
  if (el.textContent.trim() === 'Manage Files') el.click();
});
```

## Heading Types (found in the DOM)

| Sidebar Item | Tag | Action |
|---|---|---|
| Home | `<a href="?tree=home.over">` | Click |
| Websites | `<button>` | Click to expand submenu |
| Manage Websites | `<a>` | Click after Websites expands |
| SFTP Users & Files | `<a>` | Click |
| MySQL Databases | `<button>` | Click |
| Remixer | `<a href="?tree=remixer.marketing">` | Click |
| Domain Names | `<button>` | Click |
| Mail | `<button>` | Click |
| Servers & Usage | `<a href="?tree=server.dashboard">` | Click |

## File Manager Structure

The file manager is an AngularJS-based file browser. Directory contents are rendered as a table with per-file action menus (Open, Edit, Download, Copy Name, Create Zip Archive, Upload, etc.).

Key actions on files: Click the filename to navigate into a directory. ".." goes up one level.

Upload triggers: The file manager has "Upload File…", "Upload Folder…", and "Upload Zip…" options. However, for file transfers over 10MB, use paramiko SFTP instead — it's faster and more reliable.

## SSH/SFTP (Preferred for Large Deployments)

```python
import paramiko
host = "IAD1-SHARED-B8-42.DREAMHOST.COM"
user = "dh_mwpxuu"
password = "Rm2214ri####"  # From ~/.hermes/secrets/

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, username=user, password=password, timeout=20)
sftp = client.open_sftp()

# Upload a file
sftp.put(local_path, remote_path)

# Execute a command
stdin, stdout, stderr = client.exec_command("ls -la /home/dh_mwpxuu/mifeco.com/")
print(stdout.read().decode())

sftp.close()
client.close()
```

## Important Directories (dh_mwpxuu user)

| Path | Purpose |
|---|---|
| `/home/dh_mwpxuu/mifeco.com/` | Main WordPress/SPA site |
| `/home/dh_mwpxuu/mifeco.com/books/` | Books section (mifeco.com/books) |
| `/home/dh_mwpxuu/mifeco.com/books/magnets/` | Free download PDFs/EPUBs |
| `/home/dh_mwpxuu/books.mifeco.com/` | Separate books subdomain |
| `/home/dh_mwpxuu/stage.mifeco.com/` | Staging site |
| `/home/dh_mwpxuu/wp-content/` | WordPress plugins/themes/uploads |