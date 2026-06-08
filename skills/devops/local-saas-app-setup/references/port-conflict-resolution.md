# Port Conflict Resolution Reference

## Default Port Problem

Most Node.js/Express apps hardcode `const PORT = 3000`. When running multiple apps, this causes conflicts.

## Fix Pattern

In each app's `server.ts`, change:
```typescript
// Before:
const PORT = 3000;

// After:
const PORT = Number(process.env.PORT) || 3000;
```

## Standard Port Assignments (MIFECO SaaS)

| App | Default | Assigned |
|-----|---------|----------|
| First app | 3000 | 3001 |
| Second app | 3000 | 3002 |
| Third app | 3000 | 3003 |

## Start Pattern

```bash
cd /path/to/app && PORT=3001 NODE_ENV=production npx tsx server.ts
```

Use Hermes `terminal(background=true)` — NOT shell `&` or nohup — so the agent tracks process lifecycle.
