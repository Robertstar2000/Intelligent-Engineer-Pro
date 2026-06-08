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
