---
name: local-saas-app-setup
description: Clone, configure, and run multiple Node.js/TypeScript web apps locally from GitHub source repos — port conflict resolution, env var config, background process management, and health verification. Use when setting up local dev environments for pre-built SaaS apps.
version: 1.0.0
author: Hermes Agent
---


## Memory context (Hindsight)

Long-term memory context is now provided automatically by Hindsight (bank
`mifeco-default`) on every turn — the retired MemPalace manual query step no
longer applies. Do NOT attempt to import `~/.hermes/mempalace` (it was removed
2026-08-19).This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

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

## DOX Integration

When working in a project that uses the [DOX (Self-documenting AGENTS.md)](https://github.com/agent0ai/dox) framework:

- **Read Before Editing:** Walk the DOX tree from root to the target path. Read every AGENTS.md along the route before making any changes.
- **Update After Editing:** If the change affects purpose, scope, ownership, structure, workflows, or operating rules, update the closest owning AGENTS.md and refresh the Child DOX Index.
- **Reference:** [agent0ai/dox](https://github.com/agent0ai/dox) — copy `AGENTS.md` from the repo root into your project to initialize.

## Common Pitfalls

- **Hardcoded ports**: Most `server.ts` files hardcode `const PORT = 3000`. Always check before starting multiple apps.
- **Missing .env files**: Apps often need `GEMINI_API_KEY` or similar. Check `~/.hermes/.env` first, but be aware the security tool may redact values — you may need to read the file raw in terminal.
- **Module import errors**: TypeScript apps use `tsx` (not `ts-node`). If `tsx` isn't in the project's `devDependencies`, install it: `npm install --save-dev tsx`
- **Background process tracking**: Use Hermes `background=true` terminal parameter, not `nohup` or `&` directly, so Hermes can track lifecycle.
- **npm audit warnings**: These are normal for AI Studio apps — ignore them.
- **Firebase/Firestore dependencies**: AI Studio apps often have Firebase config files but work without them for local dev.

## MIFECO SaaS Integration Pattern

When setting up apps for the MIFECO SaaS product ecosystem (not just local dev), additional steps:
1. **Free/Pro tier flags**: Add feature-flag system distinguishing free vs paid features. See `openclaw-saas-operations` skill for tier structure.
2. **Stripe integration**: Add Stripe payment link/webhook endpoints. User provides Stripe keys after scaffolding.
3. **Unified auth**: Each app has its own SQLite auth — for Pro tier, plan to unify via Supabase or shared JWT.
4. **Ops dashboard**: Register new app in the unified monitoring dashboard at `~/saas/ops-dashboard/`.
5. **Pipeline-engine registration**: Add product to MIFECO pipeline-engine's product lines for lead routing.
6. **Backup**: Add product directory to the nightly-backup GitHub sync step in the `nightly-backup` cron job.
7. **Naming**: Rename GitHub default directory names to clean hyphenated names (e.g., `https-github.com-Robertstar2000-HypatiaPro` → `hypatia-pro`).
8. **.env management**: Each app gets its own `.env` for local dev; shared secrets go in `~/saas/.env`. Never commit `.env` to any repo.

- Each app returns HTTP 200 on its assigned port
- HTML response contains meaningful content (not just "Cannot GET /")
- Dashboard (if created) shows all apps online
