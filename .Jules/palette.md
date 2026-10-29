## 2025-05-18 - Accessibility for Interactive AI Output Controls
**Learning:** Icon-only buttons within interactive document editing surfaces (like AI refinement prompts, version compare, and edit cancels) are frequently rendered without text labels or `aria-label` attributes, rendering them unannounced to assistive technologies.
**Action:** Always verify icon-only buttons in interactive cards have explicit `aria-label` attributes describing their action in context.

## 2025-10-03 - Accessible Modal Keyboard Dismissal and Title Association
**Learning:** Shared modal components (like `ConfirmationModal`) require explicit `Escape` key handling and `aria-labelledby` attributes so keyboard and screen reader users can navigate and dismiss dialogs seamlessly.
**Action:** When working on modal dialogs, always verify `Escape` key listeners and `aria-labelledby` properties are present alongside `role="dialog"` and `aria-modal="true"`.

## 2025-10-24 - Focus Visibility for Hover-Only Card Actions
**Learning:** Overlay or corner action buttons on workspace cards using `group-hover:opacity-100` remain hidden to keyboard navigation unless `group-focus-within:opacity-100` and `focus-visible:opacity-100` are applied, and interactive card containers need explicit `role="button"` and `onKeyDown` handlers.
**Action:** When making card components interactive with hover actions, ensure keyboard focus states (`group-focus-within`, `focus-visible`) and key handling (`Enter`/`Space`) are included.

## 2026-10-25 - ARIA Attributes for Progress Bar Components
**Learning:** Visual progress indicators built with plain HTML `<div>` elements are invisible to assistive technologies unless given `role="progressbar"`, `aria-valuenow`, `aria-valuemin`, `aria-valuemax`, `aria-valuetext`, and a contextual `aria-label`.
**Action:** When building or updating reusable progress bar components, ensure ARIA progressbar semantics and customizable labels are built into the component standard.

## 2026-03-30 - ARIA Alert Live Region and Clear Dismiss Icon Semantics for Error Banners
**Learning:** Error banners using misleading non-interactive close icons (like `X`) confuse users into thinking the banner is dismissible when it is static. Adding `role="alert"` and `aria-live="assertive"` ensures screen readers announce generation failures immediately, while replacing non-functional icons with `AlertCircle` and adding an optional interactive dismiss button improves both UX clarity and keyboard accessibility.
**Action:** Always pair `role="alert"` and `aria-live="assertive"` on error banners, use standard status icons (`AlertCircle`), and ensure dismiss buttons are fully keyboard-accessible with `aria-label`.

## 2026-04-02 - Associated Labels and ARIA Live Regions for Export Workflow Tool Selectors
**Learning:** Dropdown `<select>` elements in workflow panels without explicit `<label>` or `htmlFor` bindings fail to describe their target application to screen readers, and dynamic progress log output from asynchronous export generation is ignored by assistive technologies unless wrapped in an `aria-live` region.
**Action:** Always pair form `<select>` elements with explicit `<label htmlFor="...">` and apply `aria-live="polite"` to containers displaying live status updates from multi-step workflows.
