# Standalone Pipeline Kanban Task Board

The `kanban-dashboard.html` is a **focused, standalone kanban board** — no pipeline headers, flow diagrams, product cards, or email sections. Just tabs + columns + task cards.

## Architecture Distinction

| Aspect | Integrated (pipeline-dashboard.html) | Standalone (kanban-dashboard.html) |
|---|---|---|
| **Purpose** | Full pipeline ops center | Pure task-board view |
| **Data source** | `pipeline-state.json` + `unified-pipeline.json` + per-pipeline JSONs | `kanban-data.php` (tasks array with `pipeline` + `stage` fields) |
| **Panel content** | Header + flow SVG + products + email + kanban + stats | **Kanban only** |
| **Lead/task interaction** | Modal overlay on click | Inline expand/collapse on click |
| **Filters** | None (implicit via tab switching) | Assignee dropdown + priority dropdown + search input |
| **Auto-refresh** | No | Yes, 30s interval |

## Data Contract (kanban-data.php)

The PHP endpoint must return JSON in this shape:

```json
{
  "tasks": [
    {
      "id": "BC-042",
      "title": "Build book bible for Smart Biosphere",
      "pipeline": "books-creation",
      "stage": 2,
      "assignee": "Writer",
      "priority": "normal",
      "body": "Detailed description shown on card expand...",
      "created_at": "2026-06-08T14:30:00Z"
    }
  ]
}
```

- **`pipeline`**: one of `books-creation`, `books-marketing`, `saas`, `human-consulting`, `virtual-consulting`
- **`stage`**: integer 1–8 matching the stage index
- **`title`** or **`task`**: display name (fallback chain: `title` → `task` → `'Untitled'`)
- **`assignee`**: string, used for badge color and filtering
- **`priority`**: `'high'` (red), `'normal'` (yellow), `'low'` (gray)
- **`body`** or **`description`**: shown when card is clicked (expand)
- **`created_at`**: ISO timestamp, rendered as relative time ("3h ago", "2d ago")

## Stage Definitions (8 per pipeline)

| Pipeline | Stage 1 | Stage 2 | Stage 3 | Stage 4 | Stage 5 | Stage 6 | Stage 7 | Stage 8 |
|---|---|---|---|---|---|---|---|---|
| Books Creation | Review Market | Build Book Bible | Build Framework | Write | Enrich | Edit | Prep for KDP | Finish |
| Books Marketing | Marketing Content | Infographic | Discovery | Promote | Outreach | Nurture Sequence | Analyze Results | Optimize Campaigns |
| SaaS | Identified | Contacted | Qualified | Process | Demo/Free Trial | Complete Transaction | Followup | Upsell/Cross-sell |
| Human Consulting | Lead | Contact | Qualified | Intent | Strategy Session | Proposal Sent | Negotiation | Closed Won |
| Virtual Consulting | Lead | Contacted | Qualifier | Buy | Process | Deliverables | Edit | Complete Delivery |

## JavaScript Architecture

### Statement of PIPELINE_META (inline, not fetched)

All pipeline metadata (name, icon, description, color, stages) is defined as a static JS constant `PIPELINE_META`. No external JSON fetch needed for stage names.

```javascript
const PIPELINE_META = {
  'books-creation': {
    name: 'Books Creation Pipeline',
    icon: '✍️',
    description: '...',
    color: '#3b82f6',
    bg: 'rgba(59,130,246,0.1)',
    stages: ['Review Market', 'Build Book Bible', 'Build Framework', 'Write',
              'Enrich', 'Edit', 'Prep for KDP', 'Finish']
  },
  // ...4 more pipelines
};
```

### Render Cycle

```
refresh() → fetchTasks() → allTasks = data.tasks
         → renderHeroStats(data)          // per-pipeline count cards
         → update assignee filter options
         → if first load: renderAllPanels() + switchTab('books-creation')
         → else: rerenderCurrentPipeline()
```

### renderAllPanels()
- Loops `PIPELINE_IDS` calling `renderPanel(id)` for each
- Builds all 5 panels at once in `#pipelinePanels`
- First panel gets `.active` class by default

### renderPanel(pipelineId)
Returns HTML for one pipeline panel containing:
1. **Pipeline header** — icon, name, description, total-tasks stat, stages-count stat (left border in pipeline color)
2. **Kanban container** — horizontally scrollable `<div>` with `.kanban-board` containing 8 columns

No flow SVG, no product cards, no email/nurture, no quick stats — kanban only.

### renderColumn(pipelineId, stageNum, stageName, tasks, color)
- Filters `tasks` by `parseInt(t.stage) === stageNum`
- Renders `.kanban-col` with header (stage number + name + count badge) and body (cards or "—")
- Column header bottom border uses `color33` (6-char hex + 20% alpha)

### renderCard(task)
Each task card has:
- Optional `.task-id` (monospace, dim)
- `.task-title` (bold, 0.85rem)
- `.task-meta` row: priority dot + assignee badge + relative date
- Optional `.task-body` (hidden by default, toggled via `toggleBody()`)

### Card Interaction

```javascript
function toggleBody(card) {
  const body = card.querySelector('.task-body');
  if (body) body.classList.toggle('expanded');
}
```

Cards are inline-expandable — no modal. Click anywhere on the card to toggle body visibility.

### Assignee Badge Colors

| Role | CSS Class | Color |
|---|---|---|
| writer | `.task-assignee.writer` | `#60a5fa` (blue) |
| marketing | `.task-assignee.marketing` | `#a78bfa` (purple) |
| sales | `.task-assignee.sales` | `#4ade80` (green) |
| consultant | `.task-assignee.consultant` | `#fb923c` (orange) |
| analyst | `.task-assignee.analyst` | `#22d3ee` (cyan) |
| default | `.task-assignee` | `#00ffcc` (accent) |

Badge class is derived from `task.assignee.toLowerCase()`.

### Filters

Three independent filters applied to cards in the *currently visible panel only*:

- **Assignee dropdown** — populated dynamically from `allTasks` after each refresh
- **Priority dropdown** — static options: All / High / Normal / Low
- **Search input** — matches against `data-search` attribute (title + assignee + id, lowercased)

Filter function: `applyFilters()` — loops `.task-card` in `#panel-{currentPipeline}` and toggles `display: none`.

Column count badges show **total** cards in column (not filtered count — preserves column context).

### Tab Switching

```javascript
function switchTab(pipelineId) {
  currentPipeline = pipelineId;
  // Toggle .active on tab buttons (by data-tab)
  // Toggle .active on sidebar nav links (by text content match)
  // Toggle .active on pipeline panels (by id === `panel-${pipelineId}`)
  applyFilters();  // reapply filters to newly visible panel
}
```

### Auto-Refresh

```javascript
refreshInterval = setInterval(refresh, 30000);
```

The refresh timer label is updated to "Auto-refresh: 30s" after each refresh round.

## CSS Layout

### Kanban Columns

- `.kanban-col`: min-width 260px, max-width 260px (responsive: 220px at ≤900px viewport)
- `.kanban-container`: `overflow-x: auto` — enables horizontal scroll for the full 8-column board
- `.kanban-board`: `display: flex`, `gap: 1rem`, `align-items: flex-start`

### Task Cards

- `.task-card`: `cursor: pointer`, hover lifts up (translateY(-1px) + accent border glow)
- `.task-body`: `display: none` by default, `.expanded` → `display: block` with max-height 120px + scroll
- `.task-priority.priority-high`: `#ef4444` (red, was `danger`)
- `.task-priority.priority-normal`: `#f59e0b` (yellow, was `warning`)
- `.task-priority.priority-low`: `#94a3b8` (gray, was `text-secondary`)

### Color Scheme

Same dark theme as all MIFECO dashboards (`--bg-primary: #0f172a`, `--accent: #00ffcc`). Pipeline-specific accent colors used for:
- Tab indicator bars
- Pipeline header left border
- Stat number in hero stats
- Column header bottom border (at 20% opacity)

## Differences from Integrated Pipeline Dashboard Kanban

1. **`PIPELINE_META`** is a static JS constant with stages defined inline — no `pipeline-state.json` or `unified-pipeline.json` dependency
2. **No `currentStage` / `isActive` / `isDone`** concept — all 8 columns render identically regardless of pipeline progress
3. **No lead detail modal** — body text is inline in the card, toggled by click
4. **Filters** (assignee, priority, search) filter cards in real-time — the integrated dashboard has no such controls
5. **Auto-refresh** at 30s — integrated dashboard is manually refreshed
6. **Single data source** (`kanban-data.php`) — integrated dashboard fetches 5 separate JSON files
7. **Sidebar links** include cross-links to pipeline-dashboard.html, content-command-center.html, outreach-dashboard.html, hermes-dashboard.html, and index.html — must keep in sync with other dashboards