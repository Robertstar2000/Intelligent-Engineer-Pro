#!/usr/bin/env python3
"""Push kanban.db to DreamHost."""
import pexpect, sys

env_file = "/home/bob/.hermes/.env"
dh_pass = None
with open(env_file) as f:
    for line in f:
        if "DREAMHOST_PASSWORD" in line:
            dh_pass = line.strip().split("=", 1)[1]
            break

child = pexpect.spawn(
    'ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null '
    'dh_mwpxuu@iad1-shared-b8-42.dreamhost.com',
    timeout=30, encoding='utf-8'
)
child.expect('[Pp]assword')
child.sendline(dh_pass)
child.expect(r'\$', timeout=15)

# Check if SQLite3 works on DreamHost
child.sendline('which sqlite3 2>/dev/null && echo FOUND || echo NOT_FOUND')
child.expect(r'\$', timeout=5)
print("sqlite3:", child.before.strip())

# Check PHP SQLite support
child.sendline('php -m 2>&1 | grep -i sqlite')
child.expect(r'\$', timeout=5)
print("PHP SQLite:", child.before.strip())

# Check if we can write to the admin dir
child.sendline('touch ~/mifeco.com/admin/test_write && echo OK && rm ~/mifeco.com/admin/test_write')
child.expect(r'\$', timeout=5)
print("Write test:", child.before.strip())

child.sendline('exit')
child.close()