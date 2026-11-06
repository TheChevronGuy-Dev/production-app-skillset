# Performance rules

Rules retain the original numbering. Apply only after checking the condition. Decisions are not mandatory features; controls are required when applicable.

## Contents

- R034: Server-side rendering
- R035: Static generation
- R036: CDN distribution
- R037: Database indexes
- R038: Connection pooling
- R039: Caching
- R040: Lazy loading
- R041: Asset compression
- R042: API pagination
- R043: Background queues
- R044: Micro-frontends
- R045: Load balancing
- R046: Stateless app servers

## R034 — Server-side rendering

**Type:** decision. **Applies when:** Pages needing dynamic initial HTML.

Choose SSR per route based on content and latency; avoid caching private output across users and unnecessary server work.

**Verify:** Measure initial response and test personalized cache isolation.

## R035 — Static generation

**Type:** decision. **Applies when:** Public cacheable pages.

Prebuild suitable content and define refresh/invalidation; keep private or rapidly changing values authoritative at runtime.

**Verify:** Change content/prices and verify freshness and preview behavior.

## R036 — CDN distribution

**Type:** decision. **Applies when:** Public assets or edge workloads.

Cache public resources with explicit keys and invalidation. Keep credentials and private responses out of shared caches.

**Verify:** Compare authenticated users and verify cache purge/version behavior.

## R037 — Database indexes

**Type:** control. **Applies when:** Measured slow queries.

Use query plans and representative data to add targeted indexes; consider write cost, locking and migration safety.

**Verify:** Compare query plans, latency and write throughput before/after.

## R038 — Connection pooling

**Type:** control. **Applies when:** Database-backed services.

Budget connections across instances and workers; use a pool compatible with deployment and transaction semantics.

**Verify:** Load-test peak concurrency and verify bounded connection counts/timeouts.

## R039 — Caching

**Type:** decision. **Applies when:** Measured repeated expensive work.

Choose cache only with clear invalidation and ownership keys; bound TTL and memory, prevent stampedes, and handle cache outage.

**Verify:** Test stale values, tenant isolation and cache loss.

## R040 — Lazy loading

**Type:** control. **Applies when:** Noncritical resources.

Defer below-fold images and optional code; do not lazy-load primary above-fold content. Preserve accessibility and dimensions.

**Verify:** Measure initial requests and verify deferred content loads on interaction.

## R041 — Asset compression

**Type:** control. **Applies when:** Network-delivered assets.

Use appropriate modern image formats with fallbacks and Brotli/gzip for text; preserve visual quality and avoid compressing already-compressed data unnecessarily.

**Verify:** Inspect negotiated formats, response sizes and readable fallback output.

## R042 — API pagination

**Type:** control. **Applies when:** Unbounded collections.

Set hard size limits and stable ordering; use opaque cursors where appropriate and authorize every page.

**Verify:** Test ties, concurrent inserts, bad cursors and maximum page limits.

## R043 — Background queues

**Type:** control. **Applies when:** Slow or retryable jobs.

Persist jobs reliably, define retry/backoff, idempotency and dead-letter handling; use an outbox when DB changes must cause jobs.

**Verify:** Crash workers, replay jobs and observe backlog/poison-message handling.

## R044 — Micro-frontends

**Type:** decision. **Applies when:** Independent teams with proven need.

Default to a simpler modular application; adopt micro-frontends only with explicit ownership and deployment benefits that justify integration cost.

**Verify:** Document the tradeoff and test shared auth, routing and version skew.

## R045 — Load balancing

**Type:** control. **Applies when:** Multiple application instances.

Use health/readiness checks and connection draining; design routing around long-lived connections and regional constraints.

**Verify:** Remove an instance under traffic and verify safe rerouting.

## R046 — Stateless app servers

**Type:** control. **Applies when:** Horizontally scaled request handlers.

Move durable state to suitable stores; handle websocket/session affinity explicitly when needed. Do not mistake stateless servers for a stateless system.

**Verify:** Restart instances mid-flow and verify no durable state loss.

