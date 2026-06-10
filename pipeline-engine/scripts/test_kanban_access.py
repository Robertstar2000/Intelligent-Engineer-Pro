#!/usr/bin/env python3
"""Fix DreamHost kanban access: permissions, .htaccess, and test."""
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

# 1. Fix permissions - DreamHost needs 0644 for HTML, 0644 for PHP
child.sendline('chmod 644 ~/mifeco.com/admin/kanban-dashboard.html ~/mifeco.com/admin/kanban-data.php ~/mifeco.com/admin/.htaccess')
child.expect(r'\$', timeout=5)
print("=== Permissions fixed ===")
print(child.before)

# 2. Verify permissions
child.sendline('ls -la ~/mifeco.com/admin/kanban-dashboard.html ~/mifeco.com/admin/kanban-data.php ~/mifeco.com/admin/.htaccess')
child.expect(r'\$', timeout=5)
print("\n=== Current permissions ===")
print(child.before)

# 3. Check if there's an ErrorDocument directive causing issues
child.sendline('grep -r ErrorDocument ~/mifeco.com/admin/.htaccess ~/mifeco.com/.htaccess 2>/dev/null')
child.expect(r'\$', timeout=5)
print("\n=== ErrorDocument directives ===")
print(child.before)

# 4. Test fetching the HTML file directly via curl
child.sendline('curl -s -o /tmp/kanban_test.html -w "%{http_code}" https://mifeco.com/admin/kanban-dashboard.html 2>&1')
child.expect(r'\$', timeout=10)
print("\n=== HTTP status for kanban-dashboard.html ===")
print(child.before)

# 5. Check the actual content returned
child.sendline('head -5 /tmp/kanban_test.html 2>/dev/null')
child.expect(r'\$', timeout=5)
print("\n=== First 5 lines ===")
print(child.before)

# 6. Test kanban-data.php
child.sendline('curl -s -o /tmp/kanban_data_test.json -w "%{http_code}" https://mifeco.com/admin/kanban-data.php 2>&1')
child.expect(r'\$', timeout=10)
print("\n=== HTTP status for kanban-data.php ===")
print(child.before)

child.sendline('head -3 /tmp/kanban_data_test.json 2>/dev/null')
child.expect(r'\$', timeout=5)
print("\n=== First 3 lines of JSON ===")
print(child.before)

# 7. Also test via index.php gate
child.sendline('curl -s -o /tmp/index_test.html -w "%{http_code}" https://mifeco.com/admin/ 2>&1')
child.expect(r'\$', timeout=10)
print("\n=== HTTP status for admin/ ===")
print(child.before)

child.sendline('grep -c "kanban" /tmp/index_test.html 2>/dev/null')
child.expect(r'\$', timeout=5)
print("\n=== Kanban link in index.php? ===")
print(child.before)

child.sendline('exit')
child.close()