# Localization rules

Rules retain the original numbering. Apply only after checking the condition. Decisions are not mandatory features; controls are required when applicable.

## Contents

- R091: Locale routing
- R092: Dates, times and numbers
- R093: RTL layouts

## R091 — Locale routing

**Type:** decision. **Applies when:** Multiple language/market routes.

Choose stable locale rules, explicit user override and consistent fallback; connect localized equivalents appropriately.

**Verify:** Test unknown locales, direct links and preference changes.

## R092 — Dates, times and numbers

**Type:** control. **Applies when:** Locale-sensitive output.

Store instants with timezone context as needed; use locale formatting and explicit display zones. Preserve date-only and scheduled-local-time semantics.

**Verify:** Test DST gaps/overlaps, date boundaries and decimal separators.

## R093 — RTL layouts

**Type:** decision. **Applies when:** Right-to-left language support.

Use logical CSS properties and explicit bidirectional handling; mirror directional affordances selectively.

**Verify:** Test real RTL text, mixed identifiers and keyboard order.

