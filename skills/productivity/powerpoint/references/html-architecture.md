# HTML Deck Architecture (Reference)

Use this as a baseline structure. Customize theme tokens + layout + motion so the result feels *hand-designed*.

## Skeleton
- One `<section class="slide">` per slide.
- CSS tokens in `:root` for: colors, typography, spacing, easing, durations.
- `.reveal` elements animate when the slide gets `.visible`.

## Must-have UX
- Arrow keys / space / shift+space
- Touch swipe (horizontal)
- Wheel navigation with cooldown
- Progress bar (top or side)
- Dots or mini-map nav (optional)

## Accessibility
- Respect reduced motion.
- Ensure contrast.
- Focus outlines.
- `aria-label` on controls.

## Performance
- Avoid heavy effects on mobile.
- Use `will-change` sparingly.
- Prefer CSS transforms/opacity.
