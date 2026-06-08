# Image Upload via SCP + pexpect

When sshpass is not available, use Python's pexpect module for password-based SCP uploads.

## Prerequisites

- `pexpect` is available in the system Python (`python3 -c "import pexpect"`)
- The remote server allows password auth over SSH
- File: `/home/bob/.hermes/skills/devops/mifeco-website-deployment/images/` contains source images

## Single File Upload

```python
import pexpect

SERVER = "dh_mwpxuu@iad1-shared-b8-42.dreamhost.com"
REMOTE_PATH = "/home/dh_mwpxuu/mifeco.com/books/images/"
PASSWORD = "[stored in .env]"
LOCAL_FILE = "/path/to/local/file.jpg"

child = pexpect.spawn(f"scp -o StrictHostKeyChecking=no {LOCAL_FILE} {SERVER}:{REMOTE_PATH}", timeout=30)
child.expect("password:")
child.sendline(PASSWORD)
child.expect(pexpect.EOF, timeout=30)
```

## Batch Upload via Tarball

For 5+ files, create a tarball locally, upload it, then extract on the server:

```python
import pexpect, tarfile, os, time

# 1. Create tarball
local_dir = "/path/to/local/images"
tar_path = "/tmp/images.tar.gz"
with tarfile.open(tar_path, "w:gz") as tar:
    for f in os.listdir(local_dir):
        tar.add(os.path.join(local_dir, f), arcname=f)

# 2. Upload tarball
child = pexpect.spawn(f"scp {tar_path} {SERVER}:{REMOTE_PATH}", timeout=120)
child.expect("password:")
child.sendline(PASSWORD)
child.expect(pexpect.EOF, timeout=120)

# 3. Extract on server
child2 = pexpect.spawn(f"ssh -o StrictHostKeyChecking=no {SERVER}", timeout=60)
child2.expect("password:")
child2.sendline(PASSWORD)
time.sleep(2)
child2.sendline(f"cd {REMOTE_PATH} && tar xzf images.tar.gz && rm images.tar.gz")
```

## Verifying Upload

```python
child = pexpect.spawn(f"ssh -o StrictHostKeyChecking=no {SERVER}", timeout=60)
child.expect("password:")
child.sendline(PASSWORD)
time.sleep(2)
child.sendline(f"ls -la {REMOTE_PATH} | wc -l")
```

## Pitfalls

- **pexpect $ interpretation**: `sendline()` interprets `$` characters — use `send()` for strings containing PHP `$` variables
- **Timeout**: Single large files (>5MB) may need `timeout=120`
- **Key auth fallback**: If password auth keeps failing, set up SSH key on DreamHost panel: Users → SSH Keys → Add Public Key