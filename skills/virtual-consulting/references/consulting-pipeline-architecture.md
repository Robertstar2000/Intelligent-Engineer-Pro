# MIFECO Virtual Consulting — Pipeline Architecture Reference

## System Overview

The Virtual Consulting product is a **$199 online business assessment** at `mifeco.com/consult/`. It is a hybrid PHP + Python application deployed across two machines:

- **DreamHost shared hosting**: PHP frontend (auth, payments, survey UI, sessions)
- **Local machine** (97.91.18.250): Python API server (question generation, PDF reports)

**NOT to be confused with**: Human/expert consulting on the main mifeco.com site (free 30-min consultation booking form).

## Architecture Diagram

```
User Browser
    │
    ▼
DreamHost (mifeco.com)
    ├── /consult/index.php          ← Landing page
    ├── /consult/register.php       ← Sign up / Sign in / Backdoor
    ├── /consult/pay.php            ← Stripe Express Checkout
    ├── /consult/survey.php         ← Interactive survey engine
    ├── /consult/download.php       ← PDF download handler
    ├── /consult/stripe-webhook.php ← Stripe webhook
    ├── /consult/config.php         ← DB + Stripe + API config
    └── /consult/vendor/            ← Stripe PHP SDK v20.2.0
    │
    │  HTTP POST (5s timeout)
    ▼
Local Machine (97.91.18.250:8190)
    └── api/api_server.py
        ├── POST /api/generate-questions  ← Generate 30-50 tailored questions
        └── POST /api/generate-reports    ← Generate Assessment + Strategy Plan PDFs
                │
                ▼
            WeasyPrint → PDF files saved to ~/.hermes/consulting-reports/
```

## Database Schema (MySQL: mifeco_com_1)

All tables use `consulting_` prefix to avoid WordPress collisions.

```sql
CREATE TABLE consulting_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    business_name VARCHAR(255),
    business_role VARCHAR(100),
    business_type VARCHAR(100),
    employee_count VARCHAR(50),
    verification_token VARCHAR(64),
    verified_at DATETIME NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE consulting_surveys (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    status ENUM('initial','generating_questions','in_progress','analyzing','complete') DEFAULT 'initial',
    current_question INT DEFAULT 0,
    questions JSON NULL,
    initial_responses JSON NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE consulting_responses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    survey_id INT NOT NULL,
    question_id VARCHAR(10) NOT NULL,
    answer TEXT,
    answered_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE consulting_followups (
    id INT AUTO_INCREMENT PRIMARY KEY,
    survey_id INT NOT NULL,
    question_id VARCHAR(10) NOT NULL,
    answer TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    stripe_session_id VARCHAR(255) UNIQUE,
    stripe_payment_intent VARCHAR(255),
    amount INT DEFAULT 19900,
    currency VARCHAR(3) DEFAULT 'usd',
    status ENUM('pending','completed','failed','refunded') DEFAULT 'pending',
    paid_at DATETIME NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    survey_id INT NOT NULL,
    user_id INT NOT NULL,
    type ENUM('assessment','strategy_plan') NOT NULL,
    filename VARCHAR(255),
    file_path VARCHAR(500),
    status ENUM('generating','ready','failed') DEFAULT 'generating',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## File Inventory

### DreamHost: `/home/dh_mwpxuu/mifeco.com/consult/`

| File | Purpose |
|------|---------|
| `index.php` | Landing page with pain points, process steps, CTA |
| `register.php` | Sign up, sign in, backdoor login, survey reset |
| `pay.php` | Stripe Express Checkout Element + Card fallback |
| `survey.php` | Survey state machine, question display, response saving, IDK branching |
| `survey-questions.php` | 42 fallback questions with "I don't know" on all |
| `download.php` | PDF download handler with ownership verification |
| `stripe-webhook.php` | Stripe webhook: payment confirmed/failed/refunded |
| `config.php` | DB credentials, Stripe keys, Python API URL, helpers |
| `logout.php` | Session destroy |
| `.htaccess` | Security: blocks config.php, vendor/, directory listing |

### Local: `/mnt/usb_4tb/consulting/`

| File | Purpose |
|------|---------|
| `public/` | Mirror of DreamHost consult/ (source of truth for deployment) |
| `api/api_server.py` | Python HTTP server on port 8190 |

## User Flow (Detailed)

### 1. Landing (index.php)
- Dark-themed single-page site with animated grid background
- Pain points: Overwhelmed by Admin, Technology Confusion, Scaling Pressure, Data & Compliance, Stalled Revenue, Team Misalignment
- Process: Quick Profile → Deep Survey → Expert Analysis → Download & Act
- CTA: "Start Your Assessment → $199"
- Logged in users see "Dashboard" button instead

### 2. Authentication (register.php)
- **Register**: email, password (8+ chars), full name, business name → create account → redirect to pay.php
- **Login**: email + password → check if paid → redirect to survey.php or pay.php
- **Backdoor**: Robertstar@aol.com / Rm2214ri# → auto-create account, skip payment, reset survey to initial
- **Survey reset on backdoor login**: DELETE FROM consulting_responses, consulting_followups, consulting_surveys for user; INSERT new survey with status='initial'
- CSRF protection on all forms

### 3. Payment (pay.php)
- Requires auth (redirect to register.php if not logged in)
- Backdoor users skip payment (redirect to survey.php)
- Check if already paid (redirect to survey.php)
- Stripe Express Checkout Element: Link, Apple Pay, Google Pay, PayPal, Klarna
- Inline Card Element fallback
- AJAX: POST action=create_session → creates Stripe Checkout Session → returns sessionId
- On success: Stripe redirects to pay.php?success=1 → webhook marks payment complete → redirect to survey.php
- On cancel: Stripe redirects to pay.php?canceled=1 → show retry button

### 4. Survey Gateway (survey.php, status=initial)
- 4 gateway questions: business_role, primary_issue, business_type, employee_count
- Optional: business_name, industry, issue_description
- On submit: POST action=submit_initial → save to consulting_users and consulting_surveys.initial_responses
- Call Python API: POST /api/generate-questions with initial responses
- On success: update survey status to 'in_progress', store questions JSON
- On failure (5s timeout): use generateFallbackQuestions() from survey-questions.php
- Show loading spinner during generation

### 5. Interactive Survey (survey.php, status=in_progress)
- One question at a time, displayed with scale/choice/text input
- Progress saved after every answer (POST action=save_answer)
- "I don't know / Not applicable" option on every scale/choice question
- **IDK branching**:
  - Modal: "Someone else knows?" or "Nobody knows?"
  - Someone else: save question index to pending list, show pause screen, continue to next
  - Nobody knows: show 2-3 diagnostic follow-up questions, save to consulting_followups
- Pending "someone else knows" questions shown in banner for later completion
- After last question: POST action=submit_survey → status='analyzing' → call Python API to generate reports

### 6. Report Generation (survey.php, status=analyzing)
- Call Python API: POST /api/generate-reports with all responses
- Python builds two PDFs via WeasyPrint:
  - Assessment Report (20+ pages): benchmark comparison, root cause analysis
  - Strategic Action Plan (20+ pages): specific action steps
- PDFs saved to ~/.hermes/consulting-reports/
- On completion: update survey status to 'complete', create documents records
- On failure: retry or show error with contact support

### 7. Download (download.php)
- Requires auth
- Verify ownership: SELECT * FROM documents WHERE survey_id=? AND user_id=? AND type=? AND status='ready'
- Serve PDF with Content-Disposition: attachment
- Fallback path: consult/reports/ directory

## Survey State Machine

```
initial → generating_questions → in_progress → analyzing → complete
```

| State | What is shown |
|-------|--------------|
| `initial` | 4 gateway questions (role, issue, business type, size) |
| `generating_questions` | Loading spinner while Python API builds questions |
| `in_progress` | One question at a time with scale/choice/text input |
| `analyzing` | Loading spinner while PDFs are generated |
| `complete` | Download links for both PDF reports |

## "I Don't Know" Branching Detail

```
User selects "I don't know / Not applicable"
    │
    ▼
Modal appears:
    ┌─────────────────────────────────────┐
    │ "Someone else in your organization  │
    │  knows the answer?"                 │
    │                                     │
    │  [Yes, someone else knows]          │
    │  [No, nobody knows]                 │
    └─────────────────────────────────────┘
    │                        │
    ▼                        ▼
Save question index      Show 2-3 diagnostic
to pending list          follow-up questions:
Show pause screen        - "Why don't you know?"
Continue to next         - "What would it take
question                 to find out?"
                         - "How critical is
                         this gap?"
                         Save to consulting_followups
                         Continue to next question
```

## Reverse SSH Tunnel Setup

### Problem
DreamHost shared hosting cannot reach this machine's port 8190 (ISP/firewall blocks outbound to non-standard ports). Without a tunnel, the PHP frontend falls back to `generateFallbackQuestions()` — the Python API is unreachable for question generation and PDF report building.

### Solution: paramiko Reverse Forward Tunnel

The tunnel uses paramiko's `request_port_forward()` to create a remote-forward from DreamHost:`localhost:8190` → this machine:`localhost:8190`.

**Tunnel script** (`/tmp/reverse_tunnel.py`):
```python
import paramiko, socket, select, threading

def forward_tunnel(transport, remote_port, local_host, local_port):
    def handler(chan, host, port):
        sock = socket.socket()
        sock.connect((host, port))
        while True:
            r, w, x = select.select([sock, chan], [], [])
            if sock in r:
                data = sock.recv(1024)
                if not data: break
                chan.send(data)
            if chan in r:
                data = chan.recv(1024)
                if not data: break
                sock.send(data)
        chan.close(); sock.close()

    transport.request_port_forward("", remote_port)
    while transport.is_active():
        chan = transport.accept(1000)
        if chan is None: continue
        t = threading.Thread(target=handler, args=(chan, local_host, local_port))
        t.daemon = True; t.start()
```

**Run it**:
```bash
nohup /tmp/tunnel-env/bin/python3 /tmp/reverse_tunnel.py > /tmp/tunnel.log 2>&1 &
```

**Config changes** (deploy to DreamHost `config.php`):
```
define('PYTHON_API_URL', 'http://127.0.0.1:8190');  # via tunnel, not public IP
```

### Prerequisites
- `uv` → `uv venv /tmp/tunnel-env` → `uv pip install paramiko --python /tmp/tunnel-env/bin/python`
- DreamHost SSH must allow `request_port_forward` (most shared hosts do)

### Cron Job Watchdog
A cron job checks every 5 minutes that both the tunnel and API server are running:

| Job | Schedule | Purpose |
|-----|----------|---------|
| `reverse-tunnel-monitor` | every 5m | Restarts tunnel or API if dead |

```bash
# Check tunnel: ps aux | grep reverse_tunnel | grep -v grep
# Check API: ss -tlnp | grep 8190
```

### Testing the Tunnel from DreamHost
```python
import paramiko
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("ssh.mifeco.com", username="dh_mwpxuu", password="<PASS>", timeout=15)
stdin, stdout, stderr = c.exec_command(
    "curl -s http://127.0.0.1:8190/api/generate-questions "
    "-H 'Content-Type: application/json' "
    "-d '{\"api_key\":\"mifeco-local-api-key-change-this\",\"business_role\":\"owner\"}' "
    "--max-time 10"
)
print(stdout.read().decode())  # Should return {"success": true, "questions": [...]}
```

### Endpoints

**POST /api/generate-questions**
```json
{
  "api_key": "mifeco-local-api-key-change-this",
  "initial": {
    "business_role": "Owner",
    "primary_issue": "Operations",
    "business_type": "Service",
    "employee_count": "10-50"
  }
}
```
Returns: `{"success": true, "questions": [...]}` (30-50 questions across 6 dimensions)

**POST /api/generate-reports**
```json
{
  "api_key": "mifeco-local-api-key-change-this",
  "responses": [...],
  "initial": {...}
}
```
Returns: `{"success": true, "assessment_path": "...", "strategy_plan_path": "..."}`

### Question Dimensions
1. People & Culture (7 areas)
2. Process & Operations (7 areas)
3. Technology (7 areas)
4. Data & Analytics (7 areas)
5. Financial Health (7 areas)
6. Customer Experience (7 areas)

### Running the Server
```bash
cd /mnt/usb_4tb/consulting/api
nohup python3 api_server.py > /tmp/api_server.log 2>&1 &
echo "PID: $!"

# Verify listening (use ss, not netstat — often not installed)
ss -tlnp | grep 8190
```

### Health Check
```bash
curl -s -X POST http://localhost:8190/api/generate-questions \
  -H "Content-Type: application/json" \
  -d '{"api_key":"mifeco-local-api-key-change-this","initial":{"business_role":"Owner","primary_issue":"Operations"}}'
```

## Deployment Procedures

### PHP Files (DreamHost via SFTP)
```python
import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("ssh.mifeco.com", username="dh_mwpxuu", password="Rm2214ri####", timeout=15)
sftp = client.open_sftp()
sftp.put("/mnt/usb_4tb/consulting/public/<filename>.php",
         "/home/dh_mwpxuu/mifeco.com/consult/<filename>.php")
sftp.close()
client.close()
```

**Always edit in `/mnt/usb_4tb/consulting/public/` first, then deploy.**

### JS Bundle (mifeco.com main site)
```python
sftp.put("/tmp/mifeco_bundle_modified.js",
         "/home/dh_mwpxuu/mifeco.com/assets/index-Dd5ye8Ze.js")
```

**Verify MD5 after upload.** The bundle filename is content-hashed — if hash changes, update index.html.

### Python API (Local)
```bash
pkill -f api_server.py
cd /mnt/usb_4tb/consulting/api
nohup python3 api_server.py > /tmp/api_server.log 2>&1 &
```

## Configuration Reference

### config.php
```php
// Database
define('DB_HOST', 'mysql.mifeco.com');
define('DB_NAME', 'mifeco_com_1');
define('DB_USER', 'ak48bme');
define('DB_PASS', '7jpetxEL');

// Stripe (PLACEHOLDERS)
define('STRIPE_PUBLISHABLE_KEY', 'pk_live_CHANGEME');
define('STRIPE_SECRET_KEY', 'sk_live_CHANGEME');
define('STRIPE_PRICE_ID', 'price_CHANGEME');
define('STRIPE_WEBHOOK_SECRET', 'whsec_CHANGEME');

// Python API
define('PYTHON_API_URL', 'http://97.91.18.250:8190');
define('PYTHON_API_KEY', 'mifeco-local-api-key-change-this');

// Site
define('SITE_URL', 'https://mifeco.com/consult');
```

## Main Site Integration (mifeco.com)

The main site is a React SPA in `assets/index-Dd5ye8Ze.js` (minified, ~470KB, no source map).

### Virtual Consulting Links (all → /consult)
| Location | Element | Links To |
|----------|---------|----------|
| Desktop nav | "Virtual Consulting" | `/consult` (new tab) |
| Mobile nav | "Virtual Consulting" | `/consult` (new tab) |
| Hero | "Business Assessment — $199" button | `/consult` (new tab) |
| Products card | "Virtual Consulting" title | `/consult` (new tab) |
| Products card | "Start Your Assessment — $199" button | `/consult` (new tab) |
| $199 Card | "$199 Business Assessment" title | `/consult` (new tab) |
| $199 Card | "Start Assessment — $199" button | `/consult` (new tab) |
| Footer | "Virtual Consulting" | `/consult` (new tab) |
| Footer | "Books & Bookstore" | `/books` (new tab) |

### Human Consulting Links (keep separate)
| Location | Element | Action |
|----------|---------|--------|
| Various | "Schedule Free Consultation" buttons | Opens consultation form popup |
| Various | "Consult with an Expert" buttons | Opens consultation form popup |
| Industries | "Schedule Industry Consultation" | Opens consultation form |
| Popup | "Book your free 30-minute strategy session" | Human expert consultation |

## Credentials

| System | Host | User | Password | Method |
|--------|------|------|----------|--------|
| DreamHost SSH/SFTP | ssh.mifeco.com | dh_mwpxuu | Rm2214ri#### | paramiko (password auth) |
| MySQL | mysql.mifeco.com | ak48bme | 7jpetxEL | PDO |
| Stripe | — | — | pk_live_CHANGEME (placeholder) | — |
| Python API | 97.91.18.250:8190 | — | mifeco-local-api-key-change-this | HTTP |
| Backdoor login | — | Robertstar@aol.com | Rm2214ri# | Hardcoded in register.php |

## Known Issues

1. ~~**Python API unreachable from DreamHost**~~ **RESOLVED**: Port 8190 was outbound blocked by ISP/firewall, so DreamHost PHP could not reach the Python API. **Fix applied**: A paramiko-based reverse SSH tunnel (`request_port_forward`) bridges DreamHost:8190 → this machine's localhost:8190. PHP config was changed from `http://97.91.18.250:8190` to `http://127.0.0.1:8190`. A cron job monitors tunnel + API health every 5 minutes. See "Reverse SSH Tunnel Setup" below.
2. **Stripe keys are placeholders**: pk_live_CHANGEME, price_CHANGEME, whsec_CHANGEME. Real keys needed for production.
3. **JS bundle is fragile**: Minified, no source map. Always verify MD5 after upload.
4. **Session requires HTTPS**: session.cookie_secure=1. Won't work on HTTP.
5. **Backdoor survey reset**: Must delete consulting_responses, consulting_followups, and consulting_surveys before creating fresh survey.
6. **"$199" buttons opening wrong target** (June 2026): Any button with "$199" or "Book for $199" text MUST open `/consult` in a new tab (`window.open("/consult","_blank")`). It must NOT open the human consultation form popup (`de(!0)`). The "Book for $199" button in the products card was incorrectly wired to `onClick:()=>de(!0)` instead of `onClick:()=>window.open("/consult","_blank")`. Always verify the onClick handler when modifying product cards in the JS bundle.

## MemPalace Memory Storage

The virtual consulting pipeline architecture and credentials are stored in MemPalace for cross-session retrieval:

- **Storage path**: `~/.hermes/mempalace/`
- **FAISS index**: 42 vectors, 384-dim, IndexFlatIP
- **Embedding model**: all-MiniLM-L6-v2
- **Key entries**:
  - `d20a43cc` — Full pipeline architecture (score 0.56 for pipeline queries)
  - `f1dd1327` — Credentials and configuration (score 0.53 for credentials queries)
- **Search**: `embed.search_embeddings("virtual consulting pipeline", k=5)`
- **Direct module import** (for cron/non-interactive): `import capture; import tag; import embed` then call `init_*()` individually

## E2E Testing Procedure

Test the full survey flow end-to-end using the backdoor credentials. Useful after any config/survey/API change.

### Prerequisites
- Tunnel and API server running (port 8190 reachable from DreamHost via 127.0.0.1)
- A working session cookie jar (`/tmp/cookies.txt`)

### Step 1: Login via Backdoor
```bash
# Get CSRF token from register page
CSRF=$(curl -s -c /tmp/cookies.txt -b /tmp/cookies.txt \
  "https://www.mifeco.com/consult/register.php?tab=login" | \
  grep -oP 'name="csrf_token" value="\K[^"]+')

# Login with backdoor credentials
curl -s -c /tmp/cookies.txt -b /tmp/cookies.txt \
  -w "HTTP %{http_code} -> %{url_effective}" \
  "https://www.mifeco.com/consult/register.php" \
  -d "action=login&email=Robertstar%40aol.com&password=Rm2214ri%23&csrf_token=$CSRF"
```
Expected: `HTTP 200 -> https://www.mifeco.com/consult/survey.php`

Note: Tab switching uses URL query params (`?tab=register` / `?tab=login`), not JavaScript.

### Step 2: Submit Gateway (4 initial questions)
```bash
CSRF=$(curl -s -c /tmp/cookies.txt -b /tmp/cookies.txt \
  "https://www.mifeco.com/consult/survey.php" | \
  grep -oP 'name="csrf_token" value="\K[^"]+')

curl -s -c /tmp/cookies.txt -b /tmp/cookies.txt \
  -w "HTTP %{http_code}" \
  "https://www.mifeco.com/consult/survey.php" \
  -d "action=submit_initial&business_role=owner&primary_issue=Technology+Confusion&business_type=LLC&employee_count=1-10&business_name=Test+Corp&industry=technology&issue_description=testing&csrf_token=$CSRF"
```
Expected: HTTP 200, survey switches from `initial` → `generating_questions` → `in_progress`

### Step 3: Answer Survey Questions
```bash
# Get fresh CSRF (new token per page load, stored in session)
CSRF=$(curl -s -c /tmp/cookies.txt -b /tmp/cookies.txt \
  "https://www.mifeco.com/consult/survey.php" | \
  grep -oP 'name="csrf_token" value="\K[^"]+')

# Answer question q01
curl -s -c /tmp/cookies.txt -b /tmp/cookies.txt \
  "https://www.mifeco.com/consult/survey.php" \
  -d "action=answer&question_id=q01&answer=4+%E2%80%93+Comfortable&question_index=0&is_last=0&csrf_token=$CSRF"
```
CSRF tokens are session-bound — always extract from the current page before POSTing. A 403 means the token expired or session was lost.

### Step 4: Verify Key Outputs
- Check `status` field in page — should show `in_progress` with question count
- Verify "I don't know / Not applicable" option exists on every scale/choice question
- Verify IDK modal has both branching paths
- Check progress bar shows correct percentage
- After final question, status transitions: `in_progress` → `analyzing` → `complete`

### Step 5: Verify PDF Generation
After survey completion, check the reports directory:
```bash
ls -la ~/.hermes/consulting-reports/
```
Expected: Two PDF files (assessment + strategy plan)

When tunnel is down, the fallback `generateFallbackQuestions()` is used instead — verify by checking for 42 hardcoded questions with IDK options.

### Browser E2E Testing Notes
The survey is a PHP-rendered page (not an SPA). Key behaviors:
- Scale buttons use `onclick="pickScale(this)"` JS handlers
- "I don't know" on scale/choice triggers JS modal (`showDkModal()`)
- Multiple forms exist per page (question form, IDK modal forms)
- CSRF hidden input is on every form
- Some clicks may trigger empty snapshots in browser tool (JS rendering quirks) — navigate directly to known URLs when this happens

- [ ] `curl -I https://mifeco.com/consult/` returns 200
- [ ] Landing page shows "Business Assessment for Any Issue"
- [ ] No "AI Readiness" text anywhere
- [ ] Backdoor login works: Robertstar@aol.com / Rm2214ri#
- [ ] Backdoor redirects to survey gateway (4 initial questions)
- [ ] Survey advances past gateway
- [ ] "I don't know" option on all scale/choice questions
- [ ] IDK modal shows both branching options
- [ ] Main site nav: "Virtual Consulting" → /consult
- [ ] Main site buttons: "Business Assessment — $199" → /consult
- [ ] Human consulting forms still work
- [ ] JS bundle MD5 matches after upload
