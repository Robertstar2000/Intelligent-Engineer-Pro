## 2025-05-18 - Accessibility for Interactive AI Output Controls
**Learning:** Icon-only buttons within interactive document editing surfaces (like AI refinement prompts, version compare, and edit cancels) are frequently rendered without text labels or `aria-label` attributes, rendering them unannounced to assistive technologies.
**Action:** Always verify icon-only buttons in interactive cards have explicit `aria-label` attributes describing their action in context.

## 2025-10-03 - Accessible Modal Keyboard Dismissal and Title Association
**Learning:** Shared modal components (like `ConfirmationModal`) require explicit `Escape` key handling and `aria-labelledby` attributes so keyboard and screen reader users can navigate and dismiss dialogs seamlessly.
**Action:** When working on modal dialogs, always verify `Escape` key listeners and `aria-labelledby` properties are present alongside `role="dialog"` and `aria-modal="true"`.
