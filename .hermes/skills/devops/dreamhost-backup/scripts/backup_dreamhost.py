#!/usr/bin/env python3
"""Backup DreamHost mifeco.com to USB drive."""
import pexpect
import os
import sys
from datetime import datetime

BACKUP_DIR = "/mnt/usb_4tb/Mifeco_Web_Backup"
REMOTE = "dh_mwpxuu@iad1-shared-b8-42.dreamhost.com"
REMOTE_PATH = "/home/dh_mwpxuu/mifeco.com/"

env_file = os.path.expanduser("~/.hermes/.env")
dh_pass = None
with open(env_file) as f:
    for line in f:
        if line.startswith("DREAMHOST_PASSWORD="):
            dh_pass = line.strip().split("=", 1)[1]
            break

if not dh_pass:
    print("ERROR: No DREAMHOST_PASSWORD found")
    sys.exit(1)

os.makedirs(BACKUP_DIR, exist_ok=True)

print(f"=== MIFECO DreamHost Backup ===")
print(f"Time: {datetime.now()}")

cmd = (
    f'rsync -avz --compress-level=6 '
    f'-e "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" '
    f'{REMOTE}:{REMOTE_PATH} {BACKUP_DIR}/'
)

print(f"Running rsync...\n")

child = pexpect.spawn(cmd, timeout=600, encoding='utf-8')
child.logfile_read = sys.stdout

try:
    idx = child.expect([r'[Pp]assword', r'passphrase'], timeout=60)
    if idx in (0, 1):
        child.sendline(dh_pass)
        print("\n[password sent, waiting for rsync...]")
except pexpect.TIMEOUT:
    print("\n[no password prompt after 60s]")

child.expect(pexpect.EOF, timeout=600)
child.close()

exit_code = child.exitstatus
print(f"\nrsync exit code: {exit_code}")

if exit_code in (0, 23, 24):
    print("\n=== Backup Complete ===")
    print(f"Time: {datetime.now()}")
    os.system(f'du -sh "{BACKUP_DIR}/"')
    os.system(f'find "{BACKUP_DIR}/" -type f | wc -l | xargs -I{{}} echo "Total files: {{}}"')
else:
    print(f"\nERROR: exit code {exit_code}")
    sys.exit(1)