---
name: php-admin-dashboard-deployment
title: PHP Admin Dashboard Deployment on Shared Hosting
description: Deploy static HTML dashboards behind a PHP session-based password gate on shared hosting (co-located with WordPress), with a PHP webhook endpoint for agent-triggered data refresh.
tags: [deployment, dashboard, php, password-gate, webhook, shared-hosting, dreamhost, wordpress]
related_skills:
  - devops/wordpress-pipeline-integration
  - devops/webhook-subscriptions
  - business/sales-pipeline-infrastructure
triggers:
  - "User has static HTML dashboards with embedded JSON data and wants them live on a shared hosting site"
  - "User wants a password-protected admin area on their WordPress site that's separate from wp-admin"
  - "Deploy pipeline dashboards, content command centers, or admin panels to a shared hosting server"
  - "Create a PHP webhook endpoint on shared hosting that an agent or external service can POST data to"
  - "Set up recurring rsync-based sync from an agent machine to a shared hosting server for dashboard updates"
  - "User has WordPress on DreamHost (or similar) and needs admin dashboards deployed alongside it"
  - "Protect static HTML files with a single-password session-based PHP gate"
  - "Build a content dashboard with view/approve/send/delete buttons and 3-state approval workflow"
  - "User wants to replace alert()-based placeholder links with live interactive modals (intake forms, email sequences, architecture docs)"
  - "User wants visual infographic metrics sections on content cards (X posts, blog posts, LinkedIn posts)"
  - "User wants to correct book titles or add missing books to a pipeline dashboard catalog"
  - "User wants sidebar navigation cleanup — removing duplicate alert-based links"
  - "Deploy static HTML forms, JSON sequence files, and markdown docs to the server alongside dashboards"
  - "User asks for pipeline status/queue display per pipeline stage — add a pipeline status modal with stage-by-stage counters"
  - "User wants SaaS apps to show as open-source downloads with a Pro waitlist option and download/waitlist counters"
  - "User wants a human-action task checklist on the dashboard — track blocked/pending/done tasks with action links"
  - "User wants a waitlist/mailing-list signup modal that sends to AgentMail using +addressing"
  - "User wants pipeline-level progress summary with stage counts, queue depth, and completed-this-month stats"
  - "User wants to deploy a new section (e.g. books, storefront) to a DreamHost shared hosting site alongside WordPress"
---


## Memory context (Hindsight)

Long-term memory context is now provided automatically by Hindsight (bank
`mifeco-default`) on every turn — the retired MemPalace manual query step no
longer applies. Do NOT attempt to import `~/.hermes/mempalace` (it was removed
2026-08-19).This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# PHP Admin Dashboard Deployment on Shared Hosting

Deploy static HTML dashboards behind a PHP password gate on shared hosting, with a webhook endpoint for agent-triggered data refresh.

## Architecture

```
Agent Machine (Hermes)                 Shared Hosting (e.g., DreamHost)
┌──────────────────────┐               ┌──────────────────────────────┐
│ pipeline-engine/     │  rsync -avz   │ /home/user/domain.com/admin/ │
│   dashboard/         │ ───────────→  │   index.php     ← Password gate│
│   data/*.json        │               │   dashboard.html ← Live data │
│   scripts/           │               │   webhook.php   ← POST endpoint│
│     dashboard-sync.sh│               │   .htaccess     ← Security   │
└──────────────────────┘               └──────────────────────────────┘
        │                                       │
        │  Webhook POST (data refresh)          │
        └───────────────────────────────────────┘
```

## Key Components

### 1. PHP Password Gate (`index.php`)

A session-based single-password gate that protects all admin pages:

- PHP sessions with configurable timeout (default 2 hours)
- Single password hardcoded in the file (one gate, not multi-user)
- On successful login: redirect to the specified dashboard HTML page
- Logout support
- Clean dark-themed login form matching the dashboard design
- Session cookie: HttpOnly + SameSite=Strict

**Password storage:** Hardcoded in the PHP file (single-user, single-password). Use a strong password — it's the only barrier between the public internet and your data.

**Session management:**
```php
session_start();
$ADMIN_PASSWORD = 'your-strong-password-here';
$SESSION_TIMEOUT = 7200; // 2 hours

// Check timeout on each request
if (time() - $_SESSION['login_time'] > $SESSION_TIMEOUT) {
    session_destroy();
    header('Location: ?expired=1');
    exit;
}
```

### 2. Static Dashboard HTML

The dashboards are self-contained HTML files with data embedded as JavaScript objects in `<script>` tags. No database, no server-side rendering. Data is embedded fresh on each sync.

**Data embed pattern:**
```html
<script>
// ===== LIVE PIPELINE DATA =====
const saasPipeline = { ... };  // From pipeline-saas.json
const consultingPipeline = { ... };
const booksPipeline = { ... };
</script>
```

### 3. PHP Webhook Endpoint (`webhook.php`)

A PHP endpoint that the agent can POST data to:

**Endpoints:**
| Method | Action | Description |
|--------|--------|-------------|
| GET | Health check | Returns `{"status": "ok", "timestamp": "..."}` |
| POST | `action: "ping"` | Ping test with secret validation |
| POST | `action: "refresh"` | Touch dashboard files to signal freshness |
| POST | `action: "sync"` | Write JSON data files to `data/` directory |

**Security:**
- Secret token in payload (not in URL or headers — avoids logging)
- 403 on invalid secret
- CORS headers for cross-origin access
- OPTIONS preflight support

**Pattern:**
```php
$SECRET = 'your-webhook-secret';
$input = json_decode(file_get_contents('php://input'), true);
if (!isset($input['secret']) || $input['secret'] !== $SECRET) {
    http_response_code(403);
    exit(json_encode(['status' => 'error', 'message' => 'Invalid secret']));
}
```

### 4. .htaccess Security

Protect the admin directory:
- Allow direct access to webhook.php (no session needed)
- Allow static assets (CSS, JS, images)
- Block direct access to `data/` directory
- Block direct PHP file access except index.php and webhook.php

### 5. Sync Script (rsync from agent to server)

A script on the agent machine that:
1. Reads the latest pipeline data from local JSON files
2. Rsyncs the dashboard directory to the server
3. Optionally triggers the webhook for data refresh

**⚠️ SSH/SFTP may be unavailable on DreamHost shared hosting.** Port 22 connection refused is a known limitation of shared hosting plans. When SSH is unavailable, use the DreamHost Panel File Manager (Monsta FTP) as fallback:
1. Zip the dashboard directory locally
2. Upload via panel file manager at `panel.dreamhost.com` → Users → SFTP Users & Files → File Manager
3. Extract on server

**Rsync with password (no sshpass, when SSH works):**

**Rsync with password (when SSH is available, e.g. VPS):**
```python
import pexpect
child = pexpect.spawn(f'rsync -avz --rsh="ssh -o StrictHostKeyChecking=accept-new" '
    f'{local_dir}/ {user}@{host}:{remote_dir}')
child.expect_exact("password:")
child.sendline(password)
child.expect(pexpect.EOF)
```

**⚠️ NEVER use `--delete` flag** when rsyncing to a directory co-located with WordPress. It will delete all WordPress files.

## File Structure on Server

```
/var/www/domain.com/admin/
├── index.php                       # Password gate → login or menu
├── pipeline-dashboard.html         # Dashboard with embedded data
├── content-command-center.html     # Content management dashboard
├── webhook.php                     # Webhook endpoint
├── .htaccess                       # Security rules
└── data/                           # Synced JSON data (webhook writes here)
    ├── pipeline-saas.json
    ├── pipeline-books.json
    └── ...
```

## Cron Schedule

| Time | Job | Action |
|------|-----|--------|
| Daily (30 min after pipeline run) | Dashboard Sync | rsync dashboard files + trigger webhook refresh |

## DOX Integration

When working in a project that uses the [DOX (Self-documenting AGENTS.md)](https://github.com/agent0ai/dox) framework:

- **Read Before Editing:** Walk the DOX tree from root to the target path. Read every AGENTS.md along the route before making any changes.
- **Update After Editing:** If the change affects purpose, scope, ownership, structure, workflows, or operating rules, update the closest owning AGENTS.md and refresh the Child DOX Index.
- **Reference:** [agent0ai/dox](https://github.com/agent0ai/dox) — copy `AGENTS.md` from the repo root into your project to initialize.

## Approval Workflow UI Pattern

For content dashboards (emails, social posts, blog drafts) where nothing should go live without explicit sign-off, implement this **3-state approval workflow**.

### State Management (localStorage)

```javascript
const LS_KEY = 'mifeco_content_center_v2';

function loadState() {
  try {
    const raw = localStorage.getItem(LS_KEY);
    return raw ? JSON.parse(raw) : { approved: {}, sent: {}, deleted: {} };
  } catch(e) { return { approved: {}, sent: {}, deleted: {} }; }
}

let state = loadState();

function isApproved(id) { return state.approved[id] === true; }
function isSent(id)     { return state.sent[id] === true; }
function isDeleted(id)  { return state.deleted[id] === true; }
function markApproved(id) { state.approved[id] = true; saveState(state); }
function markSent(id)     { state.sent[id] = true; saveState(state); }
function markDeleted(id)  { state.deleted[id] = true; saveState(state); }
```

### Three-State Flow

```
🟦 Pending → [View] [Approve] [Delete]
         ↓ (click Approve → confirm modal)
🟧 Approved → [View] [✔ Approved] [Send Now] [Delete]
         ↓ (click Send Now → confirm modal → webhook notification)
🟩 Sent → [View] [✓ Sent] (all actions disabled)
```

**State transitions:**
- **Pending:** Default. Item shows amber "Approve" button. "Send" button is hidden.
- **Approved:** After clicking Approve. Item gets an amber border + "✔ Approved" overlay. "Send Now" button appears.
- **Sent:** After clicking Send. Item gets a green border + "✓ Sent" overlay. All action buttons disabled.

### Card Button Pattern

Each card renders 3-4 buttons depending on state:

```javascript
function buildCardActions(viewer, id) {
  const approved = isApproved(id);
  const sent = isSent(id);

  // View — always visible
  let html = `<button onclick="openViewModal('${viewer}','${id}')">👁 View</button>`;

  if (sent) {
    html += `<button disabled>✓ Sent</button>`;
  } else if (approved) {
    html += `<button class="approved-done">✔ Approved</button>`;
    html += `<button onclick="confirmAction('${viewer}','${id}','send')">📤 Send Now</button>`;
    html += `<button onclick="confirmAction('${viewer}','${id}','delete')">🗑 Delete</button>`;
  } else {
    html += `<button onclick="confirmAction('${viewer}','${id}','approve')">✔ Approve</button>`;
    html += `<button onclick="confirmAction('${viewer}','${id}','delete')">🗑 Delete</button>`;
  }
  return html;
}
```

### View Modal

A full-content overlay that shows the complete item (subject, body, keywords, metadata) with inline actions:

- **Status badge:** Shows current state (⏳ Pending Approval / ✔ Approved / ✓ Sent) with color coding
- **Metadata row:** Type, pipeline, day, target type, book title, CTA — whatever is relevant
- **Body panel:** Full content with highlighted `{{placeholders}}` in accent color, monospace whitespace preservation (`white-space: pre-wrap`)
- **Keywords panel:** Flex-wrap list of tags below the body
- **Footer buttons:** Same approve/send/delete buttons as the card — closes the modal first, then opens the confirmation modal
- **Escape key** closes the view modal
- **Overlay click** closes the view modal
- **Responsive:** 720px max-width, scrollable on mobile

```javascript
function openViewModal(viewer, id) {
  const item = getItem(viewer, id);
  if (!item) return;

  // Populate header (subject/meta), status badge, body with highlighted placeholders,
  // keyword tags, and matching footer buttons
  document.getElementById('vmSubject').textContent = item.subject || item.title;
  document.getElementById('vmBody').innerHTML = highlightPlaceholders(item.body || item.copy);
}
```

### Confirmation Modal

A three-modal-style confirmation system (one reusable overlay, three configurations):

| Action | Title | Description | Confirm Button |
|--------|-------|-------------|----------------|
| **Approve** | "Approve this email?" | "You are approving this content for publication. Once approved, the Send button will become active. Nothing will be sent yet." | `✔ Approve` (amber) |
| **Send** | "Send this email now?" | "This content has been approved. Clicking Send will dispatch it via the webhook. This cannot be undone." | `📤 Send Now` (accent) |
| **Delete** | "Remove from queue?" | "This will permanently remove the item with a slide-out animation." | `🗑 Delete` (red) |

### Sidebar Stats

Include approved count alongside total/sent/queued:

```
Total Items: 38
Approved:    3   ← new amber-colored stat
Sent:        12
Queued:      23  ← remaining pending items
```

### Visual Styling

- **Approved cards:** Amber border (`#f59e0b`), amber overlay badge, amber background tint
- **Sent cards:** Green border (`#22c55e`), green overlay badge, green background tint
- **Pending cards:** Default dark card with amber "Approve" button
- **View modal:** Dark overlay (85% opacity), inner card with close button, status badges with color-coded backgrounds
- **Buttons:** View (purple outline), Approve (amber fill), Send (accent/fill), Delete (red outline)

### Webhook Notification on Send

When an item is sent, POST a fire-and-forget notification to the webhook endpoint:

```javascript
function notifyWebhook(viewer, id, action) {
  const item = getItem(viewer, id);
  if (!item) return;

  fetch('/admin/webhook.php', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      secret: 'your-webhook-secret',
      action: 'content_action',
      content: { viewer, item_id: id, action, timestamp: new Date().toISOString() }
    })
  }).catch(() => {}); // Fire-and-forget
}
```

### State Persistence Keying

Always version the localStorage key so old state doesn't collide with new schema:

```javascript
const LS_KEY = 'mifeco_content_center_v2'; // Increment on schema change
```

---

## Pipeline Dashboard Modals

When building a multi-section pipeline dashboard, replace `alert()`-based placeholder links with live interactive modals. The three common modal patterns are:

### 1. Intake Form Modal (iframe)

Opens a self-contained HTML form in an iframe within a modal overlay. The form submits directly to AgentMail via its own JavaScript — no additional backend needed.

**CSS:**
```css
.modal-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.8);z-index:300;align-items:center;justify-content:center;padding:20px}
.modal-overlay.show{display:flex}
.modal-content{background:#1e293b;border:1px solid #334155;border-radius:12px;max-width:800px;width:100%;max-height:85vh;overflow:hidden;display:flex;flex-direction:column;position:relative}
.modal-header{display:flex;align-items:center;justify-content:space-between;padding:16px 20px;border-bottom:1px solid #334155;flex-shrink:0}
.modal-header h3{font-size:16px;font-weight:700;color:#e2e8f0}
.modal-close-btn{background:transparent;border:1px solid #334155;color:#94a3b8;width:32px;height:32px;border-radius:6px;cursor:pointer;font-size:16px;display:flex;align-items:center;justify-content:center;transition:all .15s}
.modal-close-btn:hover{background:#ef4444;color:#fff;border-color:#ef4444}
.modal-body{flex:1;overflow-y:auto;padding:20px}
.modal-body iframe{width:100%;height:100%;border:none;min-height:60vh;border-radius:8px;background:#0f172a}
```

**HTML:**
```html
<!-- Form Modal -->
<div class="modal-overlay" id="formModal">
  <div class="modal-content">
    <div class="modal-header">
      <h3 id="formModalTitle">Intake Form</h3>
      <button class="modal-close-btn" onclick="closeModals()">✕</button>
    </div>
    <div class="modal-body">
      <iframe id="formIframe" src="about:blank"></iframe>
    </div>
  </div>
</div>
```

**JavaScript:**
```javascript
function closeModals() {
  ['formModal','sequenceModal','archModal'].forEach(id => {
    document.getElementById(id).classList.remove('show');
  });
}
// Close on overlay click
document.querySelectorAll('.modal-overlay').forEach(el => {
  el.addEventListener('click', function(e) {
    if (e.target === this) closeModals();
  });
});
// ESC key closes all modals
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') closeModals();
});

function openFormModal(type) {
  const labels = {saas:'SaaS Intake Form',consulting:'Consulting Intake Form',books:'Books Inquiry Form'};
  const urls = {saas:'/admin/forms/saas-intake.html',consulting:'/admin/forms/consulting-intake.html',books:'/admin/forms/books-intake.html'};
  document.getElementById('formModalTitle').textContent = labels[type];
  document.getElementById('formIframe').src = urls[type];
  document.getElementById('formModal').classList.add('show');
}
```

**Usage in HTML:**
```html
<a href="#" onclick="openFormModal('saas')" class="btn btn-primary">📝 Open Intake Form</a>
```

**Server file structure:** The form HTML files live in `/admin/forms/{product}-intake.html` on the server. Deploy them alongside the dashboard.

### 2. Email Sequence Modal (JSON fetch → styled cards)

Fetches a nurture sequence JSON file from the server and renders each email as a stylized card showing day, subject, body preview, and CTA.

**CSS (add after form modal CSS):**
```css
.sequence-card{background:#0f172a;border:1px solid #334155;border-radius:8px;padding:14px;margin-bottom:12px}
.sequence-card h4{font-size:13px;font-weight:600;color:#00ffcc;margin-bottom:4px}
.sequence-card .seq-day{font-size:11px;color:#667eea;font-weight:600;margin-bottom:2px}
.sequence-card .seq-subject{font-size:13px;color:#e2e8f0;margin-bottom:6px}
.sequence-card .seq-preview{font-size:12px;color:#94a3b8;line-height:1.5;max-height:60px;overflow:hidden}
.sequence-card .seq-cta{font-size:11px;color:#f59e0b;margin-top:6px}
```

**HTML:**
```html
<!-- Sequence Modal -->
<div class="modal-overlay" id="sequenceModal">
  <div class="modal-content">
    <div class="modal-header">
      <h3 id="sequenceModalTitle">Email Sequence</h3>
      <button class="modal-close-btn" onclick="closeModals()">✕</button>
    </div>
    <div class="modal-body" id="sequenceModalBody"></div>
  </div>
</div>
```

**JavaScript:**
```javascript
function openSequenceModal(type) {
  const labels = {saas:'SaaS Nurture (7 emails)',consulting:'Consulting Nurture (5 emails)',books:'Books Nurture (4 emails)'};
  const urls = {saas:'/admin/sequences/saas-nurture.json',consulting:'/admin/sequences/consulting-nurture.json',books:'/admin/sequences/books-nurture.json'};
  document.getElementById('sequenceModalTitle').textContent = labels[type];
  const body = document.getElementById('sequenceModalBody');
  body.innerHTML = '<div style="text-align:center;padding:40px;color:#94a3b8">⏳ Loading...</div>';
  document.getElementById('sequenceModal').classList.add('show');

  fetch(urls[type])
    .then(r => r.json())
    .then(data => {
      const emails = data.emails || data.email_sequences || [];
      if (emails.length === 0) {
        body.innerHTML = '<div style="text-align:center;padding:40px;color:#94a3b8">No emails found</div>';
        return;
      }
      body.innerHTML = emails.map(e =>
        `<div class="sequence-card">
          <div class="seq-day">Day ${e.day || '—'}</div>
          <h4>${escapeHtml(e.subject || e.subject_line || '(No subject)')}</h4>
          <div class="seq-preview">${escapeHtml((e.body || e.body_template || '').slice(0,200))}...</div>
          ${e.cta ? `<div class="seq-cta">📌 ${escapeHtml(e.cta)}</div>` : ''}
        </div>`
      ).join('');
    })
    .catch(err => {
      body.innerHTML = `<div style="text-align:center;padding:40px;color:#ef4444">❌ ${err.message}</div>`;
    });
}
```

**JSON sequence file structure (`/admin/sequences/{product}-nurture.json`):**
```json
{
  "pipeline": "SaaS",
  "email_sequences": [
    {
      "day": 1,
      "subject": "Welcome to MIFECO!",
      "body": "Hi {{name}},\n\nThanks for your interest...",
      "cta": "Schedule your demo"
    }
  ]
}
```

The function handles both `emails` and `email_sequences` array key conventions.

### 4. Pipeline Status Modal (stage-by-stage queue)

When a consulting or services tier needs to show its current queue and pipeline stage breakdown, add a **pipeline status modal** that renders stages with item counts, status dots, and summary stats.

**Data structure:**
```javascript
const pipelineQueueData = {
  'consulting-full': {
    title: '📊 Full Transformation Pipeline',
    stages: [
      { name: 'Lead Intake', count: 10, status: 'active', desc: 'New inquiries via website forms' },
      { name: 'Discovery Call', count: 6, status: 'active', desc: 'Needs assessment scheduled' },
      { name: 'Strategy Session', count: 2, status: 'active', desc: '1-on-1 booked' },
      { name: 'Full Transformation', count: 0, status: 'waiting', desc: 'No clients at this tier yet' }
    ],
    totalLeads: 10,
    activeInPipeline: 6,
    completedThisMonth: 3
  }
};
```

**JavaScript render function pattern:**
```javascript
function openPipelineStatusModal(tierKey) {
  const data = pipelineQueueData[tierKey];
  const modal = document.getElementById('pipelineStatusModal');
  const body = document.getElementById('psModalBody');

  // Summary stats grid (3 columns: Total, Active, Completed)
  body.innerHTML = `
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:20px;">
      <div style="background:#0f172a;border:1px solid #334155;border-radius:8px;padding:14px;text-align:center;">
        <div style="font-size:24px;font-weight:800;color:var(--accent);">${data.totalLeads}</div>
        <div style="font-size:10px;color:var(--text-secondary);text-transform:uppercase;">Total Leads</div>
      </div>
      <!-- repeat for activeInPipeline and completedThisMonth -->
    </div>
    <!-- Stage list -->
    ${data.stages.map(s => `
      <div style="display:flex;align-items:center;gap:14px;padding:12px;background:#0f172a;border-radius:8px;border:1px solid #334155;margin-bottom:8px;">
        <div style="width:36px;height:36px;border-radius:50%;background:${dotColor}22;display:flex;align-items:center;justify-content:center;">
          <span style="font-size:16px;font-weight:700;color:${dotColor};">${s.count}</span>
        </div>
        <div style="flex:1;">
          <div style="font-size:13px;font-weight:600;">${s.name}</div>
          <div style="font-size:11px;color:var(--text-secondary);">${s.desc}</div>
        </div>
        <span style="width:10px;height:10px;border-radius:50%;background:${dotColor};${glow}"></span>
      </div>
    `).join('')}
  `;
  modal.classList.add('show');
}
```

**Button pattern to trigger:**
```html
<button class="btn btn-primary" onclick="openPipelineStatusModal('consulting-full')">
  📊 View Pipeline Status & Queue
</button>
```

Color coding for stage status: `active` → green dot, `done` → accent dot, `waiting` → muted dot.

### 5. Waitlist / Signup Modal via AgentMail

When offering a Pro version waitlist or mailing-list signup, use an **email-based waitlist modal** that instructions the user to email AgentMail:

```javascript
function openWaitlistModal(productName) {
  document.getElementById('wlProductName').textContent = productName + ' Pro';
  document.getElementById('waitlistModal').classList.add('show');
}
```

**Modal content pattern:**
```html
<div class="modal-content" style="max-width:500px">
  <div class="modal-header"><h3>⭐ Join Pro Waitlist</h3><button class="modal-close-btn" onclick="closeWaitlistModal()">✕</button></div>
  <div class="modal-body">
    <div style="text-align:center;padding:20px;">
      <p style="color:var(--text-secondary);font-size:13px;margin-bottom:16px;">
        Be first in line when the <strong id="wlProductName">Pro version</strong> launches.
      </p>
      <div style="background:#0f172a;border:1px solid #334155;border-radius:8px;padding:16px;text-align:left;margin-bottom:16px;">
        <p style="font-size:12px;color:var(--text-secondary);margin-bottom:8px;">To join the waitlist, send an email to:</p>
        <code style="display:block;background:#1e293b;padding:10px;border-radius:6px;font-size:14px;color:var(--accent);text-align:center;">
          waitlist+{agentmail-inbox}@agentmail.to
        </code>
      </div>
      <p style="font-size:11px;color:var(--text-secondary);">
        Subject: "Pro Waitlist — [Product Name]"<br>
        Include your name, company, and use case.
      </p>
      <a href="mailto:..." class="btn btn-primary" style="margin-top:16px;">📧 Send Email to Join</a>
    </div>
  </div>
</div>
```

**Key concept:** The `+` addressing suffix on AgentMail inboxes (e.g., `waitlist+inboxname@agentmail.to`) allows the agent to auto-classify incoming waitlist signups. The dashboard's cron pipeline reads these emails, counts them, and updates the waitlistSignups counter.

---

## Stripe Express Checkout Element (On-Page Payment)

When building a gated PHP app that requires payment, add a backdoor login for testing that bypasses payment:

### In `register.php` (login handler):

```php
// Backdoor check — BEFORE normal auth
define('BACKDOOR_EMAIL', 'test@example.com');
define('BACKDOOR_PASSWORD_HASH', password_hash('SecureP@ssw0#', PASSWORD_DEFAULT));

if ($_POST['email'] === BACKDOOR_EMAIL && 
    password_verify($_POST['password'], BACKDOOR_PASSWORD_HASH)) {
    // Auto-create account if doesn't exist
    $stmt = $db->prepare('SELECT id FROM users WHERE email = ?');
    $stmt->execute([BACKDOOR_EMAIL]);
    if (!$stmt->fetch()) {
        $stmt = $db->prepare('INSERT INTO users (email, name, password_hash, created_at) VALUES (?, ?, ?, NOW())');
        $stmt->execute([BACKDOOR_EMAIL, 'Test User', BACKDOOR_PASSWORD_HASH]);
    }
    // Set session
    $_SESSION['user_id'] = $db->lastInsertId();
    $_SESSION['user_name'] = 'Test User';
    $_SESSION['backdoor'] = true;  // Flag for payment bypass
    redirect('/pay.php');
}
```

### In `pay.php`:

```php
// Backdoor bypass — skip payment
if (!empty($_SESSION['backdoor'])) {
    redirect('/survey.php');
}
```

### Security Notes

- Store the backdoor password hash with `password_hash()`, never plaintext
- The backdoor should only work for a specific hardcoded email
- Add a comment in the code: `// BACKDOOR — remove before production`
- The `$_SESSION['backdoor']` flag should be checked on every gated page (survey, download, etc.)

### Dynamic API Pattern for Dashboards (2026-05)

When the dashboard needs to track tasks requiring manual human intervention (API keys, domain verification, manuscript fixes, pricing setup), add a **human action checklist**:

```javascript
const humanActionItems = [
  {
    id: 'stripe-keys',
    title: '🔑 Configure Stripe Payment Links',
    desc: 'Replace placeholder Stripe link IDs with live payment links.',
    status: 'blocked',          // 'blocked' | 'pending' | 'done'
    actionUrl: '/wp-admin/plugins/editor/',
    actionLabel: 'Open Editor'
  }
];
```

**Render pattern — stats bar + items:**
```javascript
function renderHumanActionChecklist() {
  const blocked = humanActionItems.filter(i => i.status === 'blocked').length;
  const pending = humanActionItems.filter(i => i.status === 'pending').length;
  const done = humanActionItems.filter(i => i.status === 'done').length;

  container.innerHTML = `
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:16px;">
      <div style="background:#ef444422;border:1px solid #ef444455;border-radius:8px;padding:10px;text-align:center;">
        <div style="font-size:20px;font-weight:800;color:var(--danger);">${blocked}</div>
        <div style="font-size:10px;color:var(--danger);text-transform:uppercase;">Blocked (Keys Needed)</div>
      </div>
      <!-- repeat for Pending and Completed with appropriate colors -->
    </div>
    ${humanActionItems.map(item => `<div style="display:flex;align-items:center;gap:12px;padding:12px;background:#0f172a;border-radius:8px;border:1px solid #334155;">
      <div style="flex:1;">
        <div style="font-size:13px;font-weight:600;">${item.title}</div>
        <div style="font-size:11px;color:var(--text-secondary);">${item.desc}</div>
      </div>
      <div>
        <span style="font-size:10px;font-weight:600;color:${statusColor};">${statusLabel}</span>
        <a href="${item.actionUrl}" class="btn btn-outline" style="padding:3px 8px;font-size:9px;">${item.actionLabel}</a>
      </div>
    </div>`).join('')}
  `;
}
```

**Status categories:**
- `blocked` (red) — requires API key, domain ownership, or external credential the user must manually set up
- `pending` (amber) — manuscript fix, promotion launch, pricing decision — needs human action but is not blocked by credentials
- `done` (green/dimmed) — completed, rendered with reduced opacity

**Placement:** Add to sidebar as "✅ Human Actions" and to the page body as a dedicated section before the footer, with a "View Full Checklist" button that opens the full modal.

### 7. SaaS Open-Source + Pro Waitlist Card Pattern

When a dashboard section needs to show SaaS apps as **free open-source downloads + paid Pro waitlist**, use this card pattern:

```javascript
// Data model — each SaaS app gets download/waitlist counters
const saasApps = [
  {
    name: 'Project Hypatia Pro',
    ghName: 'HypatiaPro',
    github: 'https://github.com/user/repo.git',
    prodUrl: 'https://app.example.com',
    openSourceUrl: 'https://github.com/user/repo/releases',
    downloads: 47,
    waitlistSignups: 12,
    waitlistOpen: true
  }
];

// Render — insert open-source block below links but above status
function renderSaaS() {
  grid.innerHTML = saasApps.map(a => {
    let osHtml = '';
    if (!a.isWebsite) {
      osHtml = `
        <div style="margin-top:12px;padding:10px;background:#0f172a;border-radius:8px;border:1px solid #334155;">
          <div style="display:flex;gap:12px;align-items:center;margin-bottom:8px;">
            <span style="font-size:11px;color:var(--accent);">⬇ Open Source (Free)</span>
            <span style="font-size:11px;color:var(--warning);">⭐ Pro (Waitlist)</span>
          </div>
          <div style="display:flex;gap:8px;margin-bottom:8px;">
            <a href="${a.openSourceUrl}" target="_blank" class="btn btn-primary" style="padding:5px 12px;font-size:10px;">⬇ Free Download</a>
            <button class="btn btn-outline" style="padding:5px 12px;font-size:10px;" onclick="openWaitlistModal('${a.name}')">⭐ Join Pro Waitlist</button>
          </div>
          <div style="display:flex;gap:16px;font-size:10px;color:var(--text-secondary);">
            <span>📥 <strong style="color:var(--success)">${a.downloads}</strong> downloads</span>
            <span>📋 <strong style="color:var(--warning)">${a.waitlistSignups}</strong> waitlist signups</span>
          </div>
        </div>`;
    }
    return `<div class="saas-card">...${osHtml}...</div>`;
  }).join('');
}
```

**Counters:** Download counts come from parsing the GitHub release page or a local counter file. Waitlist signups come from the AgentMail `waitlist+inbox` email address — the agent's daily cron reads the inbox, counts new signup emails, and updates the JSON data before dashboard sync.

### 8. Architecture Modal (fetch markdown → rendered)

Fetches an ARCHITECTURE.md from the server and renders it with basic markdown-to-HTML conversion. Good for displaying system design docs inline.

**CSS:**
```css
.arch-content{font-size:13px;color:#e2e8f0;line-height:1.7}
.arch-content h2{font-size:18px;color:#00ffcc;margin-top:20px;margin-bottom:10px;border-bottom:1px solid #334155;padding-bottom:6px}
.arch-content h3{font-size:15px;color:#667eea;margin-top:16px;margin-bottom:8px}
.arch-content code{background:#0f172a;padding:1px 5px;border-radius:3px;font-size:12px;color:#f59e0b}
.arch-content pre{background:#0f172a;border:1px solid #334155;border-radius:8px;padding:14px;overflow-x:auto;margin:10px 0;font-size:12px;color:#e2e8f0}
.arch-content table{border-collapse:collapse;width:100%;margin:10px 0;font-size:12px}
.arch-content td,.arch-content th{border:1px solid #334155;padding:6px 10px;text-align:left}
.arch-content th{background:#0f172a;color:#00ffcc;font-weight:600}
.arch-content a{color:#667eea}
```

**HTML:**
```html
<!-- Architecture Modal -->
<div class="modal-overlay" id="archModal">
  <div class="modal-content" style="max-width:900px">
    <div class="modal-header">
      <h3>📐 Architecture</h3>
      <button class="modal-close-btn" onclick="closeModals()">✕</button>
    </div>
    <div class="modal-body" id="archModalBody"></div>
  </div>
</div>
```

**JavaScript:**
```javascript
function openArchitectureModal() {
  const body = document.getElementById('archModalBody');
  body.innerHTML = '<div style="text-align:center;padding:40px;color:#94a3b8">⏳ Loading...</div>';
  document.getElementById('archModal').classList.add('show');
  fetch('/admin/ARCHITECTURE.md')
    .then(r => r.text())
    .then(md => {
      let html = md
        .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
        .replace(/^### (.+)$/gm, '<h3>$1</h3>')
        .replace(/^## (.+)$/gm, '<h2>$1</h2>')
        .replace(/^# (.+)$/gm, '<h1 style="font-size:20px;color:#00ffcc">$1</h1>')
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.+?)\*/g, '<em>$1</em>')
        .replace(/\[(.+?)\]\((.+?)\)/g, '<a href="$2" target="_blank">$1</a>');
      body.innerHTML = '<div class="arch-content">' + html + '</div>';
    })
    .catch(err => {
      body.innerHTML = `<div style="text-align:center;padding:40px;color:#ef4444">❌ ${err.message}</div>`;
    });
}
```

The markdown converter handles: code blocks, headings (h1-h3), bold, italic, links, tables (basic), lists, and horizontal rules. For a full markdown renderer, consider adding `marked.js` via CDN, but the inline converter keeps zero dependencies.

---

## Infographic Sections on Content Cards

For content command center dashboards, add compact infographic metric sections to content cards. These provide at-a-glance performance estimates and visual progress bars.

### Pattern

Insert a styled `<div>` block before the `.actions` div in each render function:

```html
<div style="margin:8px 0 10px;padding:8px 10px;background:rgba(0,255,204,.04);border-radius:6px;border:1px solid rgba(0,255,204,.08)">
  <div style="display:flex;gap:12px;font-size:10px;flex-wrap:wrap">
    <span style="color:#94a3b8">📈 <strong style="color:#00ffcc">2.4K</strong> est. impressions</span>
    <span style="color:#94a3b8">💬 <strong style="color:#667eea">85</strong> engagements</span>
    <span style="color:#94a3b8">⏰ Best: <strong style="color:#f59e0b">8-10am EST</strong></span>
  </div>
  <div style="margin-top:4px;height:4px;background:#334155;border-radius:2px;overflow:hidden">
    <div style="height:100%;width:68%;background:linear-gradient(90deg,#00ffcc,#667eea);border-radius:2px"></div>
  </div>
</div>
```

### Per-Content-Type Template

**X Posts:** Impressions (2.4K), Engagements (85), Best time (8-10am EST), gradient bar
**Blog Posts:** Dynamic read time (`Math.max(1, Math.round(item.body.split(/\s+/).length / 200))` min), difficulty badge (Beginner/Intermediate/Advanced based on word count), topic from first keyword, multi-color bar
**LinkedIn Posts:** Reach (3.1K), Reactions (124), Comments (18), Content type tag, gradient bar

For blog posts, calculate dynamically:
```javascript
const wordCount = item.body.split(/\s+/).length;
const readTime = Math.max(1, Math.round(wordCount / 200));
const difficulty = wordCount > 500 ? 'Advanced' : wordCount > 200 ? 'Intermediate' : 'Beginner';
```

---

## Book Catalog Maintenance

When a pipeline dashboard has an embedded book catalog that needs updating:

### Correcting Wrong Titles

1. Find the `books:` array in the pipeline data JS object (e.g., `booksPipeline.books`)
2. Replace each wrong title string with the correct one
3. Update prices if needed
4. Validate JSON integrity with `python3 -c "import json; json.load(open('file.html'))" - not applicable for embedded JS — just visually verify the array syntax

### Adding Missing Books

Append new entries to the array:

```javascript
books: [
  { title:'No Blue Sky: Built from Dust',            price:9.99 },
  { title:'No Blue Sky: The Oxygen Gamble',          price:11.99 },
  // ... existing books ...
  { title:'AI That Works for Small Business',        price:19.99 },   // 🆕
  { title:'No Blue Sky Box Set (all 5 vols)',        price:49.99 },   // 🆕
  { title:'The MIFECO AI Playbook',                  price:9.99 }     // 🆕
]
```

---

## Sidebar Navigation Cleanup

When a pipeline dashboard has duplicate sidebar links (one set that scrolls to sections, another set that shows alerts), consolidate to a single clean nav:

**Before (problematic):**
```html
<nav class="sidebar-nav">
  <a href="#intake-forms">📝 Intake Forms</a>
  <a href="#email-sequences">✉️ Email Sequences</a>
</nav>
<!-- ... later in sidebar-footer ... -->
<nav class="sidebar-footer">
  <a href="#" onclick="alert('Forms available locally')">📝 Intake Forms</a>  ← DUPLICATE
  <a href="#" onclick="alert('Sequences available locally')">✉️ Email Sequences</a>  ← DUPLICATE
</nav>
```

**After (clean):**
```html
<nav class="sidebar-nav">
  <a href="#overview">📊 Overview</a>
  <a href="#saas">☁️ SaaS Pipeline</a>
  <a href="#consulting">💼 Consulting Pipeline</a>
  <a href="#books">📚 Books Pipeline</a>
  <a href="#intake-forms">📝 Intake Forms</a>       ← scrolls to section
  <a href="#email-sequences">✉️ Email Sequences</a>   ← scrolls to section
  <hr><!-- separator -->
  <a href="content-command-center.html">📊 Content Command Center</a>
  <a href="#" onclick="openArchitectureModal()">📐 View Architecture</a>
</nav>
<nav class="sidebar-footer">
  <a href="?logout=1">🚪 Logout</a>
</nav>
```

**Rules:**
- Scroll-to-section links (`href="#section"`) go in `sidebar-nav`
- External dashboard links (Hermes Dashboard, Content Command Center) also go in `sidebar-nav` — NOT in `sidebar-footer` — so they appear in the mobile hamburger menu
- Only Logout stays in `sidebar-footer` (it's small and fits)
- Never have two links pointing to the same function on the same page
- Replace all `onclick="alert(...)` with either modals or proper href navigation

## Mobile Responsive Sidebar

When a dashboard uses a hamburger menu on mobile (sidebar slides in from the left), anything in `.sidebar-footer` is typically **below the scroll fold** — users don't know to scroll down in the sidebar. This means:

- **Links in `.sidebar-footer` are invisible on mobile** even when the hamburger menu opens
- **Fix:** Promote external dashboard links (🤖 Hermes Dashboard, 📊 Content Command Center) into the main `.sidebar-nav` above the footer, separated by a `<hr>` line
- **Good pattern:**
  ```html
  <nav class="sidebar-nav">
    <a href="#overview">📊 Overview</a>
    <a href="#saas">☁️ SaaS Pipeline</a>
    <!-- ... main nav links ... -->
    <hr style="border:none;border-top:1px solid #334155;margin:8px 20px;">
    <a href="hermes-dashboard.html" onclick="closeSidebar()">🤖 Hermes Dashboard</a>
    <a href="content-command-center.html" onclick="closeSidebar()">📊 Content Command Center</a>
  </nav>
  <div class="sidebar-footer">
    <a href="?logout=1">🚪 Logout</a>
  </div>
  ```
- **Always add `onclick="closeSidebar()"`** to each nav link so mobile hamburger autocloses on tap
- Verify on real mobile: open the hamburger, check all links are visible without scrolling
- The sidebar must have `overflow-y: auto` (already present) so the full content is scrollable if needed

---

## SFTP Deployment via Python paramiko

When `sshpass` or `pexpect` isn't available, use Python's `paramiko` library for password-based SFTP deployment:

```python
import paramiko
import os

host = "your-host.com"
user = "your-username"
password = "your-password"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=user, password=password, look_for_keys=False)
sftp = ssh.open_sftp()

# Upload a file
local_path = "/local/path/to/file.html"
remote_path = "/remote/path/to/file.html"
sftp.put(local_path, remote_path)

# Upload multiple files
files = ["pipeline-dashboard.html", "content-command-center.html", "index.php"]
for f in files:
    sftp.put(os.path.join(local_dir, f), os.path.join(remote_dir, f))

# Create remote directories
for d in ["/forms", "/sequences"]:
    try:
        sftp.stat(remote_dir + d)
    except:
        sftp.mkdir(remote_dir + d)

sftp.close()
ssh.close()
```

**Usage pattern:** Wrap in `execute_code` or run via `terminal()` with `python3 -c`.

**Fallback when paramiko isn't installed:**
```bash
pip3 install paramiko
```

## Pitfalls

| Pitfall | Why | How to Avoid |
|---------|-----|--------------|
| **SSH unavailable on shared hosting** | DreamHost shared plans do NOT provide SSH shell access. Port 22 SSH is refused. **BUT SFTP works on port 22** with password `Rm2214ri####`. Use `paramiko.Transport((host, 22))` + `SFTPClient`. See `references/dreamhost-deployment.md` for full code. | Use paramiko SFTP for automated deployment. Fall back to Panel File Manager for one-off uploads. FTP (port 21) connects but panel password ≠ FTP password — create separate FTP user if needed. |
| **Dashboard password accidentally set to service password** | When deploying multiple services (dashboard + DreamHost + WordPress), it's easy to accidentally use a service password (e.g., DreamHost SSH password) as the dashboard backdoor password. The dashboard password is a *public-facing* credential and should be separate from infrastructure passwords. | Always use a unique password for the PHP dashboard backdoor. Never reuse DreamHost, WordPress, or other service passwords. If the dashboard is compromised, service passwords should remain safe. The converse is also true — a DreamHost breach shouldn't expose the dashboard. |
| **`write_file` mangles passwords containing `*`** | The `write_file` tool's content field interprets `*text*` as markdown italic. A password like `***` or `Rm2214ri#` followed by `***` can be silently mangled. When the file is read back it shows `***` (three literal asterisks) instead of the actual value. **Always verify the raw hex bytes after writing a PHP file with a password.** | After writing a PHP file that sets a password, verify with: `python3 -c "f=open('file.php','rb'); print([hex(b) for b in f.readline()])"` or `xxd file.php | grep -A1 "ADMIN_PASS"`. If the hex doesn't match the expected password string, rewrite using Python `open()` + `write()` instead of the `write_file` tool. |
| **`mifeco.com` → `www.mifeco.com` redirect loses POST data** | When testing PHP login forms with `curl -X POST https://mifeco.com/admin/...`, the server returns a 301 redirect to `www.mifeco.com`. The POST body is lost during the redirect, so the login silently fails and returns the login page again. | **Always post directly to `www.mifeco.com`** when testing logins: `curl -X POST https://www.mifeco.com/admin/index.php -d "email=...&password=..."`. If you accidentally hit `mifeco.com`, the 301 redirect drops POST data and login fails silently. After successful login, grep for a dashboard title (not "Login") to confirm. |
| **nginx ignores .htaccess** | DreamHost (and many shared hosts) use nginx, not Apache. `.htaccess` — rewrite rules, access control, PHP flags — is completely ignored. | Never rely on `.htaccess` for routing or security on DreamHost. Use a PHP smart router in `index.php` instead. Add a comment-only `.htaccess` noting nginx ignores it. |
| **SPA intercepts /wp-json/** | When a Vite/React SPA is built to the web root, nginx's `try_files` serves `index.html` for ALL non-file-including `/wp-json/` requests. | Implement a PHP router in `index.php` that checks the request URI against known WP paths and loads `wp-blog-header.php` for those routes. Test with `curl -s 'https://domain.com/index.php/wp-json/'` not `curl -s 'https://domain.com/wp-json/'`. |
| **`--delete` wipes WordPress** | Rsync with `--delete` removes anything not in the source. WordPress lives in the same root. | Never use `--delete` on a WordPress root. Target a subdirectory like `admin/`. |
| **`$_survey` vs `$survey` typo** | `$_survey` is not a PHP superglobal — it's an undefined variable that silently returns null. `$surveyId = (int)$_survey['id']` always evaluates to 0, causing UPDATE/INSERT to affect 0 rows with no error. | Always use `$survey` (no underscore prefix). Enable `error_reporting(E_ALL)` during development to catch undefined variables. |
| **DreamHost `.htaccess` — `Require` directive** | DreamHost shared hosting uses Apache but may not support `Require all denied` (Apache 2.4+ syntax). Using it causes a 500 Internal Server Error with no useful error message. | Use `Order allow,deny` / `Deny from all` instead. Test `.htaccess` changes by checking if the page still returns 200 after each change. |
| **DreamHost PHP `error_log` disabled** | `php -i` shows `error_log => no value` — PHP's built-in error logging is disabled. `error_log()` calls silently do nothing. | Use `@file_put_contents('/tmp/debug.log', $msg . "\n", FILE_APPEND)` for ad-hoc debugging. `/tmp/` is writable on DreamHost shared hosting. Remember to remove debug code before production. |
| **Fire-and-forget curl in PHP** | `CURLOPT_TIMEOUT_MS` with `CURLOPT_NOSIGNAL` may not work reliably on all shared hosting configurations. The curl handle may hang or throw warnings that break the HTTP response. | For non-critical background API calls, either: (1) skip the call entirely and use fallback data, or (2) use a proper queue/cron system. Don't rely on fire-and-forget curl in production PHP on shared hosting. |
| **`strcasecmp` for email comparison** | `strtolower()` can produce unexpected results with Unicode. `strcasecmp()` is safer for case-insensitive email comparison. | Use `strcasecmp($email, $backdoorEmail) === 0` instead of `strtolower($email) === strtolower($backdoorEmail)`. |
**Key concept:** The `+` addressing suffix on AgentMail inboxes (e.g., `waitlist+inboxname@agentmail.to`) allows the agent to auto-classify incoming waitlist signups. The dashboard's cron pipeline reads these emails, counts them, and updates the waitlistSignups counter.

---

## Stripe Express Checkout Element (On-Page Payment)

When building a gated PHP app that requires payment, add a backdoor login for testing that bypasses payment:

### In `register.php` (login handler):

```php
// Backdoor check — BEFORE normal auth
define('BACKDOOR_EMAIL', 'test@example.com');
define('BACKDOOR_PASSWORD_HASH', password_hash('SecureP@ssw0#', PASSWORD_DEFAULT));

if ($_POST['email'] === BACKDOOR_EMAIL && 
    password_verify($_POST['password'], BACKDOOR_PASSWORD_HASH)) {
    // Auto-create account if doesn't exist
    $stmt = $db->prepare('SELECT id FROM users WHERE email = ?');
    $stmt->execute([BACKDOOR_EMAIL]);
    if (!$stmt->fetch()) {
        $stmt = $db->prepare('INSERT INTO users (email, name, password_hash, created_at) VALUES (?, ?, ?, NOW())');
        $stmt->execute([BACKDOOR_EMAIL, 'Test User', BACKDOOR_PASSWORD_HASH]);
    }
    // Set session
    $_SESSION['user_id'] = $db->lastInsertId();
    $_SESSION['user_name'] = 'Test User';
    $_SESSION['backdoor'] = true;  // Flag for payment bypass
    redirect('/pay.php');
}
```

### In `pay.php`:

```php
// Backdoor bypass — skip payment
if (!empty($_SESSION['backdoor'])) {
    redirect('/survey.php');
}
```

### Security Notes

- Store the backdoor password hash with `password_hash()`, never plaintext
- The backdoor should only work for a specific hardcoded email
- Add a comment in the code: `// BACKDOOR — remove before production`
- The `$_SESSION['backdoor']` flag should be checked on every gated page (survey, download, etc.)

### Dynamic API Pattern for Dashboards (2026-05)

Instead of embedding static JSON data in HTML `<script>` tags, use a **PHP REST API** that serves live data from JSON files. This lets the dashboard refresh without re-deploying HTML.

### API File (`/admin/api.php`)

```php
<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

$DATA_DIR = __DIR__ . '/data';

// Resource to file mapping
$RESOURCES = [
    'pipeline-state'  => __DIR__ . '/pipeline-state.json',
    'pipeline-books'  => __DIR__ . '/pipeline-books.json',
    'pipeline-saas'   => __DIR__ . '/pipeline-saas.json',
    'leads'           => __DIR__ . '/leads-registry.json',
    'unified'         => __DIR__ . '/unified-pipeline.json',
    'promotion'       => __DIR__ . '/data/promotion-status.json',
];

if ($_GET['action'] === 'get') {
    $resource = $_GET['resource'] ?? '';
    if ($resource === 'all') {
        $all = [];
        foreach ($RESOURCES as $name => $path) {
            if (file_exists($path)) {
                $all[$name] = json_decode(file_get_contents($path), true);
            }
        }
        echo json_encode($all, JSON_PRETTY_PRINT);
        exit;
    }
    if (isset($RESOURCES[$resource]) && file_exists($RESOURCES[$resource])) {
        readfile($RESOURCES[$resource]);
        exit;
    }
    http_response_code(404);
    echo json_encode(['error' => 'Not found']);
}
```

### JavaScript Dynamic Loader

```javascript
const API_BASE = 'api.php';
let dashboardData = {};

async function loadAllData() {
    const resources = ['pipeline-books','pipeline-saas','pipeline-consulting','pipeline-state','leads','unified','promotion'];
    const results = await Promise.all(resources.map(r => 
        fetch(API_BASE + '?action=get&resource=' + r).then(res => res.ok ? res.json() : null)
    ));
    resources.forEach((r, i) => { if (results[i]) dashboardData[r] = results[i]; });
}

function renderAll() {
    renderBooks(getBooksCatalog());
    renderSaaS(getSaasApps());
    renderOps(getPipelinesData());
    renderHealth(getPipelineHealth());
    renderLeadStats(getLeadStats());
    updateStatCounters();
}

async function initDashboard() {
    await loadAllData();
    renderAll();
    setInterval(async () => { await loadAllData(); renderAll(); }, 60000); // 60s refresh
}
document.addEventListener('DOMContentLoaded', initDashboard);
```

### Data Transformation

The JSON file structures rarely match what render functions expect. Write **transformer functions** that convert API data to render-ready format:

```javascript
function getBooksCatalog() {
    const pb = dashboardData['pipeline-books'];
    if (!pb?.pipeline?.products) return getDefaultBooks();
    
    const titles = [];
    const products = pb.pipeline.products;
    
    // Transform nested structure to flat array
    if (products.titles) {
        products.titles.forEach(t => titles.push({
            title: t.title,
            series: products.series || 'Unknown',
            status: t.asin ? 'published' : 'draft',
            asin: t.asin || ''
        }));
    }
    // Handle moon_books, standalone similarly...
    
    return titles.length ? titles : getDefaultBooks();
}
```

### Key Principle

**Always fetch from API → transform to render format → render.** Never embed data in HTML. The HTML is a pure presentation layer; all data lives in JSON files served by the API.

### nginx Pitfall: API File Access

When the admin directory is routed through WordPress (e.g., via an admin proxy plugin), PHP files in `/admin/` may be intercepted. To ensure the API file is accessible:
1. Place `api.php` in `/admin/` alongside other dashboard files
2. Fetch from relative path: `fetch('api.php?action=get&resource=all')` not `/admin/api.php`
3. If the admin proxy intercepts, use `index.php?rest_route=` to reach WordPress, then serve the API from a custom REST endpoint instead of a standalone PHP file

### Duplicate Endpoint Pitfall

When multiple WordPress plugins register the same REST route (e.g., `/mifeco/v1/send-email`), WordPress uses the **first registered** one. The old endpoint wins and the new one is silently ignored.

```bash
# Detect duplicate registrations
grep -rn 'register_rest_route.*send-email' wp-content/plugins/
grep -rn 'mifeco_handle_send_email' wp-content/plugins/
```

**Fix**: Remove the old endpoint registration entirely. Keep only the canonical plugin.
