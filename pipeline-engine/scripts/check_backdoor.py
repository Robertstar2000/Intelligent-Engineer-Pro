#!/usr/bin/env python3
"""Check and fix survey.php backdoor on DreamHost."""
import pexpect, os, sys

env_file = os.path.expanduser("~/.hermes/.env")
dh_pass = None
with open(env_file) as f:
    for line in f:
        if line.startswith("DREAMHOST_PASSWORD=***            dh_pass = line.strip().split("=", 1)[1]
            break

# Use SSH with SSH_ASKPASS to handle password interactively
import subprocess
result = subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-o', 'UserKnownHostsFile=/dev/null',
    'dh_mwpxuu@iad1-shared-b8-42.dreamhost.com',
    'grep -n "backdoor" ~/mifeco.com/consult/survey.php || echo "NOT_FOUND"'],
    capture_output=True, text=True, timeout=15)
print("stdout:", result.stdout)
print("stderr:", result.stderr)
print("returncode:", result.returncode)