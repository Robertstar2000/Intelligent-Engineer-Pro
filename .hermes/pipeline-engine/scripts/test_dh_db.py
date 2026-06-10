#!/usr/bin/env python3
"""Test DB access on DreamHost."""
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

child.sendline('php -r "echo file_exists(\'/home/dh_mwpxuu/mifeco.com/admin/kanban.db\') ? \'DB EXISTS\' : \'DB NOT FOUND\'; echo PHP_EOL;"')
child.expect(r'\$', timeout=5)
print("DB existence:", child.before.strip())

child.sendline('ls -la ~/mifeco.com/admin/kanban.db')
child.expect(r'\$', timeout=5)
print("DB perms:", child.before.strip())

child.sendline('php -r "$db=new SQLite3(\'/home/dh_mwpxuu/mifeco.com/admin/kanban.db\'); $r=$db->query(\'SELECT COUNT(*) FROM tasks\'); echo $r->fetchArray()[0]; $db->close();"')
child.expect(r'\$', timeout=5)
print("DB query:", child.before.strip())

child.sendline('exit')
child.close()