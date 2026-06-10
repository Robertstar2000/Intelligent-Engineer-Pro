#!/usr/bin/env python3
"""Deploy kanban.db to DreamHost."""
import pexpect, sys, os

env_file = os.path.expanduser("~/.hermes/.env")
dh_pass = None
with open(env_file) as f:
    for line in f:
        if "DREAMHOST_PASSWORD" in line:
            dh_pass = line.strip().split("=", 1)[1]
            break

db_path = '/home/bob/.hermes/kanban.db'
db_size = os.path.getsize(db_path)
print(f"Local DB: {db_path} ({db_size} bytes)")

# Use scp via pexpect
cmd = (
    f'scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null '
    f'{db_path} '
    f'dh_mwpxuu@iad1-shared-b8-42.dreamhost.com:/home/dh_mwpxuu/mifeco.com/admin/kanban.db'
)

child = pexpect.spawn(cmd, timeout=60, encoding='utf-8')
idx = child.expect([r'[Pp]assword'], timeout=15)
if idx == 0:
    child.sendline(dh_pass)
child.expect(pexpect.EOF, timeout=30)
child.close()

if child.exitstatus == 0:
    # Verify on remote
    child2 = pexpect.spawn(
        'ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null '
        'dh_mwpxuu@iad1-shared-b8-42.dreamhost.com',
        timeout=30, encoding='utf-8'
    )
    child2.expect('[Pp]assword')
    child2.sendline(dh_pass)
    child2.expect(r'\$', timeout=15)
    child2.sendline('sqlite3 ~/mifeco.com/admin/kanban.db "SELECT COUNT(*) FROM tasks;"')
    child2.expect(r'\$', timeout=5)
    print("Remote DB task count:", child2.before.strip())
    child2.sendline('exit')
    child2.close()
else:
    print(f"SCP failed with exit code {child.exitstatus}")
