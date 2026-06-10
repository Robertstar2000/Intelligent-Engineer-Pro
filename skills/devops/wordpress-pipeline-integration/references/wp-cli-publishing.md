# WordPress CLI Publishing via PHP Script (DreamHost)

For publishing blog posts to WordPress from the agent (especially cron jobs), use a PHP CLI script on the DreamHost server. This avoids REST API authentication issues and works reliably over SSH.

## Script: `wp-publish-post.php`

Located at `/home/dh_mwpxuu/mifeco.com/scripts/wp-publish-post.php` on DreamHost.

### Usage

```bash
cd /home/dh_mwpxuu/mifeco.com && php scripts/wp-publish-post.php \
  --title="Post Title" \
  --content-file=/home/dh_mwpxuu/mifeco.com/tmp/slug.html \
  --slug=post-slug \
  --category="Books" \
  --tags="tag1,tag2" \
  --featured-image=/home/dh_mwpxuu/mifeco.com/images/slug.png
```

### Key Details
- Content is read from a **file** (not CLI arg) to avoid shell escaping issues with HTML
- Requires `wp-load.php` AND `wp-admin/includes/taxonomy.php` (for `wp_create_category()`)
- Returns JSON: `{"success": true, "post_id": 42, "post_url": "https://www.mifeco.com/slug/", ...}`
- Duplicate slug detection built in

## Publishing Workflow from Agent (pexpect)

```python
import pexpect, json

DHP = 'dh_mwpxuu@IAD1-SHARED-B8-42.DREAMHOST.COM'
PW = 'Rm2214ri####'

def ssh_run(cmd, timeout=60):
    child = pexpect.spawn('ssh', [
        '-o', 'StrictHostKeyChecking=accept-new',
        '-o', 'PubkeyAuthentication=no', DHP, cmd
    ], timeout=timeout)
    child.expect('password:')
    child.sendline(PW)
    child.expect(pexpect.EOF, timeout=timeout)
    return child.before.decode()

def scp_upload(local, remote, timeout=60):
    remote_dir = remote.rsplit('/', 1)[0]
    ssh_run(f'mkdir -p {remote_dir}')  # CRITICAL: SCP can't create dirs
    child = pexpect.spawn('scp', [
        '-o', 'StrictHostKeyChecking=accept-new',
        '-o', 'PubkeyAuthentication=no', local, f'{DHP}:{remote}'
    ], timeout=timeout)
    child.expect('password:')
    child.sendline(PW)
    child.expect(pexpect.EOF, timeout=timeout)
    return child.exitstatus == 0

# Write HTML locally, upload, publish
with open('/tmp/blog-content-slug.html', 'w') as f:
    f.write('<article>...</article>')
scp_upload('/tmp/blog-content-slug.html', '/home/dh_mwpxuu/mifeco.com/tmp/slug.html')
scp_upload('/tmp/blog-image.png', '/home/dh_mwpxuu/mifeco.com/images/slug.png')
result = ssh_run('cd /home/dh_mwpxuu/mifeco.com && php scripts/wp-publish-post.php '
    '--title="Title" --content-file=.../tmp/slug.html --slug=slug '
    '--category="Books" --tags="tag1,tag2" --featured-image=.../images/slug.png')
data = json.loads(result.strip())
```

## Pitfalls

| Pitfall | Why | Fix |
|---------|-----|-----|
| SCP fails silently | Remote dir doesn't exist | `mkdir -p` first |
| `wp_create_category()` undefined | Missing taxonomy.php | Include it in PHP script |
| HTML mangled | Shell escaping | Use `--content-file` not inline |
| SSH hangs | Key auth delay | `-o PubkeyAuthentication=no` |
