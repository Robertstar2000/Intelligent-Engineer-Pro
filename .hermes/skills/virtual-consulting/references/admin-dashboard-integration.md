# Virtual Consulting — Admin Dashboard Integration

## Admin Dashboard Tabs

The MIFECO admin dashboard (`mifeco.com/admin/`) includes a tab linking to the Virtual Consulting pipeline:

- **💬 Consult** → `/consult` (opens in new tab)

This is configured in the admin sidebar nav at `/home/dh_mwpxuu/mifeco.com/admin/index.html`.

## Related Pages

| Page | URL | Description |
|------|-----|-------------|
| Admin Dashboard | `/admin/` | Pipeline Command Center with tabs |
| Jarvis | `/jarvis` | AI Assistant interface |
| Consulting | `/consult` | Virtual Consulting landing + flow |
| Books | `/books` | Author book site |

## Main Site Links

On the main mifeco.com React SPA, all Virtual Consulting references link to `/consult`:
- Nav: "Virtual Consulting" → `/consult`
- Hero: "Business Assessment — $199" → `/consult`
- Products cards: Virtual Consulting card → `/consult`
- Footer: "Virtual Consulting" → `/consult`

See `mifeco-website-deployment` skill for details on modifying the React SPA bundle.
