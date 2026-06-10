#!/usr/bin/env python3
"""Push kanban.db to DreamHost so the data endpoint works there too."""
import pexpect, sys

env_file = "/home/bob/.hermes/.env"
dh_pass = None
with open(env_file) as f:
    for line in f:
        if "DREAMHOST_PASSWORD" in line:
            dh_pass = line.strip().split("=", 1)[1]
            break

# Check if we can find a writable directory on DreamHost
child = pexpect.spawn(
    'ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null '
    'dh_mwpxuu@iad1-shared-b8-42.dreamhost.com',
    timeout=30, encoding='utf-8'
)
child.expect('[Pp]assword')
child.sendline(dh_pass)
child.expect(r'\$', timeout=15)

# Test two approaches:
# 1. Can we write to admin/kanban.db?
child.sendline('php -r "\$db = new SQLite3(\"/home/dh_mwpxuu/mifeco.com/admin/kanban.db\"); \$db->exec(\"CREATE TABLE IF NOT EXISTS tasks (id TEXT PRIMARY KEY, title TEXT, body TEXT, assignee TEXT, status TEXT, priority INTEGER, tenant TEXT, stage INTEGER, created_at INTEGER, created_by TEXT)\"); echo \"SQLite works: \" . \$db->lastErrorCode(); \$db->close();" 2>&1')
child.expect(r'\$', timeout=10)
echo_line = child.before
print("=== SQLite test on DreamHost ===")
print(echo_line)

child.sendline('exit')
child.close()