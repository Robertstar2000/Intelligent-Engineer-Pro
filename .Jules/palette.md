## 2025-05-18 - Accessibility for Interactive AI Output Controls
**Learning:** Icon-only buttons within interactive document editing surfaces (like AI refinement prompts, version compare, and edit cancels) are frequently rendered without text labels or `aria-label` attributes, rendering them unannounced to assistive technologies.
**Action:** Always verify icon-only buttons in interactive cards have explicit `aria-label` attributes describing their action in context.
