# Ux rules

Rules retain the original numbering. Apply only after checking the condition. Decisions are not mandatory features; controls are required when applicable.

## Contents

- R047: Responsive design
- R048: Accessibility target
- R049: Keyboard and focus
- R050: Loading states
- R051: Layout stability
- R052: Form autocomplete
- R053: Inline validation
- R054: Theme preferences
- R055: Optimistic mutations
- R056: Collection navigation
- R057: Notifications in UI
- R058: Browser compatibility
- R059: Empty states

## R047 — Responsive design

**Type:** control. **Applies when:** Interactive web or mobile UI.

Design small-screen layouts, touch targets, safe areas and zoom behavior; use content-driven breakpoints.

**Verify:** Test narrow/wide layouts, zoom, orientation and long content.

## R048 — Accessibility target

**Type:** control. **Applies when:** User interfaces.

Target WCAG 2.2 AA for web unless requirements specify otherwise. Use semantic controls, labels and accessible errors; do not claim conformance from an automated scan.

**Verify:** Combine automated checks with keyboard, screen reader and contrast review.

## R049 — Keyboard and focus

**Type:** control. **Applies when:** Interactive UI.

Use predictable focus order, visible focus, modal containment/return and escape behavior. Prefer native controls over custom ARIA widgets.

**Verify:** Complete key flows without a pointer and check no unintended traps.

## R050 — Loading states

**Type:** decision. **Applies when:** Noticeable asynchronous UI work.

Use appropriate skeletons or progress messages without flicker; announce meaningful changes and respect reduced motion.

**Verify:** Test slow/offline transitions and screen reader announcements.

## R051 — Layout stability

**Type:** control. **Applies when:** Rendered visual content.

Reserve image/embed dimensions and account for font swaps and inserted banners.

**Verify:** Measure CLS under slow fonts/images and consent/loading transitions.

## R052 — Form autocomplete

**Type:** control. **Applies when:** Data-entry forms.

Use standard input types and autocomplete tokens on appropriate fields; keep payment card fields within provider-hosted integrations.

**Verify:** Test browser autofill, password managers and mobile keyboards.

## R053 — Inline validation

**Type:** control. **Applies when:** Interactive forms.

Validate helpfully without interrupting typing; retain values and connect errors to labels. Repeat validation on the server.

**Verify:** Submit invalid forms by keyboard and verify readable recoverable errors.

## R054 — Theme preferences

**Type:** decision. **Applies when:** Products offering themes.

Respect system preference and explicit user choice; ensure contrast in every theme and avoid initial theme flash.

**Verify:** Test theme persistence, system changes and contrast.

## R055 — Optimistic mutations

**Type:** decision. **Applies when:** Reversible low-risk actions.

Use pending state, cancellation/rollback and response ordering. Require authoritative confirmation for destructive or financial outcomes.

**Verify:** Test failed and reordered operations and concurrent edits.

## R056 — Collection navigation

**Type:** decision. **Applies when:** Long lists.

Choose pagination/load-more/infinite scrolling based on task; preserve position and access to footer and navigation.

**Verify:** Test back navigation, keyboard traversal and refresh/bookmarks.

## R057 — Notifications in UI

**Type:** decision. **Applies when:** Background status updates.

Use accessible status messages with sufficient display time; keep essential errors/actionable details persistent instead of toast-only.

**Verify:** Test screen reader announcements and recovery after a toast disappears.

## R058 — Browser compatibility

**Type:** control. **Applies when:** Web apps.

Define a support matrix and test Chromium, WebKit and Gecko as relevant; use feature detection and progressive enhancement.

**Verify:** Run critical flows on supported engines and representative devices.

## R059 — Empty states

**Type:** control. **Applies when:** Views with no results.

Distinguish first use, no match, permissions, loading and failure; offer the appropriate next action.

**Verify:** Exercise each state without suggesting unauthorized actions.

