# DreamHost File Manager & SCP Upload — Lessons Learned (2026-06-04)

## File Manager Access Path

The correct path to access the file manager for dh_mwpxuu:
1. DreamHost panel → Websites → SFTP Users & Files
2. Find the user row (dh_mwpxuu for mifeco.com)
3. Click the "File Manager" BUTTON (not link) in that row
4. This opens https://us-east-files.dreamhost.com/ with pre-filled credentials

Do NOT navigate to https://files.dreamhost.com/ directly — the standalone login form has an authentication bug where the SFTP password doesn't work with "Password" auth mode. Always use the panel's File Manager button.

## SCP Upload via pexpect

When uploading files via SCP with pexpect, write files locally first, then SCP. Do NOT use pexpect sendline to write PHP files containing $ signs — pexpect interprets $ as shell variables and strips them.

Correct pattern:
1. Write file locally: open('/tmp/router.php', 'w').write(content)
2. SCP the file: pexpect.spawn(f"scp ... /tmp/router.php {SERVER}:{REMOTE_PATH}/")

Wrong pattern (strips $ signs):
child.sendline(f"cat > router.php << 'EOF'\n{content}\nEOF")

## Image Naming Convention Mismatch

When replacing images on a live site, the HTML may reference old naming conventions:
- Old: images/infographic-series-name.png
- New: images/series-name-infographic.png

Solution: Create symlinks for old names pointing to new files:
ln -sf age-of-lightships-infographic.png infographic-age-of-lightships.png

## Router.php for Subdirectory Sites

When a static HTML site lives inside a WordPress subdirectory (/books/), a router.php is needed. Write router.php locally and SCP it — do NOT use shell heredocs or pexpect sendline for PHP files with $ variables.

## Disk Space

Root partition is 117GB. Check before large operations: df -h /

## Chrome Installation

If npx agent-browser install times out downloading Chrome (177MB):
wget --continue --timeout=600 "https://storage.googleapis.com/chrome-for-testing-public/149.0.7827.54/linux64/chrome-linux64.zip" -O /tmp/chrome-linux64.zip
python3 -c "import zipfile; zipfile.ZipFile('/tmp/chrome-linux64.zip').extractall('/tmp/chrome-install')"
cp -r /tmp/chrome-install/chrome-linux64 /home/bob/.agent-browser/browsers/
chmod -R 755 /home/bob/.agent-browser/browsers/chrome-linux64/

Chrome requires --no-sandbox flag on this system.

## ⚠️ Shell-Special Characters in Passwords (2026-06-08)

When a password contains `#`, `*`, or other shell-special characters, writing it to files via shell commands fails in multiple ways:

| Character | Failure mode |
|-----------|-------------|
| `#` | Treated as shell comment start — everything after `#` is silently dropped |
| `***` | Glob-expanded to match files in current directory |
| `$var` | Expanded as shell variable |
| `!` | History expansion in bash |

**Failed approaches (all silently corrupt the password):**
- `echo "PASSWORD" >> .env` — `#` starts comment, `***` glob-expands
- `python3 -c "s = "PASSWORD""` — `#` starts Python comment inside shell heredoc
- Python triple-quoted strings passed through shell — `#` interpreted by shell before Python sees it

**Working approach — base64 encode/decode:**
```python
import base64, subprocess

pw = "Rm2214ri####"
pw_b64 = base64.b64encode(pw.encode()).decode()

# Decode inline when writing
subprocess.run(['sed', '-i', f's/DREAMHOST_PASSWORD=***/DREAMHOST_PASSWORD=*** + base64.b64decode(pw_b64).decode() + "}/', '.env'])
```

**Alternative — chr() construction in a .py script file (not inline):**
```python
pw = "Rm2214ri" + chr(35)*4  # chr(35) = '#'
```

**Key rule: Never pass passwords with special characters through shell strings. Use file I/O or base64.**

## ⚠️ Always Test Auth Before Assuming the Password (2026-06-08)

The user may state a password that differs from the actual working password. Always test with a quick SSH probe before updating multiple files:
```python
import pexpect, os
os.system("ssh-keygen -R 'host' 2>/dev/null")
child = pexpect.spawn(f"ssh -o StrictHostKeyChecking=accept-new user@host 'echo OK'", timeout=20)
child.expect_exact(["password:", "Password:"])
child.sendline(password)
child.expect(pexpect.EOF)
print(child.before)
```

If the first password fails, try variations (different number of `#` characters, `!` vs `#`, etc.) before concluding auth is broken.

## ⚠️ Multi-Location File Sync (2026-06-08)

When the same file exists in multiple locations (e.g., `dashboard/index.php` in both `.hermes/pipeline-engine/` and `FL-Hermes/`), editing one copy does NOT update the other. The second copy silently diverges.

**After editing a shared file, explicitly sync:**
```bash
cp /home/bob/.hermes/pipeline-engine/dashboard/index.php /home/bob/FL-Hermes/pipeline-engine/dashboard/index.php
```
