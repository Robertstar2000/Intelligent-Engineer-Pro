#!/usr/bin/env python3
"""Check DreamHost file permissions and fix kanban access."""
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

# Check file permissions
child.sendline('ls -la ~/mifeco.com/admin/.htaccess ~/mifeco.com/admin/kanban-dashboard.html ~/mifeco.com/admin/kanban-data.php ~/mifeco.com/admin/index.php 2>&1')
child.expect(r'\$', timeout=5)
print("=== File permissions ===")
print(child.before)

# Check if there's a data directory that might conflict
child.sendline('ls -la ~/mifeco.com/admin/ 2>&1')
child.expect(r'\$', timeout=5)
print("\n=== Admin directory listing ===")
print(child.before)

# Check if mod_rewrite is enabled
child.sendline('apache2ctl -M 2>&1 | grep rewrite || httpd -M 2>&1 | grep rewrite || echo "Cannot check modules"')
child.expect(r'\$', timeout=5)
print("\n=== mod_rewrite ===")
print(child.before)

# Check error logs
child.sendline('tail -20 ~/logs/*/error.log 2>/dev/null || echo "No error logs found"')
child.expect(r'\$', timeout=5)
print("\n=== Error logs ===")
print(child.before)

# Fix permissions if needed
child.sendline('chmod 644 ~/mifeco.com/admin/.htaccess ~/mifeco.com/admin/kanban-dashboard.html ~/mifeco.com/admin/kanban-data.php 2>&1')
child.expect(r'\$', timeout=5)
print("\n=== chmod result ===")
print(child.before)

# Also check if there's a data/ directory in admin that could conflict
child.sendline('test -d ~/mifeco.com/admin/data && echo "DATA DIR EXISTS" || echo "No data dir"')
child.expect(r'\$', timeout=5)
print("\n=== data dir check ===")
print(child.before)

child.sendline('exit')
child.close()