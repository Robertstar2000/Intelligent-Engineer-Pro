---
name: cloudflare-worker-proxy
description: Deploy a Cloudflare Worker as reverse proxy to route mifeco.com/<service>/* to Google Cloud Run backends by URL path prefix. Use when setting up SaaS subpaths on mifeco.com without custom domain mapping on Cloud Run.
---

# Cloudflare Worker → Cloud Run Proxy Architecture

## When to Use

Use this pattern when:
- SaaS backends are on Cloud Run (random `*.run.app` URLs)
- You want clean URLs like `mifeco.com/<service>/*` instead of `*.run.app`
- You want to avoid Cloud Run's complex custom domain mapping + certificate provisioning
- Cloudflare already manages the domain DNS

## Architecture

```
User → mifeco.com/vibraengineer/*   → Cloudflare Worker → vibraengineer.run.app
User → mifeco.com/accelerator/*     → Cloudflare Worker → pm-accelerator.run.app
User → mifeco.com/hypatia/*         → Cloudflare Worker → hypatia-pro.run.app
```

## Benefits

- **No DNS changes** — Worker routes by path, not hostname
- **No Cloud Run domain mapping** — avoids certificate provisioning (15-30 min wait)
- **Single SSL cert** — Cloudflare handles SSL for mifeco.com
- **Works immediately** — no DNS propagation wait
- **Free** — Workers free tier = 100K requests/day

## Worker Implementation

Create `~/cloudflare-workers/mifeco-saas-proxy/src/index.js`:

```js
const SERVICES = {
  vibraengineer: 'https://vibraengineer-845075991286.us-west1.run.app',
  accelerator:   'https://project-management-accelerator-845075991286.us-west1.run.app',
  hypatia:       'https://project-hypatia-pro-1064319572465.us-west1.run.app',
};
const ROUTES = [
  { prefix: '/vibraengineer', service: 'vibraengineer' },
  { prefix: '/accelerator',   service: 'accelerator' },
  { prefix: '/hypatia',       service: 'hypatia' },
];

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const pathname = url.pathname;

    let matchedRoute = null;
    for (const route of ROUTES) {
      if (pathname === route.prefix || pathname.startsWith(route.prefix + '/')) {
        matchedRoute = route;
        break;
      }
    }

    if (!matchedRoute) {
      return new Response(JSON.stringify({ error: 'Not Found', path: pathname }),
        { status: 404, headers: { 'Content-Type': 'application/json' } });
    }

    const serviceUrl = SERVICES[matchedRoute.service];
    const targetUrl = new URL(serviceUrl);
    targetUrl.pathname = pathname;
    targetUrl.search = url.search;

    const modifiedRequest = new Request(targetUrl, {
      method: request.method,
      headers: {
        ...Object.fromEntries(request.headers),
        'Host': new URL(serviceUrl).host,
        'X-Forwarded-Host': url.host,
        'X-Mifeco-Service': matchedRoute.service,
      },
      body: request.body,
      redirect: 'follow',
    });

    const response = await fetch(modifiedRequest);
    const modifiedResponse = new Response(response.body, response);
    modifiedResponse.headers.set('X-Served-By', 'cloudflare-worker-mifeco');
    return modifiedResponse;
  },
};
```

Create `wrangler.jsonc`:

```jsonc
{
  "name": "mifeco-saas-proxy",
  "main": "src/index.js",
  "compatibility_date": "2026-06-07",
  "routes": [
    { "pattern": "mifeco.com/vibraengineer/*", "zone_name": "mifeco.com" },
    { "pattern": "mifeco.com/accelerator/*", "zone_name": "mifeco.com" },
    { "pattern": "mifeco.com/hypatia/*", "zone_name": "mifeco.com" }
  ]
}
```

## Deployment

```bash
npm install -g wrangler
wrangler login
cd ~/cloudflare-workers/mifeco-saas-proxy
wrangler deploy
```

## App-Side Requirements

Each Cloud Run app behind the proxy **must**:

1. **CORS** — Restrict to `mifeco.com`, not wide-open:
   ```js
   app.use(cors({
     origin: ['https://mifeco.com', 'https://www.mifeco.com', 'http://localhost:PORT'],
     credentials: true,
   }));
   ```
2. **Vite base path** — Set `base: '/<prefix>/'` in `vite.config.ts`
3. **Health endpoint** — `GET /api/health` returning `{ status: 'ok' }`
4. **PORT env var** — `const PORT = Number(process.env.PORT) || 3000`

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Worker 404 | Path doesn't match route prefix | Check URL format |
| CORS error | `cors()` too restrictive | Add `https://mifeco.com` |
| Assets 404 | Vite base path not set | Add `base: '/<prefix>/'` |
| Worker 502 | Cloud Run down | Check `<service>.run.app/api/health` |

## Hosting Decision Matrix for MIFECO SaaS

| Option | Recommendation | Reason |
|---|---|---|
| **Cloudflare Worker + Cloud Run** | ✅ Current best | Free, fast, no DNS changes |
| **Cloud Run standalone** | ❌ Rejected by Bob | URLs are random `*.run.app` |
| **DreamHost shared** | ❌ Impossible | Does NOT support Node.js |
| **VPS (Hetzner/DO)** | ⏳ Next step | When revenue justifies €5-10/mo |
