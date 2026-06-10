# Pipeline Data API — Server-Side Endpoints

The HTTPS server (`dashboard/https-server.py`) serves both static dashboard files AND a JSON API for lead advancement and mock inbox operations. Import: `from pipeline_data_api import handle_request`.

## Endpoints

### `POST /api/advance-lead`

Advances a lead from Stage 1 ("Lead Inbox"/"Identified"/"lead") to Stage 2 ("Contacted"/"contacted") in the per-product pipeline JSON file. Also handles email routing based on mode.

**Request:**
```json
{
  "pipeline": "books|saas|consulting",
  "lead_name": "Sarah Chen",
  "mode": "test|production",
  "email": "schen@example.com",
  "subject": "[Books] Following up",
  "body": "Hi Sarah..."
}
```

**Response (test mode):**
```json
{
  "success": true,
  "message": "Lead advanced + email written to mock inbox. Lead 'Sarah Chen' advanced to 'Contacted' in books pipeline",
  "mode": "test"
}
```

**Response (production mode):**
```json
{
  "success": true,
  "message": "Lead advanced + email sent. Lead 'Sarah Chen' advanced to 'Contacted' in books pipeline",
  "mode": "production"
}
```

**How it works:**
1. Loads the appropriate `pipeline-{product}.json` file
2. Finds the lead by name/company match (case-insensitive substring)
3. Sets `current_stage` → 2, `current_stage_name` → "Contacted" and related timestamps
4. In test mode: writes email to `data/mock-inbox.json`
5. In production mode: POSTs to `https://mifeco.com/wp-json/mifeco/v1/send-email` with `secret: "Rm2214ri%%%%"`

### `POST /api/mock-inbox`

Returns all mock inbox emails (test mode only).

**Request:** `{}`

**Response:**
```json
{
  "success": true,
  "items": [
    {
      "id": "mock-1",
      "sent_at": "2026-05-14T16:38:10Z",
      "pipeline": "books",
      "to_name": "Sarah Chen",
      "to_email": "schen@example.com",
      "subject": "...",
      "body": "...",
      "mode": "test"
    }
  ]
}
```

### `POST /api/clear-mock-inbox`

Clears all entries from the mock inbox. Returns `{"success": true, "message": "Mock inbox cleared"}`.

## Stage Advancement Details (v2 — 5 Product Pipelines)

Each product pipeline has different field names for stage tracking:

| Pipeline | Stage 1 | Stage 2 | ID field | Stage field |
|----------|---------|---------|----------|-------------|
| books-marketing | "Marketing Content" (id=1) | "Infographic" (id=2) | `id` (e.g. "B-001") | `current_stage` / `current_stage_name` |
| saas | "Identified" (id=1) | "Contacted" (id=2) | `id` (e.g. "S-001") | `stage` |
| human-consulting | "Lead" (id=1) | "Contact" (id=2) | `id` (e.g. "C-001") | `stage` / `status` |
| virtual-consulting | "Lead" (id=1) | "Contacted" (id=2) | `id` (e.g. "C-0xx") | `stage` / `status` |

**Note:** books-creation pipeline (manuscript production) does NOT use lead advancement — it tracks manuscript progress through writing stages via filesystem scans, not API calls.

The API matches leads by name/company (substring), not by pipeline-specific ID, since the outreach dashboard uses a separate LEADS array.

## HTTPS Server Handler

The `https-server.py` `DashboardHandler` class replaces the previous `SimpleHTTPRequestHandler`:

- `do_GET` — Serves static HTML/CSS/JS/images from `dashboard/` with security (no directory traversal)
- `do_POST` — Routes `/api/*` paths to `pipeline_data_api.handle_request()`
- `do_OPTIONS` — CORS preflight (allows cross-origin from dashboard)
- Static fallback: 301 HTTP → HTTPS redirect on port 5540

## Dashboard Integration

The `outreach-dashboard.html` calls these endpoints via `fetch()`:

- Mode toggle buttons call `setMode('test'|'production')`
- Send button calls `POST /api/advance-lead` with lead data
- Mock inbox panel calls `POST /api/mock-inbox` on load and after each send
- Clear button calls `POST /api/clear-mock-inbox`
