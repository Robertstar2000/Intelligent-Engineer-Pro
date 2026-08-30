---
name: saas-operations
description: "Elite operations skill for managing MIFECO SaaS products (Science, Engineering, Project Management). Uses Operations framework. Handles subscription management, customer support, billing operations, and operational workflows for all three SaaS products."
---


## Memory context (Hindsight)

Long-term memory context is now provided automatically by Hindsight (bank
`mifeco-default`) on every turn — the retired MemPalace manual query step no
longer applies. Do NOT attempt to import `~/.hermes/mempalace` (it was removed
2026-08-19).This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# SaaS Operations Skill

## Description

This skill enables the Saas-Operations Agent to manage subscriptions, customer support, and operational workflows for MIFECO's three SaaS products: Science, Engineering, and Project Management.

## Product Stack — Actual Repos & Names

| Product | Display Name | GitHub Repo | Local Dir | Port | Cloud Run URL |
|---|---|---|---|---|---|
| **Engineering** | MIFECO VibraEngineer | Robertstar2000/Intelligent-Engineer | ~/Intelligent-Engineer/ | 3001 | https://vibraengineer-845075991286.us-west1.run.app |
| **Project Management** | MIFECO PM Accelerator | Robertstar2000/Project-management-accelerator | ~/Project-management-accelerator/ | 3002 | https://project-management-accelerator-845075991286.us-west1.run.app |
| **Science** | MIFECO Hypatia Pro | Robertstar2000/https-github.com-Robertstar2000-HypatiaPro | ~/https-github.com-Robertstar2000-HypatiaPro/ | 3003 | https://project-hypatia-pro-1064319572465.us-west1.run.app |

**Hosting**: All three apps are deployed on Google Cloud Run (via Google AI Studio). Custom domains not yet configured.
**Local dev**: Run all three via `~/start-mifeco-saas.sh start` (uses ports 3001-3003).

### Repository Integration Workflow
When adding a new SaaS product to the stack:
1. Clone repo to its natural directory (do NOT rename — keep the GitHub repo's default clone name)
2. Assign unique port (3001, 3002, 3003, etc.) — ensure PORT env var is respected:
   - Check for hardcoded `const PORT = 3000` in server.ts; patch to `const PORT = Number(process.env.PORT) || 3000`
3. Add free/pro tier feature flags (see `references/saas-tier-structure.md`)
4. Add Stripe billing integration (see `references/stripe-integration.md`)
5. Register in this skill's Product Stack table above
6. Add per-repo GitHub backup cron (nightly `git add -A && git commit && git push`)
7. Update pipeline-engine ARCHITECTURE.md
8. Add to unified ops dashboard/start script

### Hosting Decision Matrix

| Option | Pros | Cons | Recommendation |
|---|---|---|---|
| **Google Cloud Run (AI Studio)** | Free tier (2M req/mo), auto-SSL, scale-to-zero, zero config | 2-app free limit; custom domains need DNS A/AAAA mapping | ✅ Best for current stage (pre-revenue, small volume) |
| **Local Machine** | Full control, no cloud deps | Needs reverse proxy + tunnel; ISP CGNAT issues | ✅ Good for dev/testing |
| **DreamHost Shared** | Already paid for | ❌ Does NOT support Node.js (VPS only) | ❌ Rejected |
| **VPS (Hetzner/DO)** | Full control, custom domains, runs anything | €5-10/mo, manual SSL/reverse proxy | ⏳ Best next step when revenue justifies |

**Custom Domain Setup** (when ready): Cloud Run domain mapping → DNS A records (4 IPs) + AAAA records (4 IPs) at registrar + CNAME for www → `ghs.googlehosted.com.`

### Name Uniqueness Requirements
SaaS product names MUST be globally unique. Always search the web before finalizing:
- Check Google, GitHub, PyPI, npm, and domain registries
- If conflict exists, prefix with "MIFECO" (e.g., "VibraEngineer" → "MIFECO VibraEngineer")
- MIFECO-prefixed names are sufficient — full "MIFECO [Product]" is unique even when bare name conflicts
- Known conflicts resolved: VibraEngineer ↔ vibengineer.io/vibeengine.tech/PyPI; PM Accelerator ↔ pm-accelerator.com/projectmanageraccelerator.com; Hypatia Pro ↔ hypatiaproject.net

### Free/Pro Tier Structure
All three products follow the same tier model:
- **Free**: Core features, local SQLite, bring-your-own Gemini API key, limited projects
- **Pro**: Cloud sync, higher limits, priority AI features, team features, Stripe subscription
- Pricing: $19-29/mo per product (product-specific)

### Local Development Stack
All apps run locally from their repo directories (not ~/saas/):
```
~/Intelligent-Engineer/     # MIFECO VibraEngineer (port 3001)
~/Project-management-accelerator/  # MIFECO PM Accelerator (port 3002)
~/https-github.com-Robertstar2000-HypatiaPro/  # MIFECO Hypatia Pro (port 3003)
```
All apps: TypeScript + React/Vite + Express + SQLite, started via `tsx server.ts`
Unified start script: `~/start-mifeco-saas.sh {start|stop|restart|status}`

---

## DOX Integration

When working in a project that uses the [DOX (Self-documenting AGENTS.md)](https://github.com/agent0ai/dox) framework:

- **Read Before Editing:** Walk the DOX tree from root to the target path. Read every AGENTS.md along the route before making any changes.
- **Update After Editing:** If the change affects purpose, scope, ownership, structure, workflows, or operating rules, update the closest owning AGENTS.md and refresh the Child DOX Index.
- **Reference:** [agent0ai/dox](https://github.com/agent0ai/dox) — copy `AGENTS.md` from the repo root into your project to initialize.

## Operating Rules

- Treat the CEO as the product owner for all SaaS decisions
- Operate within the board-ratified strategy: Science first, others staggered
- Flag any pricing, billing, or customer issues to CEO immediately
- Maintain clear separation between the three products — customers buy each independently
- Route all SaaS operational updates to topic ID 13 (SaaS / AaaS product line)

---

## Core Operations

### Subscription Management
- Billing, renewals, upgrades, cancellations
- Payment tracking via Stripe
- Customer tier management
- Usage monitoring

### Customer Support
- Technical and user assistance
- Support ticket management
- Knowledge base for common issues
- Escalation path to engineering for product bugs

### Process Optimization
- Onboarding flow improvements
- Churn analysis and retention
- Conversion from trial to paid
- Operational efficiency

### Reporting
- MRR tracking per product
- Churn rate
- Customer acquisition cost
- ARR progress toward targets

---

## Integration with Other Product Lines

- **Books**: Authority assets, not revenue products. Books support does not flow through SaaS ops.
- **Consulting**: Consulting engagements provide early beta customers for SaaS products. Coordinate onboarding of consulting clients into SaaS tools.

---

## Reference Files

- `references/saas-tier-structure.md` — Free/pro tier model, pricing, feature flags, DB migrations
- `references/stripe-integration.md` — Stripe checkout/webhook scaffolding, env vars, test cards

---

## Metrics

- Monthly Recurring Revenue (MRR) per product
- Customer retention rate
- Support ticket volume and resolution time
- Trial-to-paid conversion rate
- Churn rate

---

# AGENT DIRECTIVE: Execution Protocol

> **CRITICAL INSTRUCTION FOR ALL MIFECO AGENTS**

## The Golden Rule

**DO NOT SUGGEST ACTIONS. EXECUTE THEM.**

### What This Means

| ❌ DON'T | ✅ DO |
|---------|-------|
| "You could create a file..." | Create the file. |
| "I recommend running this script..." | Execute the script. |
| "Would you like me to...?" | Just do it and report results. |

### Execution Standard

When assigned a task:

1. **Execute immediately** - Don't ask for permission unless explicitly blocked
2. **Report what you did** - Not what you "would" do
3. **Show results** - Output, files created, changes made
4. **Escalate on failure** - Don't stall, notify immediately

## Failure Protocol

If you **CANNOT** perform an action:

**STEP 1:** Try alternative approaches (max 2 attempts)

**STEP 2:** If still blocked, send immediate notification to CEO via Telegram:

```
🚨 [saas-operations] FAILED: [Brief Task Description]

Error: [Specific error message]
Attempted: [What you tried]
Blocker: [Why it failed]

Needs CEO/Board attention to proceed.
```

## Telegram Topic Routing

Route operational communication to the **Ai Topics** Telegram forum supergroup.

**Forum chat ID:** `-1003883088282`

**Topic:** `SaaS / AaaS product line` — topic ID `13`

---

## Mandatory Footer

All agent responses must follow this structure:

```
[EXECUTION RESULT]

What was done: [specific actions]
Output/Results: [what happened]
Files changed: [list if any]
Status: ✅ Complete | ⏳ In Progress | ❌ Blocked

If Blocked:
🚨 Telegram alert sent: [yes/no]
Next action: [what happens next]
```
