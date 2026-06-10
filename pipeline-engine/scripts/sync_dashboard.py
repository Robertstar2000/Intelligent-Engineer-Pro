#!/usr/bin/env python3
"""Sync dashboard to DreamHost."""
import pexpect, os, sys

env_file = os.path.expanduser("~/.hermes/.env")
dh_pass = None
with open(env_file) as f:
    for line in f:
        if line.startswith("DREAMHOST_PASSWORD="):
            dh_pass = line.strip().split("=", 1)[1]
            break

cmd = (
    'rsync -avz --compress-level=6 '
    '-e "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" '
    '/home/bob/.hermes/pipeline-engine/dashboard/ '
    'dh_mwpxuu@iad1-shared-b8-42.dreamhost.com:/home/dh_mwpxuu/mifeco.com/admin/'
)

print("Syncing to DreamHost...")
child = pexpect.spawn(cmd, timeout=300, encoding='utf-8')
child.logfile_read = sys.stdout

idx = child.expect([r'[Pp]assword', r'passphrase'], timeout=30)
if idx in (0, 1):
    child.sendline(dh_pass)
    print("[sent password]")

child.expect(pexpect.EOF, timeout=300)
child.close()

print(f"\nrsync exit: {child.exitstatus}")
if child.exitstatus in (0, 23, 24):
    print("DreamHost sync complete")
else:
    print(f"exit code {child.exitstatus}")
