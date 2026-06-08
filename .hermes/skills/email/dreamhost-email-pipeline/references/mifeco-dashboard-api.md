# MIFECO Dashboard API & Email Configuration Reference

## Dashboard Data API

The dashboard at `https://www.mifeco.com/admin/` uses a PHP API for all dynamic data.

### API Endpoint
- **Base**: `https://www.mifeco.com/admin/api.php`
- **Health**: `GET /admin/api.php?action=health`
- **Get all**: `GET /admin/api.php?action=get&resource=all`
- **Get specific**: `GET /admin/api.php?action=get&resource=RESOURCE`
- **Update**: `POST /admin/api.php` with `{"secret":"M1f3c0_W3bh00k_2026!","action":"update","resource":"NAME","data":{...}}`
- **Sync**: `POST /admin/api.php` with `{"secret":"M1f3c0_W3bh00k_2026!","action":"sync","pipeline_state":{...},...}`

### Available Resources
| Resource | File | Description |
|----------|------|-------------|
| pipeline-state | /admin/pipeline-state.json | Pipeline status, 9 pipelines, contentSummary |
| pipeline-books | /admin/pipeline-books.json | Books catalog (5 No Blue Sky + moon_books + standalone) |
| pipeline-saas | /admin/pipeline-saas.json | SaaS apps (3 products) |
| pipeline-consulting | /admin/pipeline-consulting.json | Consulting tiers (2 products) |
| leads | /admin/leads-registry.json | Lead registry (18 leads across 3 pipelines) |
| unified | /admin/unified-pipeline.json | Unified lead array (10 leads with enrichment) |
| promotion | /admin/data/promotion-status.json | Promotion engine statuses |
| saas-nurture | /admin/sequences/saas-nurture.json | SaaS nurture sequence |
| books-nurture | /admin/sequences/books-nurture.json | Books nurture sequence |
| consulting-nurture | /admin/sequences/consulting-nurture.json | Consulting nurture sequence |
| nurture-sequences | /admin/sequences/nurture-sequences.json | All sequences combined |
| social-content | /admin/data/social-content-books.json | Social media content |

### Webhook Endpoint
- **Health**: `GET /admin/webhook.php` — returns data file inventory
- **Sync**: `POST /admin/webhook.php` with `{"secret":"M1f3c0_W3bh00k_2026!","action":"sync",...}`
- **Update**: `POST /admin/webhook.php` with `{"secret":"M1f3c0_W3bh00k_2026!","action":"update","resource":"NAME","data":{...}}`

### Data File Locations
```
/home/dh_mwpxuu/mifeco.com/admin/
  api.php                          # REST API endpoint
  webhook.php                      # Webhook for Hermes agent sync
  pipeline-state.json              # Main pipeline state (9 pipelines)
  pipeline-books.json              # Books catalog
  pipeline-saas.json               # SaaS apps
  pipeline-consulting.json         # Consulting tiers
  unified-pipeline.json            # Unified leads array
  leads-registry.json              # Lead registry by pipeline
  pipeline-dashboard.html          # Main dashboard (dynamic JS)
  content-command-center.html      # Content management
  hermes-dashboard.html            # Hermes agent info
  outreach-dashboard.html          # Outreach engine
  index.php                        # Password gate + menu
  data/
    promotion-status.json          # Promotion engine status
  sequences/
    nurture-sequences.json         # All nurture sequences
    saas-nurture.json              # SaaS sequence
    books-nurture.json             # Books sequence
    consulting-nurture.json        # Consulting sequence
  flows/                           # SVG flow diagrams (9 files)
  forms/                           # Intake form HTML (3 files)
```

## Email Configuration

### WordPress REST API (via nginx)
All email endpoints use `/index.php?rest_route=` (NOT `/wp-json/`):

| Endpoint | Method | URL |
|----------|--------|-----|
| Send email | POST | `/index.php?rest_route=/mifeco/v1/send-email` |
| Unsubscribe | POST | `/index.php?rest_route=/mifeco/v1/unsubscribe` |
| Suppress check | POST | `/index.php?rest_route=/mifeco/v1/suppress` |

### Authentication
Parameter: `secret=JY2pcWpfu1*JeubsVBpm`

⚠️ **Do NOT use the old secret `Rm2214ri%%%%`** — it was replaced. Check all files for hardcoded old secrets:
```bash
grep -rn 'Rm2214ri%%%%' /home/dh_mwpxuu/mifeco.com/wp-content/plugins/
grep -rn 'rmills@mifeco.com' /home/dh_mwpxuu/mifeco.com/wp-content/plugins/
grep -rn 'rmills@mifeco.com' /home/dh_mwpxuu/mifeco.com/admin/
```

### Suppression List
- File: `/home/dh_mwpxuu/mifeco.com/wp-content/mifeco-suppression-list.txt`
- One email per line, lowercase
- Checked before every send (403 response if suppressed)

### Plugin Locations
| Plugin | Path |
|--------|------|
| MIFECO Mailer | `wp-content/plugins/mifeco-mailer/mifeco-mailer.php` (v1.2.0) |
| MIFECO Admin Proxy | `wp-content/plugins/mifeco-admin-proxy/mifeco-admin-proxy.php` (v1.0.0) |
| MIFECO Pipeline Setup | `wp-content/plugins/mifeco-pipeline-setup/mifeco-pipeline-setup.php` |
| MIFECO Outreach | `wp-content/plugins/mifeco-outreach/mifeco-outreach-admin.php` |
| WP Mail SMTP | `wp-content/plugins/wp-mail-smtp/wp_mail_smtp.php` |

### WP Mail SMTP Settings
| Setting | Value |
|---------|-------|
| From Email | MIFECOinc@gmail.com |
| From Name | MIFECO |
| Mailer | Other SMTP |
| SMTP Host | smtp.gmail.com |
| SMTP Port | 587 |
| Encryption | STARTTLS |
| Auth | ON |
| User | MIFECOinc@gmail.com |
| Pass | Rm2214ri# |

## SSH Access Pattern (Paramiko)

```python
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('IAD1-SHARED-B8-42.DREAMHOST.COM', username='dh_mwpxuu', password=pw, timeout=15)

stdin, stdout, stderr = client.exec_command("cd /home/dh_mwpxuu/mifeco.com && [cmd]", timeout=15)
out = stdout.read().decode('utf-8', errors='replace')

sftp = client.open_sftp()
sftp.get(remote, local)  # download
sftp.put(local, remote)  # upload
sftp.close()
client.close()
```

**Never use `--delete`** with rsync to the web root — the SPA and WordPress coexist.
**Never use `.htaccess`** — nginx ignores it completely.
**Always use absolute paths** in PHP scripts on DreamHost (`__DIR__`, `WP_CONTENT_DIR`).
