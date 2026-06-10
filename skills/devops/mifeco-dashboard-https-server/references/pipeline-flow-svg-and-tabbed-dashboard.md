# Pipeline Flow SVG & Tabbed Dashboard Patterns

## Part A: 8-Stage Pipeline Flow SVGs

Each pipeline gets a static SVG in `~/.hermes/pipeline-engine/dashboard/flows/<pipeline-id>.svg`.

### SVG Template

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1050 50" width="100%" height="50">
  <defs>
    <style>
      .stage-box { fill: #1a2332; stroke: #334155; stroke-width: 1.2; rx: 6; }
      .stage-text { fill: #e2e8f0; font-family: 'Inter', -apple-system, sans-serif; font-size: 11px; text-anchor: middle; dominant-baseline: central; }
      .stage-active { fill: <COLOR>22; stroke: <COLOR>; stroke-width: 1.5; rx: 6; }
      .arrow-line { stroke: <COLOR>; stroke-width: 1.5; fill: none; }
      .arrow-head { fill: <COLOR>; }
    </style>
    <marker id="arrow" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" class="arrow-head"/>
    </marker>
  </defs>
  <!-- 7 arrow connectors between 8 stages -->
  <line x1="125" y1="25" x2="140" y2="25" class="arrow-line" marker-end="url(#arrow)"/>
  <line x1="240" y1="25" x2="255" y2="25" class="arrow-line" marker-end="url(#arrow)"/>
  <line x1="355" y1="25" x2="370" y2="25" class="arrow-line" marker-end="url(#arrow)"/>
  <line x1="470" y1="25" x2="485" y2="25" class="arrow-line" marker-end="url(#arrow)"/>
  <line x1="585" y1="25" x2="600" y2="25" class="arrow-line" marker-end="url(#arrow)"/>
  <line x1="700" y1="25" x2="715" y2="25" class="arrow-line" marker-end="url(#arrow)"/>
  <line x1="815" y1="25" x2="830" y2="25" class="arrow-line" marker-end="url(#arrow)"/>
  <!-- 8 stage boxes: first is .stage-active, rest .stage-box -->
  <rect x="25" y="11" width="100" height="28" class="stage-active"/>
  <rect x="140" y="11" width="100" height="28" class="stage-box"/>
  <rect x="255" y="11" width="100" height="28" class="stage-box"/>
  <rect x="370" y="11" width="100" height="28" class="stage-box"/>
  <rect x="485" y="11" width="100" height="28" class="stage-box"/>
  <rect x="600" y="11" width="100" height="28" class="stage-box"/>
  <rect x="715" y="11" width="100" height="28" class="stage-box"/>
  <rect x="830" y="11" width="100" height="28" class="stage-box"/>
  <!-- 8 text labels -->
  <text x="75" y="25" class="stage-text">Stage 1</text>
  <text x="190" y="25" class="stage-text">Stage 2</text>
  <text x="305" y="25" class="stage-text">Stage 3</text>
  <text x="420" y="25" class="stage-text">Stage 4</text>
  <text x="535" y="25" class="stage-text">Stage 5</text>
  <text x="650" y="25" class="stage-text">Stage 6</text>
  <text x="765" y="25" class="stage-text">Stage 7</text>
  <text x="880" y="25" class="stage-text">Stage 8</text>
</svg>
```

### Dimensions Reference

| Element | X Position |
|---------|-----------|
| Stage 1 box | 25 |
| Arrow 1 → | 125 → 140 |
| Stage 2 box | 140 |
| Arrow 2 → | 240 → 255 |
| Stage 3 box | 255 |
| Arrow 3 → | 355 → 370 |
| Stage 4 box | 370 |
| Arrow 4 → | 470 → 485 |
| Stage 5 box | 485 |
| Arrow 5 → | 585 → 600 |
| Stage 6 box | 600 |
| Arrow 6 → | 700 → 715 |
| Stage 7 box | 715 |
| Arrow 7 → | 815 → 830 |
| Stage 8 box | 830 |

- **Box**: 100×28px, rx=6, y=11
- **Text anchor X**: box X + 50 (center of box)
- **Arrow origin X**: box X + 100 (right edge of box)
- **Arrow target X**: next box X (140, 255, 370, 485, 600, 715, 830)
- **Arrow Y**: 25 (center of box height)
- **Text Y**: 25

### Per-Pipeline Colors

| Pipeline ID | Color | Hex |
|-------------|-------|-----|
| books-creation | Blue | `#3b82f6` |
| books-marketing | Purple | `#8b5cf6` |
| saas | Green | `#22c55e` |
| human-consulting | Orange | `#f97316` |
| virtual-consulting | Cyan | `#06b6d4` |

---

## Part B: Tabbed Kanban Dashboard

The `pipeline-dashboard.html` is a data-driven, multi-tab dashboard for 5 product pipelines.

### Architecture

```
Layer 1: Static HTML/CSS — sidebar, tabs, panel placeholders, modal overlays
Layer 2: JS Data — loaded via fetch() from JSON files on page load
Layer 3: JS Renders — functions that generate HTML for each panel section
```

### Data Source Loading Pattern

```javascript
async function loadAllData() {
  const [unified, state, books, saas, consulting] = await Promise.all([
    fetch('unified-pipeline.json').then(r => r.ok ? r.json() : null),
    fetch('pipeline-state.json').then(r => r.ok ? r.json() : null),
    fetch('pipeline-books.json').then(r => r.ok ? r.json() : null),
    fetch('pipeline-saas.json').then(r => r.ok ? r.json() : null),
    fetch('pipeline-consulting.json').then(r => r.ok ? r.json() : null),
  ]);
  // Store globally, then render
}
```

### Panel Sections (in order)

Each pipeline panel contains:

1. **Pipeline Header** — icon, name, description, health dot, status label, last run, stage progress %, total/active/queued counts (cards). Styled with a left border in the pipeline's color.
2. **Flow Diagram** — section with title "📐 Pipeline Flow — 8 Stages" and an `<img>` tag pointing to `flows/<pipeline-id>.svg`.
3. **Products/Services** — grid of cards showing name, price, description, and (for books) a list of titles. Left border in pipeline color.
4. **Email & Nurture** — two-column layout with inbox address (monospace, colored) and nurture sequence description. Left border in pipeline color.
5. **Kanban Board** — horizontally scrollable board with 8 columns (one per stage). Each column shows stage number+name, lead count badge, and lead cards. Active stage column has colored border/header. Completed stages are dimmed.
6. **Quick Stats** — grid of stat cards showing per-stage item counts plus totals.

### Kanban Column Pattern

```javascript
function renderKanbanCol(pipelineId, stage, idx, currentStage, color) {
  const isActive = (idx+1) === currentStage;
  const isDone = (idx+1) < currentStage;
  // Query leads for this pipeline+stage
  let leads = getLeadsForStage(pipelineId, idx+1);
  return `<div class="kanban-col ${isActive ? 'kc-active' : ''} ${isDone ? 'kc-done' : ''}">...</div>`;
}
```

### Lead Card Pattern

Lead data shapes differ across JSON files. The render function adapts via fallback chain:

```javascript
const name = lead.contact_name || lead.name || (lead.contact?.name) || 'Unknown';
const company = lead.company_name || lead.company || (lead.contact?.organization) || '';
const value = lead.value_estimate || lead.value || 0;
```

Each lead card is clickable and opens a detail modal showing contact info, value, stage, source, and notes.

### Tab Switching

```javascript
function switchTab(tabId) {
  // 1. Toggle .active on tab buttons (by data-tab attribute)
  // 2. Toggle .active on pipeline panels (by data-pipeline attribute)
  // 3. Toggle .active on sidebar nav links (by onclick string match)
}
```

### Pipeline Color Map (JS)

Used consistently across all sections — header borders, active stage highlights, stat numbers, email addresses:

```javascript
const PIPELINE_COLORS = {
  'books-creation': { primary: '#3b82f6', bg: 'rgba(59,130,246,0.1)' },
  'books-marketing': { primary: '#8b5cf6', bg: 'rgba(139,92,246,0.1)' },
  'saas': { primary: '#22c55e', bg: 'rgba(34,197,94,0.1)' },
  'human-consulting': { primary: '#f97316', bg: 'rgba(249,115,22,0.1)' },
  'virtual-consulting': { primary: '#06b6d4', bg: 'rgba(6,182,212,0.1)' }
};
```

### CSS Layout Foundations

- **Sidebar**: Fixed 220px, dark background, nav links with left-border active indicator
- **Main**: margin-left: 220px, max-width 1500px container
- **Tabs**: flex row in a card, 5 tab buttons with colored indicator bars
- **Kanban**: overflow-x: auto on wrapper, flex row with min-width columns (200-220px each)
- **Stat grids**: CSS grid with auto-fill/minmax responsive columns
- **Color theme**: Dark (#0f172a base), accent (#00ffcc), pipeline-specific accent colors

### Pitfalls

- **Lead data shapes differ** — books leads have `current_stage` (number), SaaS leads have `stage` (number), consulting leads have `stage` (number). Use the `getBooksLeadsForStage()`/`getSaaSLeadsForStage()`/`getConsultingLeadsForStage()` wrapper functions to normalize.
- **unified-pipeline.json** has `stages` as array of `{id, name, description}` objects. pipeline-state.json has `stages` as flat string arrays. The kanban uses `stage.name` from unified or falls back to the string directly.
- **Products vs Services**: unified-pipeline.json uses `products` for books/saas and `services` for consulting. The render must check which exists.
- **Nurture can be null**: some pipelines have `nurture: null` — guard against this in render.
- **flowFile** in pipeline-state.json references `flows/<pipeline-id>.svg` — the HTML embeds the SVG as an `<img>` tag, not inline.
- **Tab panels are hidden/shown via CSS display toggle** — only one panel visible at a time. Use `display: none` / `display: block` with CSS class `.active`.
- **Sidebar nav links use onclick attributes** (`switchTab('id')`), not href hashes. Scroll-based active detection is replaced by explicit tab switching.