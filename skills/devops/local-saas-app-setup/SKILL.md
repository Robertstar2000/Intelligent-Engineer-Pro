---
name: local-saas-app-setup
description: Clone, configure, and run multiple Node.js/TypeScript web apps locally from GitHub source repos — port conflict resolution, env var config, background process management, and health verification. Use when setting up local dev environments for pre-built SaaS apps.
version: 1.0.0
author: Hermes Agent
---


## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("MIFECO business process", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Local SaaS App Setup

## When to Use

Use this skill when a user asks you to "install", "set up", "run locally", or "configure" one or more pre-built web applications that exist as GitHub repos. The trigger is the CLASS of task: cloning existing source code and running it locally, NOT building from scratch. 

Applies to:
- Node.js/TypeScript apps (React/Vite/Express, NestJS, etc.)
- Python web apps (Flask, FastAPI, Django)
- Any app with a standard `package.json`, `requirements.txt`, or similar
- Multiple apps that need to coexist on different ports

Do NOT use this for:
- Building a new app from scratch (use project-specific skills)
- Deploying to cloud platforms (use cloud-deploy skills)
- Docker container setup (use docker skills)

## Workflow

### 1. Organize Repos
Clone all repos into a project directory structure:
```
~/projects/
  ├── AppName1/
  ├── AppName2/
  └── start-all.sh
```

Create descriptive directory names (not raw repo names).

### 2. Read Everything First
For each app, read:
- **README.md** — build instructions, prereqs, env vars
- **package.json** / requirements.txt — dependencies, scripts, name
- **server.ts** / app.py / main entry — default port, env var support

### 3. Configure Environment
- Read the project's existing `.env.example` or documentation for required vars
- Create `.env.local` or `.env` files with working API keys (from the user's credentials store — check `~/.hermes/.env` for keys like `GEMINI_API_KEY`, `OPENROUTER_API_KEY`)
- Never hardcode secrets into scripts — always use `.env` files

### 4. Resolve Port Conflicts
Most apps default to port 3000. When running multiple:
1. Check if the server respects `process.env.PORT` (Express/Node) or an env var
2. If hardcoded, patch the source to read from environment:
   ```typescript
   // Before:
   const PORT = 3000;
   // After:
   const PORT = parseInt(process.env.PORT || "3000", 10);
   ```
3. Assign unique ports per app (e.g., 3001, 3002, 3003)

### 5. Install Dependencies
```bash
cd /path/to/app && npm install
# or: pip install -r requirements.txt
```

Use `background=true` with `notify_on_complete=true` for long installs.

### 6. Start as Background Services
```bash
cd /path/to/app && PORT=3001 npx tsx server.ts 2>&1
```
Use terminal `background=true` (not nohup/disown) so Hermes tracks lifecycle.

### 7. Verify Everything
For each app, verify with HTTP health checks:
```python
import subprocess
r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
                    f"http://localhost:{port}"], capture_output=True, text=True, timeout=5)
assert r.stdout == "200"
```

Also verify the response contains real app HTML (not empty or error pages).

### 8. Create Startup Script
Create a shell script that starts all services:
```bash
cd /path/to/App1 && PORT=3001 nohup npx tsx server.ts > /tmp/app1.log 2>&1 &
cd /path/to/App2 && PORT=3002 nohup npx tsx server.ts > /tmp/app2.log 2>&1 &
```

### 9. (Optional) Build an Ops Dashboard
For 2+ apps, create a simple Flask dashboard to monitor all services:
- Live health status via curl on each port
- Quick-launch links (local, production, repo)
- Auto-refresh every 30s
- Run on a dedicated port (e.g., 5540)

## Common Pitfalls

- **Hardcoded ports**: Most `server.ts` files hardcode `const PORT = 3000`. Always check before starting multiple apps.
- **Missing .env files**: Apps often need `GEMINI_API_KEY` or similar. Check `~/.hermes/.env` first, but be aware the security tool may redact values — you may need to read the file raw in terminal.
- **Module import errors**: TypeScript apps use `tsx` (not `ts-node`). If `tsx` isn't in the project's `devDependencies`, install it: `npm install --save-dev tsx`
- **Background process tracking**: Use Hermes `background=true` terminal parameter, not `nohup` or `&` directly, so Hermes can track lifecycle.
- **npm audit warnings**: These are normal for AI Studio apps — ignore them.
- **Firebase/Firestore dependencies**: AI Studio apps often have Firebase config files but work without them for local dev.

## Verification

- Each app returns HTTP 200 on its assigned port
- HTML response contains meaningful content (not just "Cannot GET /")
- Dashboard (if created) shows all apps online
