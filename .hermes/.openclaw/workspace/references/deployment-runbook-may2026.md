# MIFECO Cloud Run Deployment Runbook
**Last Updated:** May 30, 2026
**Author:** OWL (Automated)
**Audience:** Bob (manual operator)

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [App 1: Project Hypatia Pro](#2-app-1-project-hypatia-pro)
3. [App 2: PM Accelerator (HMAP)](#3-app-2-pm-accelerator-hmap)
4. [App 3: VibraEngineer](#4-app-3-vibraengineer)
5. [Security Headers Deployment](#5-security-headers-deployment-helmetjs-verification)
6. [Post-Deploy Verification Checklist](#6-post-deploy-verification-checklist)
7. [Rollback Procedure](#7-rollback-procedure)
8. [Troubleshooting](#8-troubleshooting)

---

## 1. Prerequisites

### 1.1 Install Google Cloud SDK

The gcloud CLI is **NOT** installed on the cron job machine. Bob must install it on a local workstation before running any commands in this runbook.

```bash
# Option A: Install via apt (Debian/Ubuntu)
sudo apt-get install google-cloud-cli

# Option B: Install via snap
sudo snap install google-cloud-cli --classic

# Option C: Install via official script (any Linux)
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

Verify installation:
```bash
gcloud --version
```

### 1.2 Authenticate & Configure project

```bash
# Login to Google Cloud
gcloud auth login

# Set the active project (use the numeric project ID or project name)
gcloud config set project mifeco-saasmvp

# Verify the active configuration
gcloud config list
```

### 1.3 Enable Required APIs

Run these once per project (skip if already enabled):

```bash
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  containerregistry.googleapis.com
```

### 1.4 Verify Source Repositories

Confirm the source directories exist on the local machine at `/home/bob/saas/`:

```bash
ls -la /home/bob/saas/Project_Hypatia_Pro/
ls -la /home/bob/saas/Project_Management_Accelerator/
ls -la /home/bob/saas/VibraEngineer/
```

Each directory should contain `server.ts`, `package.json`, `node_modules/` (pre-bundled), `vite.config.*`, `tsconfig.json`, and source files.

**Key fact:** `node_modules` directories are pre-bundled — Cloud Build will **not** need to run `npm install`, making builds fast (~1-3 minutes).

### 1.5 Deploy Order

Deploy in this order to minimize risk:

1. **Project Hypatia Pro** (simplest, fewest routes — good smoke test)
2. **PM Accelerator** (moderate complexity, SQLite-backed)
3. **VibraEngineer** (has CORS wildcard issue noted below)

---

## 2. App 1: Project Hypatia Pro

### Source Details

| Field | Value |
|-------|-------|
| **Source Path** | `/home/bob/saas/Project_Hypatia_Pro/` |
| **Package Name** | `project-hypatia-pro` |
| **Expected URL** | `https://project-hypatia-pro-1064319572465.us-west1.run.app` |
| **Helmet.js Line** | Line 53 in `server.ts` |
| **Health Endpoint** | `GET /api/health` |
| **Cloud Run Region** | `us-west1` |
| **Database** | SQLite (`better-sqlite3`, file at `/tmp/mifeco.db` in prod) |
| **Auth** | JWT-based (`jsonwebtoken`) |

### Deploy Command

```bash
# Navigate to source directory
cd /home/bob/saas/Project_Hypatia_Pro/

# Deploy using Cloud Build (no Dockerfile needed — auto-detects Node.js)
gcloud run deploy project-hypatia-pro \
  --source . \
  --region us-west1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --timeout 300 \
  --set-env-vars "NODE_ENV=production"
```

**Expected output (abbreviated):**
```
Building using Buildpack... Done.
  ✓ Uploading container to project-hypatia-pro
  ✓ Creating Revision project-hypatia-pro-000XX
Done.
Service [project-hypatia-pro] revision [project-hypatia-pro-000XX] has been deployed and is serving 100 percent of traffic.
Service URL: https://project-hypatia-pro-1064319572465.us-west1.run.app
```

### Verification Steps

```bash
# 1. Check the service is running
gcloud run services describe project-hypatia-pro --region us-west1

# 2. Test the health endpoint
curl -s https://project-hypatia-pro-1064319572465.us-west1.run.app/api/health | python3 -m json.tool

# Expected response:
# {
#     "status": "ok",
#     "timestamp": "2026-05-30T...",
#     "env": "production"
# }

# 3. Verify the root page loads (check for HTML)
curl -si https://project-hypatia-pro-1064319572465.us-west1.run.app/ | head -30

# 4. Verify helmet security headers are present (see Section 5)
curl -si https://project-hypatia-pro-1064319572465.us-west1.run.app/api/health 2>/dev/null | grep -i "x-content-type-options\|x-frame-options\|strict-transport-security\|content-security-policy"
```

---

## 3. App 2: PM Accelerator (HMAP)

### Source Details

| Field | Value |
|-------|-------|
| **Source Path** | `/home/bob/saas/Project_Management_Accelerator/` |
| **Package Name** | `project-management-accelerator` |
| **Expected URL** | `https://project-management-accelerator-845075991286.us-west1.run.app` |
| **Helmet.js Line** | Line 19 in `server.ts` |
| **Health Endpoint** | `GET /api/projects` (no dedicated health endpoint; this returns projects array) |
| **Cloud Run Region** | `us-west1` |
| **Database** | SQLite (`sqlite3` + `sqlite`, file at `./database.sqlite`) |
| **CORS** | `cors()` middleware (wildcard — see VibraEngineer note below) |
| **AI** | `@google/genai` for Gemini integration |

### Deploy Command

```bash
# Navigate to source directory
cd /home/bob/saas/Project_Management_Accelerator/

# Deploy using Cloud Build
gcloud run deploy project-management-accelerator \
  --source . \
  --region us-west1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --timeout 300 \
  --set-env-vars "NODE_ENV=production"
```

### Verification Steps

```bash
# 1. Check the service descriptor
gcloud run services describe project-management-accelerator --region us-west1

# 2. Test the root page loads
curl -si https://project-management-accelerator-845075991286.us-west1.run.app/ | head -30

# 3. Test the projects API (should return empty array on fresh deploy)
curl -s https://project-management-accelerator-845075991286.us-west1.run.app/api/projects | python3 -m json.tool

# Expected response: []

# 4. Verify helmet headers
curl -si https://project-management-accelerator-845075991286.us-west1.run.app/ 2>/dev/null | grep -i "x-content-type-options\|x-frame-options\|strict-transport-security"
```

> **Note:** This app has `cors()` with no configuration options, meaning it allows all origins. This is intentional per the current deployment but should be restricted in the future.

---

## 4. App 3: VibraEngineer

### Source Details

| Field | Value |
|-------|-------|
| **Source Path** | `/home/bob/saas/VibraEngineer/` |
| **Package Name** | `vibraengineer` |
| **Expected URL** | `https://vibraengineer-845075991286.us-west1.run.app` |
| **Helmet.js Line** | Line 21 in `server.ts` |
| **Health Endpoint** | No dedicated health endpoint — use root `GET /` |
| **Cloud Run Region** | `us-west1` |
| **Database** | SQLite (`sqlite3` + `sqlite`, file at `./database.sqlite`) |
| **AI** | `@google/genai` for Gemini integration |
| **⚠️ CORS Issue** | `app.use(cors())` on line 19 — wildcard `Access-Control-Allow-Origin: *` |

### Deploy Command

```bash
# Navigate to source directory
cd /home/bob/saas/VibraEngineer/

# Deploy using Cloud Build
gcloud run deploy vibraengineer \
  --source . \
  --region us-west1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --timeout 300 \
  --set-env-vars "NODE_ENV=production"
```

### ⚠️ Known CORS Wildcard Issue

VibraEngineer has `app.use(cors())` on line 19 of `server.ts` with **no origin restriction**, resulting in `access-control-allow-origin: *` for all responses. While the app is public, this is a security concern forcredentialed requests (auth APIs are exposed).

**Fix (before next deploy):**

In `/home/bob/saas/VibraEngineer/server.ts`, change:
```ts
app.use(cors());
```
to:
```ts
app.use(cors({
  origin: ['https://vibraengineer-845075991286.us-west1.run.app'],
  credentials: true
}));
```

### Verification Steps

```bash
# 1. Check the service descriptor
gcloud run services describe vibraengineer --region us-west1

# 2. Test the root page loads
curl -si https://vibraengineer-845075991286.us-west1.run.app/ | head -30

# 3. Verify the CORS header is present (wildcard — known issue)
curl -si -X OPTIONS \
  -H "Origin: https://example.com" \
  https://vibraengineer-845075991286.us-west1.run.app/ 2>/dev/null | grep -i "access-control-allow-origin"

# Expected: "access-control-allow-origin: *"
# This is the known wildcard issue documented above.

# 4. Verify helmet headers
curl -si https://vibraengineer-845075991286.us-west1.run.app/ 2>/dev/null | grep -i "x-content-type-options\|x-frame-options\|strict-transport-security\|content-security-policy"
```

---

## 5. Security Headers Deployment (helmet.js Verification)

All three apps use **helmet v8.1.0** middleware. Verify security headers are live after each deployment.

### How helmet is wired in each app

| App | File | Line | Code |
|-----|------|------|------|
| Project Hypatia Pro | `server.ts` | 53 | `app.use(helmet());` |
| PM Accelerator | `server.ts` | 19 | `app.use(helmet());` |
| VibraEngineer | `server.ts` | 21 | `app.use(helmet());` |

### Verification Command (all apps)

```bash
# Run this helper script to check all three apps at once for helmet headers:
check_helmet() {
  local url=$1
  local name=$2
  echo "=== $name ==="
  curl -si "$url" 2>/dev/null | grep -iE \
    "x-content-type-options|x-frame-options|strict-transport-security|content-security-policy|x-dns-prefetch-control|x-download-options|x-xss-protection|referrer-policy"
  echo ""
}

check_helmet "https://project-hypatia-pro-1064319572465.us-west1.run.app/api/health" "Project Hypatia Pro"
check_helmet "https://project-management-accelerator-845075991286.us-west1.run.app/" "PM Accelerator"
check_helmet "https://vibraengineer-845075991286.us-west1.run.app/" "VibraEngineer"
```

### Expected helmet v8 Response Headers

```
x-content-type-options: nosniff
x-frame-options: sameorigin
strict-transport-security: max-age=15552000; includeSubDomains
x-download-options: noopen
x-xss-protection: 0
referrer-policy: no-referrer
```

> **Note:** helmet v8 does NOT set `content-security-policy` by default. If CSP headers are needed, add helmet options:
> ```ts
> app.use(helmet({
>   contentSecurityPolicy: {
>     directives: {
>       defaultSrc: ["'self'"],
>       scriptSrc: ["'self'", "https://esm.sh"],
>       styleSrc: ["'self'", "'unsafe-inline'"],
>     },
>   },
> }));
> ```

---

## 6. Post-Deploy Verification Checklist

Run these commands **after all three apps are deployed**. Copy the output and save it for the deployment record.

### 6.1 Service Status Check

```bash
# List all deployed services in us-west1
gcloud run services list --region us-west1

# Expected output should show all 3 services with status "✓"
```

### 6.2 Health & Availability Tests

```bash
# --- Project Hypatia Pro ---
echo "--- Hypatia Pro ---"
curl -s -o /dev/null -w "HTTP %{http_code}" https://project-hypatia-pro-1064319572465.us-west1.run.app/
echo ""
curl -s https://project-hypatia-pro-1064319572465.us-west1.run.app/api/health
echo ""

echo "--- PM Accelerator ---"
curl -s -o /dev/null -w "HTTP %{http_code}" https://project-management-accelerator-845075991286.us-west1.run.app/
echo ""
curl -s https://project-management-accelerator-845075991286.us-west1.run.app/api/projects
echo ""

echo "--- VibraEngineer ---"
curl -s -o /dev/null -w "HTTP %{http_code}" https://vibraengineer-845075991286.us-west1.run.app/
echo ""
```

### 6.3 Security Headers Check

```bash
echo "=== All Headers Check ==="

for url in \
  "https://project-hypatia-pro-1064319572465.us-west1.run.app/api/health" \
  "https://project-management-accelerator-845075991286.us-west1.run.app/" \
  "https://vibraengineer-845075991286.us-west1.run.app/"; do
  echo ""
  echo ">>> $url"
  curl -si "$url" 2>/dev/null | grep -iE \
    "HTTP/|x-content-type-options|x-frame-options|strict-transport-security|content-security-policy|referrer-policy|access-control-allow-origin"
done
```

### 6.4 CDN / ESM.sh Resource Check

All three apps load React and other ES modules from `esm.sh`. As of May 2026 these loading issues are **resolved**, but verify after deploy:

```bash
# Check that the HTML shells reference esm.sh correctly
echo "=== Checking HTML shells for esm.sh references ==="

for url in \
  "https://project-hypatia-pro-1064319572465.us-west1.run.app/" \
  "https://project-management-accelerator-845075991286.us-west1.run.app/" \
  "https://vibraengineer-845075991286.us-west1.run.app/"; do
  echo ""
  echo ">>> $url"
  curl -s "$url" | grep -oP 'https://esm\.sh/[^"]+' | head -5
done
```

### 6.5 Full Verification Script

Save and run this as a single script for complete post-deploy verification:

```bash
#!/bin/bash
# mifeco-post-deploy-check.sh
# Run after deploying all 3 apps

PASS=0
FAIL=0

check() {
  local desc="$1"
  local expected="$2"
  local actual="$3"
  if echo "$actual" | grep -q "$expected"; then
    echo "  ✅ PASS: $desc"
    ((PASS++))
  else
    echo "  ❌ FAIL: $desc (expected '$expected', got '$actual')"
    ((FAIL++))
  fi
}

echo "========================================"
echo " MIFECO Post-Deploy Verification"
echo " $(date)"
echo "========================================"

# --- Hypatia Pro ---
echo ""
echo "--- Project Hypatia Pro ---"
HP_URL="https://project-hypatia-pro-1064319572465.us-west1.run.app"

HTTP=$(curl -s -o /dev/null -w "%{http_code}" "${HP_URL}/")
check "HTTP 200" "200" "$HTTP"

BODY=$(curl -s "${HP_URL}/api/health")
check "Health endpoint OK" '"status":"ok"' "$BODY"

HEADERS=$(curl -si "${HP_URL}/api/health" 2>/dev/null)
check "X-Content-Type-Options" "nosniff" "$HEADERS"
check "X-Frame-Options" "sameorigin" "$HEADERS"

# --- PM Accelerator ---
echo ""
echo "--- PM Accelerator ---"
PMA_URL="https://project-management-accelerator-845075991286.us-west1.run.app"

HTTP=$(curl -s -o /dev/null -w "%{http_code}" "${PMA_URL}/")
check "HTTP 200" "200" "$HTTP"

PROJ=$(curl -s "${PMA_URL}/api/projects")
check "Projects API returns array" "\[" "$PROJ"

HEADERS=$(curl -si "${PMA_URL}/" 2>/dev/null)
check "X-Content-Type-Options" "nosniff" "$HEADERS"
check "X-Frame-Options" "sameorigin" "$HEADERS"

# --- VibraEngineer ---
echo ""
echo "--- VibraEngineer ---"
VE_URL="https://vibraengineer-845075991286.us-west1.run.app"

HTTP=$(curl -s -o /dev/null -w "%{http_code}" "${VE_URL}/")
check "HTTP 200" "200" "$HTTP"

HEADERS=$(curl -si "${VE_URL}/" 2>/dev/null)
check "X-Content-Type-Options" "nosniff" "$HEADERS"
check "X-Frame-Options" "sameorigin" "$HEADERS"
# Note: CORS wildcard is expected (known issue)
check "CORS header present" "access-control-allow-origin" "$HEADERS"

# --- Summary ---
echo ""
echo "========================================"
echo " Results: ${PASS} passed, ${FAIL} failed"
echo "========================================"

if [ "$FAIL" -gt 0 ]; then
  echo "  ⚠️  Some checks failed. Review before considering deploy complete."
  exit 1
else
  echo "  ✅ All checks passed!"
  exit 0
fi
```

---

## 7. Rollback Procedure

Cloud Run keeps revision history. If a deployment breaks something, roll back immediately.

### 7.1 Quick Rollback (Revert to Previous Revision)

```bash
# Step 1: List revisions to find the last working one
gcloud run revisions list --service <service-name> --region us-west1

# Step 2: Route 100% traffic to the previous revision
gcloud run services update-traffic <service-name> \
  --region us-west1 \
  --to-revisions <PREVIOUS_REVISION_NAME>=100
```

### 7.2 Per-App Rollback Commands

```bash
# --- Rollback Project Hypatia Pro ---
gcloud run revisions list --service project-hypatia-pro --region us-west1
# Note the second revision (the last working one)
gcloud run services update-traffic project-hypatia-pro \
  --region us-west1 \
  --to-revisions project-hypatia-pro-00001=100

# --- Rollback PM Accelerator ---
gcloud run revisions list --service project-management-accelerator --region us-west1
gcloud run services update-traffic project-management-accelerator \
  --region us-west1 \
  --to-revisions project-management-accelerator-00001=100

# --- Rollback VibraEngineer ---
gcloud run revisions list --service vibraengineer --region us-west1
gcloud run services update-traffic vibraengineer \
  --region us-west1 \
  --to-revisions vibraengineer-00001=100
```

### 7.3 Gradual Traffic Shift (Canary Rollback)

If you want to test the working revision before shifting all traffic:

```bash
# Send 10% to the new revision, 90% to the known-good one
gcloud run services update-traffic <service-name> \
  --region us-west1 \
  --to-revisions <NEW_REVISION>=10,<GOOD_REVISION>=90

# Monitor for 5 minutes, then shift all traffic if healthy
curl -s <app-url>/api/health   # or equivalent endpoint

# Shift all traffic to the good revision
gcloud run services update-traffic <service-name> \
  --region us-west1 \
  --to-revisions <GOOD_REVISION>=100
```

### 7.4 Verify Rollback

```bash
# After rollback, confirm the active revision
gcloud run services describe <service-name> --region us-west1 \
  --format="value(status.traffic[].revisionName, status.traffic[].percent)"

# Confirm traffic is at 100% on the correct revision
curl -s <app-url>/health-endpoint
```

---

## 8. Troubleshooting

### 8.1 Build Fails: "Could not find package.json"

**Cause:** Deploying from the wrong directory, or `package.json` is missing.

**Fix:**
```bash
cd /home/bob/saas/<correct-directory>/
ls package.json   # Confirm it exists
gcloud run deploy <service-name> --source . --region us-west1 --allow-unauthenticated
```

### 8.2 Build Fails: "npm install" Takes Too Long / Times Out

**Cause:** If `node_modules` is accidentally excluded or deleted, Cloud Build will try to run `npm install`.

**Fix:**
```bash
# Restore node_modules locally (they should be committed in source)
cd /home/bob/saas/<directory>/
ls node_modules/ | head

# If missing, run:
npm install
git add node_modules/   # if applicable
# Then redeploy
```

### 8.3 Deployment Succeeds but App Returns 502 / "Container failed to start"

**Cause:** The app crashes on startup (unhandled exception, missing env var, port binding issue).

**Fix:**
```bash
# Check Cloud Run logs
gcloud logging read \
  "resource.type=cloud_run_revision AND resource.labels.service_name=<service-name>" \
  --limit 50 \
  --format="value(textPayload)"

# Common causes:
# 1. App not listening on PORT env var — all three apps use process.env.PORT
# 2. Missing environment variables  -- add with --set-env-vars
# 3. Port binding to localhost instead of 0.0.0.0 — all three bind to 0.0.0.0
```

### 8.4 App Loads but Shows Blank Page (CDN/esm.sh Resources Not Loading)

**Cause:** The app depends on `esm.sh` CDN for ES modules. If esm.sh is slow or blocked, the page stays blank.

**Fix:**
```bash
# Check if esm.sh is reachable
curl -si https://esm.sh/react@19.2.4 | head -5

# If esm.sh is down or unreachable:
# Option A: Wait for esm.sh to recover (check https://esm.sh)
# Option B: Switch to local bundles (requires code changes + pre-building with vite build)

# Verify CSP headers aren't blocking esm.sh (helmet default CSP may block it)
curl -si <app-url> | grep -i "content-security-policy"
```

> **Note:** As of May 2026, esm.sh loading issues are resolved for all three apps. If issues recur, check https://status.esm.sh.

### 8.5 Cloud Run Returns 401 Unauthorized

**Cause:** Deployed without `--allow-unauthenticated`.

**Fix:**
```bash
# Update the service to allow unauthenticated access
gcloud run services add-iam-policy-binding <service-name> \
  --region us-west1 \
  --member="allUsers" \
  --role="roles/run.invoker"

# Or redeploy with the flag:
gcloud run deploy <service-name> --source . --region us-west1 --allow-unauthenticated
```

### 8.6 Cloud Run Container Crashes on SQLite Write (Permission Denied)

**Cause:** Cloud Run containers have a read-only filesystem except for `/tmp`.

**Fix:**
- **Project Hypatia Pro**: Already configured — uses `/tmp/mifeco.db` in production (line 18 of `server.ts`). ✅
- **VibraEngineer**: Uses `./database.sqlite` — **will crash** on Cloud Run because it tries to write to the container's read-only filesystem.
- **PM Accelerator**: Uses `./database.sqlite` — **same crash risk**.

**For VibraEngineer and PM Accelerator**, the SQLite file path must be updated before deploy:

```ts
// Change from:
filename: './database.sqlite'
// To:
filename: '/tmp/database.sqlite'
```

> ⚠️ **CRITICAL:** VibraEngineer and PM Accelerator will crash on first database write in Cloud Run unless the SQLite path is changed to `/tmp/database.sqlite`. Fix this in `server.ts` before deploying.

### 8.7 VibraEngineer CORS Wildcard Issue (Security)

**Symptom:** `Access-Control-Allow-Origin: *` in response headers.

**Current state:** This is expected — all three apps run `app.use(cors())` without restrictions.

**To fix (before deploy):**
In `/home/bob/saas/VibraEngineer/server.ts` line 19:
```ts
// Replace:
app.use(cors());
// With:
app.use(cors({
  origin: ['https://vibraengineer-845075991286.us-west1.run.app'],
  credentials: true
}));
```

Same fix may be applied to PM Accelerator (line 17 of its `server.ts`).

### 8.8 How to Check Deployed Revisions & Their Status

```bash
# List all revisions across all services
gcloud run revisions list --region us-West1

# Get detailed info on a specific revision
gcloud run revisions describe <revision-name> --region us-west1

# View the latest Cloud Build
gcloud builds list --limit 5

# View a specific build's logs
gcloud builds log <build-id>
```

### 8.9 Deploy Takes Longer Than 10 Minutes

**Cause:** Cloud Build is still running, or the build queue is delayed.

**Fix:**
```bash
# Check active builds
gcloud builds list --filter="status=WORKING"

# If stuck, cancel and retry
gcloud builds cancel <build-id>
```

### 8.10 "Revision not ready to serve" Error

**Cause:** The container health check failed. Cloud Run considers the app unhealthy if the startup probe times out.

**Fix:**
```bash
# Increase the startup probe timeout
gcloud run services update <service-name> \
  --region us-west1 \
  --timeout 600

# Check logs for startup errors
gcloud logging read \
  "resource.type=cloud_run_revision AND resource.labels.service_name=<service-name> AND severity>=ERROR" \
  --limit 20
```

---

## Quick Reference: All Deploy Commands in Sequence

```bash
# ============================================
# MIFECO Full Deploy — Run all 3 in sequence
# Authenticated local machine required
# ============================================

# --- 1. Project Hypatia Pro ---
cd /home/bob/saas/Project_Hypatia_Pro/
gcloud run deploy project-hypatia-pro \
  --source . --region us-west1 --allow-unauthenticated \
  --memory 1Gi --cpu 1 --timeout 300 \
  --set-env-vars "NODE_ENV=production"

# --- 2. PM Accelerator ---
cd /home/bob/saas/Project_Management_Accelerator/
gcloud run deploy project-management-accelerator \
  --source . --region us-west1 --allow-unauthenticated \
  --memory 1Gi --cpu 1 --timeout 300 \
  --set-env-vars "NODE_ENV=production"

# --- 3. VibraEngineer ---
cd /home/bob/saas/VibraEngineer/
gcloud run deploy vibraengineer \
  --source . --region us-west1 --allow-unauthenticated \
  --memory 1Gi --cpu 1 --timeout 300 \
  --set-env-vars "NODE_ENV=production"

echo ""
echo "✅ All three MIFECO apps deployed."
echo "Run the post-deploy verification checklist (Section 6)."
```

---

## Service Summary

| Service | Cloud Run Name | URL | Health endpoint |
|---------|---------------|-----|-----------------|
| Project Hypatia Pro | `project-hypatia-pro` | `https://project-hypatia-pro-1064319572465.us-west1.run.app` | `/api/health` |
| PM Accelerator (HMAP) | `project-management-accelerator` | `https://project-management-accelerator-845075991286.us-west1.run.app` | `/api/projects` |
| VibraEngineer | `vibraengineer` | `https://vibraengineer-845075991286.us-west1.run.app` | `/` |

---

## Known Issues & Action Items

| # | Issue | Affected App(s) | Severity | Action Required |
|---|-------|-----------------|----------|-----------------|
| 1 | CORS wildcard (`Access-Control-Allow-Origin: *`) | VibraEngineer, PM Accelerator | Medium | Restrict origin before next deploy |
| 2 | SQLite writes to read-only filesystem | VibraEngineer, PM Accelerator | **HIGH** | Change path to `/tmp/database.sqlite` in `server.ts` |
| 3 | No dedicated health endpoint | PM Accelerator, VibraEngineer | Low | Add `/api/health` for consistency |
| 4 | CDN dependency on esm.sh | All three | Medium | Monitor esm.sh availability |

---

*Generated: May 30, 2026*
*This runbook is the canonical deployment reference for MIFECO SaaS apps.*
*Do not deploy without this document.*
