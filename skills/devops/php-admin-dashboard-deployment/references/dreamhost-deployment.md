# DreamHost Shared Hosting — Deployment Reference

## SSH/SFTP Status (2026-06-03, updated 2026-06-03)

DreamHost **shared hosting** does NOT provide SSH access, but **SFTP works on port 22** with the correct password.

| Port | Protocol | Status | Notes |
|------|----------|--------|-------|
| 22 | SSH | Connection refused | Shell access disabled on shared hosting |
| 22 | **SFTP** | **Works** | Use `paramiko.Transport((host, 22))` + `SFTPClient` |
| 21 | FTP | Connects, but panel password ≠ FTP password | Requires separate FTP user |
| 2222 | SSH (alt) | Timeout | Not available |

## Critical: SFTP Password ≠ Panel Password

The SFTP password is **`Rm2214ri####`** (with `####` suffix). This was discovered by decoding the file manager token from the DreamHost panel URL at `us-east-files.dreamhost.com`:

```python
import base64, json
token = "eyJ0Ijoic2Z0cCIsImMiOnsidiI6MCwicCI6IlJtMjIxNHJpIyMjIyIsInMiOjAsIm0iOiJQYXNzd29yZCJ9fQ=="
decoded = json.loads(base64.b64decode(token))
# Result: {'t': 'sftp', 'c': {'v': 0, 'p': 'Rm2214ri####', ...}}
```

## SFTP Deployment (Recommended Method)

```python
import paramiko
import os

host = "iad1-shared-b8-42.dreamhost.com"
user = "dh_mwpxuu"
password = "Rm2214ri####"

transport = paramiko.Transport((host, 22))
transport.connect(username=user, password=password)
sftp = paramiko.SFTPClient.from_transport(transport)

# Upload a file
sftp.put("/local/path/file.html", "/remote/path/file.html")

# Create remote directories
try:
    sftp.mkdir("/remote/path/newdir")
except:
    pass  # Already exists

# Upload recursively
def upload_dir(local_dir, remote_dir):
    for item in os.listdir(local_dir):
        local_path = os.path.join(local_dir, item)
        remote_path = f"{remote_dir}/{item}"
        if os.path.isdir(local_path):
            try:
                sftp.mkdir(remote_path)
            except:
                pass
            upload_dir(local_path, remote_path)
        else:
            sftp.put(local_path, remote_path)

sftp.close()
transport.close()
```

**Pattern:** Wrap in `execute_code` tool. Always skip `data/` directories containing subscriber CSVs.

## MIFECO.com Specifics

- **Web root**: `/home/dh_mwpxuu/mifeco.com/`
- **SSH host**: `iad1-shared-b8-42.dreamhost.com`
- **SFTP user**: `dh_mwpxuu`
- **SFTP password**: `Rm2214ri####`
- **Panel login**: `rmills@mifeco.com` / `Rm2214ri####` (or `MIFECOinc@gmail.com`)
- **WordPress**: Co-located at web root (not subdirectory)
- **SPA**: Vite/React built to `dist/`, deployed to web root
- **nginx**: Front-end web server (not Apache), `.htaccess` ignored
- **PHP router**: `index.php` handles routing between SPA and WordPress
- **Books section**: `/books/` subdirectory (static HTML + PHP)
- **Never use `--delete`** in rsync — WordPress lives in the same root

## File Manager (Fallback)

DreamHost Panel File Manager is at `us-east-files.dreamhost.com`. The URL contains a base64-encoded token with SFTP credentials. The file manager UI:
- Requires double-click to enter directories (single click doesn't navigate)
- Has upload button (⬆) but may show error if no file is pre-selected
- Works best for small uploads; use paramiko SFTP for bulk deployment

## Credentials

| Service | Username | Password | Notes |
|---------|----------|----------|-------|
| DreamHost Panel | rmills@mifeco.com | Rm2214ri#### | Panel login |
| DreamHost Panel | MIFECOinc@gmail.com | Rm2214ri#### | Alternative email |
| SFTP | dh_mwpxuu | Rm2214ri#### | File upload |
| WordPress Admin | mifeco_6eexpm | (SSO only) | Must use DreamHost SSO |
| SSH | dh_mwpxuu | (disabled) | Shell access not available on shared hosting |
| FTP | (none created) | — | Must create separate FTP user in panel |
