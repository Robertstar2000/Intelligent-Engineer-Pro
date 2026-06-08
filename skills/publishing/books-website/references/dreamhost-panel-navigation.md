# DreamHost Deployment (Verified June 2026)

## Login

- **Panel:** https://panel.dreamhost.com
- **Email:** MIFECOinc@gmail.com
- **Password:** Rm2214ri####

## SSH Access (Preferred — Fast & Reliable)

SSH is accessible via password authentication. **Paramiko is the recommended method**, not pexpect or the panel file manager.

```python
import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('IAD1-SHARED-B8-42.DREAMHOST.COM', username='dh_mwpxuu', password='Rm2214ri####', timeout=20)
sftp = client.open_sftp()
sftp.put(local_path, remote_path)    # upload
sftp.get(remote_path, local_path)    # download
sftp.close()
client.close()
```

**Web root:** `/home/dh_mwpxuu/mifeco.com/books/`
**User home:** `/home/robertstar/` (panel user — different from dh_mwpxuu)

### Server Details
- Host: iad1-shared-b8-42.dreamhost.com
- Username: dh_mwpxuu (web root owner)
- Password: Rm2214ri####
- PHP: Available, `php -l file.php` before deploy
- Filesystem: Linux (case-sensitive)

## Panel File Manager (Alternative)

1. `https://panel.dreamhost.com` → log in with MIFECOinc@gmail.com / Rm2214ri####
2. Left sidebar → **Websites** → The Websites button is a `<button>` element (not `<a>`), click it to expand sub-menu
3. Click **SFTP Users & Files** in the sub-menu
4. Find `dh_mwpxuu` user row → File Manager button
5. Navigate to target directory, upload ZIP or individual files
6. **Panel is a React SPA** — direct URL navigation fails in headless browser. Use sidebar buttons with native click events. Synthetic clicks on `<button>` elements need `dispatchEvent(new MouseEvent('click', {bubbles: true}))`.

## Deployment Methods (in order of preference)

### Method 1: Paramiko SFTP (Fastest — Batch Upload)
```python
def upload_batch(files_dict):  # {remote_rel_path: local_abs_path}
    remote_base = "/home/dh_mwpxuu/mifeco.com/books"
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('IAD1-SHARED-B8-42.DREAMHOST.COM', username='dh_mwpxuu', password='Rm2214ri####', timeout=20)
    sftp = client.open_sftp()
    for rel, local in files_dict.items():
        sftp.put(local, f"{remote_base}/{rel}")
    sftp.close(); client.close()
```

### Method 2: ZIP + Panel File Manager
```bash
cd /mnt/usb_4tb/books/books-section && \
zip -r /tmp/books-deploy.zip . --exclude "*.git*" --exclude "*__pycache__*"
```
Then upload and extract via Panel → File Manager.

**NEVER use `--delete`** on the web root — SPA, WordPress, and static site coexist.

## Critical Deployment Pitfalls

- **Case sensitivity:** Linux servers are case-sensitive. `author-photo.jpg` ≠ `Author_Photo.jpg`.
- **Old file residue:** Old images with different naming conventions (e.g., `ai-agents-cover.png`, `series_infographic.png`, `NBS_*.png`) remain after new uploads. Consider cleanup if disk space is tight.
- **Router PHP variable escaping:** Writing PHP via SSH heredocs strips `$` signs. Always write PHP files locally, SFTP them.
- **subscribers.json permissions:** Must be writable by web server user. Create with `touch` and `chmod 644`.
- **PHP .htaccess:** DreamHost uses nginx, NOT Apache. `.htaccess` files are completely ignored. Use PHP router in `index.php` for URL rewriting.

## Verification After Deploy

```bash
# Check all new images return 200
for url in $(grep -oP 'src="/books/images/[^"]+' index.html | sed 's/src="//'); do
    curl -s -o /dev/null -w "$url -> %{http_code}\n" "https://www.mifeco.com$url"
done

# Check API endpoint
curl -X POST https://www.mifeco.com/books/api/subscribe.php \
  -d "first_name=Test&email=test@example.com" | python3 -m json.tool
```

## Local Backup Sync

A cron job (`sync-subscriber-db`) runs daily at 2AM to sync subscriber data:
```bash
/home/bob/.hermes/scripts/sync-subscribers.sh
```
This uses paramiko to copy `subscribers.json` from DreamHost to `/mnt/usb_4tb/books/books-section/api/subscribers.json` so it's included in the nightly Hermes backup.