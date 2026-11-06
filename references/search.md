# Search rules

Rules retain the original numbering. Apply only after checking the condition. Decisions are not mandatory features; controls are required when applicable.

## Contents

- R060: Faceted search
- R061: Fuzzy matching
- R062: Sitemaps
- R063: Semantic HTML
- R064: Structured data
- R065: Canonical URLs
- R066: Readable URLs
- R067: Typeahead
- R068: Server-rendered metadata

## R060 — Faceted search

**Type:** decision. **Applies when:** Large searchable catalogs.

Use validated filters reflected in URLs; authorize query results and counts; provide reset controls.

**Verify:** Test filter combinations, zero results and private item leakage.

## R061 — Fuzzy matching

**Type:** decision. **Applies when:** Search with spelling variability.

Tune matching to the domain and language, enforce access filters and bound query expense.

**Verify:** Evaluate typos, exact identifiers, relevance and sensitive results.

## R062 — Sitemaps

**Type:** decision. **Applies when:** Public indexable websites.

List canonical indexable URLs; regenerate on meaningful change rather than requiring daily runs. Exclude private and redirect/error pages.

**Verify:** Parse generated XML and check representative URL status/indexability.

## R063 — Semantic HTML

**Type:** control. **Applies when:** Web pages.

Use appropriate landmarks, heading order and native interactive elements; avoid redundant ARIA.

**Verify:** Inspect document structure and screen reader navigation.

## R064 — Structured data

**Type:** decision. **Applies when:** Eligible public rich-result pages.

Use supported JSON-LD types with truthful visible content; never fabricate ratings or promise rich results.

**Verify:** Validate structured data and compare values with page content.

## R065 — Canonical URLs

**Type:** decision. **Applies when:** Public pages with URL variants.

Set consistent canonical targets and coherent redirects/sitemaps; canonical is a hint, not access control.

**Verify:** Compare variant URLs and confirm intended canonical is indexable.

## R066 — Readable URLs

**Type:** decision. **Applies when:** Public routes.

Use stable meaningful slugs, support necessary Unicode and redirect changed paths; avoid sensitive identifiers in URLs.

**Verify:** Test collisions, renamed records, encoding and old links.

## R067 — Typeahead

**Type:** decision. **Applies when:** Search suggestion UI.

Debounce and cancel stale queries; implement accessible combobox behavior and do not expose private search history.

**Verify:** Test rapid input, response reorder, keyboard selection and privacy.

## R068 — Server-rendered metadata

**Type:** decision. **Applies when:** Shareable public pages.

Deliver title/description/Open Graph metadata in initial HTML where crawlers need it; use absolute image URLs and avoid leaking private content.

**Verify:** Fetch HTML without scripts and test image accessibility.

