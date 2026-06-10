#!/usr/bin/env python3
"""Verify consulting dashboard fixes on DreamHost."""
import pexpect, os

env_file = os.path.expanduser("~/.hermes/.env")
dh_pass = None
with open(env_file) as f:
    for line in f:
        if line.startswith("DREAMHOST_PASSWORD="):
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

# Check survey.php has backdoor handler
child.sendline("grep -c 'backdoor' ~/mifeco.com/consult/survey.php")
child.expect(r'\$', timeout=5)
print(f"backdoor references in survey.php: {child.before.strip()}")

# Check admin has consulting link
child.sendline("grep -c 'consult' ~/mifeco.com/admin/index.php")
child.expect(r'\$', timeout=5)
print(f"consult references in admin/index.php: {child.before.strip()}")

# Check consulting tables
child.sendline("mysql -u ak48bme -pwormh0me wormh0me -e \"SHOW TABLES LIKE 'consulting_%'\" 2>/dev/null")
child.expect(r'\$', timeout=5)
print(f"Consulting tables:\n{child.before}")

# Verify pay.php table names
child.sendline("grep -E '(INSERT INTO|payments|surveys|consulting_payments|consulting_surveys|consulting_activity)' ~/mifeco.com/consult/pay.php")
child.expect(r'\$', timeout=5)
print(f"pay.php table references:\n{child.before}")

child.sendline('exit')
child.close()