#!/usr/bin/env python3
"""
SSH/SCP helper for MIFECO blog publishing
Uses pexpect for password-authenticated SSH/SCP to DreamHost.

Usage:
    python3 ssh_blog.py ensure_dirs
    python3 ssh_blog.py scp <local_path> <remote_path>
    python3 ssh_blog.py verify <slug>
    python3 ssh_blog.py wp_publish <title> <slug> <category> <tags> <content_file> <featured_image>
    python3 ssh_blog.py ssh <command...>
"""

import os
import sys
import pexpect
import subprocess

DHP = 'dh_mwpxuu@IAD1-SHARED-B8-42.DREAMHOST.COM'
REMOTE_BASE = '/home/dh_mwpxuu/mifeco.com'

def get_password():
    """Read DREAMHOST_PASSWORD from ~/.hermes/.env at runtime (never hardcode)."""
    result = subprocess.run(
        ['bash', '-c', 'source ~/.hermes/.env && echo "$DREAMHOST_PASSWORD"'],
        capture_output=True, text=True, timeout=10
    )
    return result.stdout.strip()

PASSWORD = get_password()

def ssh_run(command, timeout=60):
    """Run command on DreamHost via SSH."""
    child = pexpect.spawn('ssh', [
        '-o', 'StrictHostKeyChecking=accept-new',
        DHP, command
    ], timeout=timeout)
    child.expect('password:')
    child.sendline(PASSWORD)
    child.expect(pexpect.EOF, timeout=timeout)
    return child.before.decode() if child.before else ''

def scp_upload(local_path, remote_path, timeout=180):
    """Upload file via SCP. Returns True on success."""
    child = pexpect.spawn('scp', [
        '-o', 'StrictHostKeyChecking=accept-new',
        local_path,
        f'{DHP}:{remote_path}'
    ], timeout=60)
    child.expect('password:')
    child.sendline(PASSWORD)
    child.expect(pexpect.EOF, timeout=60)
    output = child.before.decode() if child.before else ''
    if 'failed to upload' in output.lower() or 'no such file' in output.lower():
        return False
    return True

def ensure_remote_dirs():
    """Create remote directories for tmp and images."""
    return ssh_run("mkdir -p /home/dh_mwpxuu/mifeco.com/tmp /home/dh_mwpxuu/mifeco.com/images")

def verify_uploads(slug):
    """Verify files landed on remote server."""
    verify = ssh_run(f"ls -la {REMOTE_BASE}/tmp/{slug}.html {REMOTE_BASE}/images/{slug}.png", timeout=15)
    return "No such file" not in verify

def wp_publish(title, slug, category, tags, content_file, featured_image):
    """Publish to WordPress via PHP CLI. Returns JSON output."""
    # Double quotes inside single-quoted string for PHP getopt()
    cmd = (
        f'cd {REMOTE_BASE} && '
        f'php scripts/wp-publish-post.php '
        f'--title="{title}" '
        f'--slug="{slug}" '
        f'--category="{category}" '
        f'--tags="{tags}" '
        f'--content-file="{content_file}" '
        f'--featured-image="{featured_image}"'
    )
    return ssh_run(cmd, timeout=240)  # 240s timeout for WP publish

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ssh_blog.py <command> [args...]")
        print("Commands: ensure_dirs, scp <local> <remote>, verify <slug>, wp_publish <title> <slug> <category> <tags> <content_file> <featured_image>, ssh <command...>")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == "ensure_dirs":
        print(ensure_remote_dirs())
    elif cmd == "scp" and len(sys.argv) == 4:
        print("OK" if scp_upload(sys.argv[2], sys.argv[3]) else "FAIL")
    elif cmd == "verify" and len(sys.argv) == 3:
        print("OK" if verify_uploads(sys.argv[2]) else "FAIL")
    elif cmd == "wp_publish" and len(sys.argv) >= 8:
        print(wp_publish(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7]))
    elif cmd == "ssh" and len(sys.argv) >= 3:
        print(ssh_run(" ".join(sys.argv[2:])))
    else:
        print("Invalid command or arguments")
        sys.exit(1)