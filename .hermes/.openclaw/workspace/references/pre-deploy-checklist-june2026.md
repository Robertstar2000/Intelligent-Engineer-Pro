# Pre-Deployment Checklist — MIFECO SaaS Apps
> Created: 2026-06-03 by CEO Agent (saas-ops task CEO-executed)
> Purpose: Step-by-step checklist for Bob to deploy all 3 SaaS apps with security headers + SQLite fixes

---

## Prerequisites

- [ ] Install gcloud CLI: https://cloud.google.com/sdk/docs/install
- [ ] Authenticate: `gcloud auth login`
- [ ] Set project: `gcloud config set project <YOUR_PROJECT_ID>`
- [ ] Verify: `gcloud projects list`

---

## Fix 1: SQLite Path (PM Accelerator + VibraEngineer)

### Before deploying, fix the SQLite path in source code:

**PM Accelerator:**
```bash
cd /home/bob/saas/Project_Management_Accelerator
# Change "./database.sqlite" to "/tmp/database.sqlite"
sed -i 's|"./database.sqlite"|"/tmp/database.sqlite"|g' server.ts
grep "database.sqlite" server.ts  # Verify fix
```

**VibraEngineer:**
```bash
cd /home/bob/saas/VibraEngineer
# Change './database.sqlite' to '/tmp/database.sqlite'
sed -i "s|'./database.sqlite'|'/tmp/database.sqlite'|g" server.ts
grep "database.sqlite" server.ts  # Verify fix
```

> **Why:** Cloud Run filesystem is read-only except `/tmp`. Writing to `./database.sqlite` will crash the app on first DB write.

---

## Fix 2: Security Headers (All 3 Apps)

Verify helmet.js is present in all 3 apps:
```bash
grep -r "helmet" /home/bob/saas/Project_Hypatia_Pro/server.ts
grep -r "helmet" /home/bob/saas/Project_Management_Accelerator/server.ts
grep -r "helmet" /home/bob/saas/VibraEngineer/server.ts
```

Expected: `import helmet from 'helmet'` and `app.use(helmet())` in each.

**This fix has been in source code since May 7, 2026 (27 days undeployed).**

---

## Deployment Commands

### 1. Deploy Project Hypatia Pro
```bash
cd /home/bob/saas/Project_Hypatia_Pro
gcloud run deploy project-hypatia-pro \
  --source . \
  --region us-west1 \
  --platform managed \
  --allow-unauthenticated \
  --memory 512Mi \
  --timeout 300
```

### 2. Deploy PM Accelerator (with SQLite fix)
```bash
cd /home/bob/saas/Project_Management_Accelerator
gcloud run deploy project-management-accelerator \
  --source . \
  --region us-west1 \
  --platform managed \
  --allow-unauthenticated \
  --memory 512Mi \
  --timeout 300
```

### 3. Deploy VibraEngineer (with SQLite fix)
```bash
cd /home/bob/saas/VibraEngineer
gcloud run deploy vibraengineer \
  --source . \
  --region us-west1 \
  --platform managed \
  --allow-unauthenticated \
  --memory 512Mi \
  --timeout 300
```

---

## Post-Deployment Verification

### Check security headers (run from any machine with curl):
```bash
curl -I https://project-hypatia-pro-1064319572465.us-west1.run.app | grep -i "x-frame-options\|content-security-policy\|strict-transport-security\|x-content-type-options\|x-xss-protection\|referrer-policy"

curl -I https://project-management-accelerator-845075991286.us-west1.run.app | grep -i "x-frame-options\|content-security-policy\|strict-transport-security"

curl -I https://vibraengineer-845075991286.us-west1.run.app | grep -i "x-frame-options\|content-security-policy\|strict-transport-security"
```

Expected headers: `X-Frame-Options`, `Content-Security-Policy`, `Strict-Transport-Security`, `X-Content-Type-Options`, `X-XSS-Protection`, `Referrer-Policy`

### Check apps load correctly:
- https://project-hypatia-pro-1064319572465.us-west1.run.app
- https://project-management-accelerator-845075991286.us-west1.run.app
- https://vibraengineer-845075991286.us-west1.run.app

---

## Rollback Procedure

If deployment fails or causes issues:
```bash
# List revisions
gcloud run revisions list --service <SERVICE_NAME> --region us-west1

# Rollback to previous revision
gcloud run services update-traffic <SERVICE_NAME> \
  --to-revisions <PREVIOUS_REVISION>=100 \
  --region us-west1
```

---

## Full Deployment Runbook

For detailed troubleshooting, see: `references/deployment-runbook-may2026.md`
