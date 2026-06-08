# SaaS Tier Structure Reference

## Free vs Pro Feature Flags (per app)

### MIFECO VibraEngineer
| Feature | Free | Pro ($19/mo) |
|---------|------|--------------|
| Max projects | 3 | Unlimited |
| Max phases per project | 5 | Unlimited |
| Automation Engine | ❌ | ✅ |
| Analytics dashboard | ❌ | ✅ |
| Export (PDF/Markdown) | ❌ | ✅ |
| Team collaboration | ❌ | ✅ |

### MIFECO PM Accelerator
| Feature | Free | Pro ($29/mo) |
|---------|------|--------------|
| Max projects | 3 | Unlimited |
| Max phases per project | 5 | Unlimited |
| Automation | ❌ | ✅ |
| Analytics dashboard | ❌ | ✅ |
| Export | ❌ | ✅ |
| Team collaboration | ❌ | ✅ |
| Max team members | 1 | 10 |

### MIFECO Hypatia Pro
| Feature | Free | Pro ($29/mo) |
|---------|------|--------------|
| Max projects | 2 | Unlimited |
| Max experiments per project | 5 | Unlimited |
| AI analysis | ❌ | ✅ |
| Export | Basic | Full |
| Collaboration | ❌ | ✅ |
| Max storage | 100 MB | 5000 MB |

## DB Migration Pattern

Add to each app's `server.ts` in the table creation block:

```sql
ALTER TABLE users ADD COLUMN tier TEXT DEFAULT 'free';
ALTER TABLE users ADD COLUMN stripeCustomerId TEXT;
ALTER TABLE users ADD COLUMN subscriptionStatus TEXT;
ALTER TABLE users ADD COLUMN subscriptionEndsAt TEXT;
```

Use try/catch for idempotent migrations on existing DBs:

```typescript
try {
  await db.exec('ALTER TABLE users ADD COLUMN tier TEXT DEFAULT \'free\'');
} catch (e) { /* column already exists */ }
```

## Client-Side Tier Check Pattern

```typescript
import { Tier, FREE_TIER, PRO_TIER, isPro, canCreateProject } from '../lib/tiers';

const userTier: Tier = user.tier || 'free';
const limits = isPro(userTier) ? PRO_TIER : FREE_TIER;

if (!canCreateProject(userTier, currentProjectCount)) {
  showUpgradeModal();
}
```
