#!/usr/bin/env python3
"""Delete old SVG files from DreamHost that are no longer in local flows/."""
import pexpect, os, sys

env_file = os.path.expanduser("~/.hermes/.env")
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

child.sendline('ls ~/mifeco.com/admin/flows/*.svg')
child.expect(r'\$', timeout=5)
print("Before cleanup:")
print(child.before)

old_files = [
    'book-ideation-writing.svg', 'book-publishing.svg',
    'consulting-sales-deployment-report.svg', 'consulting-topic-ideation-writing.svg',
    'lead-generation.svg', 'promotion-generation.svg',
    'saas-branding-hosting-deployment.svg', 'saas-ideation-coding-testing.svg',
    'saas-sales-management.svg'
]

for f in old_files:
    child.sendline(f'rm -f ~/mifeco.com/admin/flows/{f}')
    child.expect(r'\$', timeout=5)

child.sendline('ls ~/mifeco.com/admin/flows/*.svg')
child.expect(r'\$', timeout=5)
print("\nAfter cleanup:")
print(child.before)

child.sendline('exit')
child.close()