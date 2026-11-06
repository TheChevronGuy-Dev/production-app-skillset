# Operations rules

Rules retain the original numbering. Apply only after checking the condition. Decisions are not mandatory features; controls are required when applicable.

## Contents

- R069: CI/CD checks
- R070: Blue-green deployment
- R071: Canary releases
- R072: Centralized logs
- R073: Synthetic monitoring
- R074: Graceful shutdown
- R075: Backups and recovery
- R076: Multi-region recovery
- R077: Circuit breakers
- R078: Reproducible runtime

## R069 — CI/CD checks

**Type:** control. **Applies when:** Versioned application development.

Run builds, lint, tests and security checks on PRs with minimal permissions. Protect release paths and never expose secrets to untrusted contributions.

**Verify:** Verify a failing change blocks the configured merge/release path.

## R070 — Blue-green deployment

**Type:** decision. **Applies when:** Services requiring low-downtime releases.

Use only when hosting and data compatibility support it; migrate using expand/contract patterns and keep rollback credible.

**Verify:** Rehearse switch/rollback with old and new versions against the same schema.

## R071 — Canary releases

**Type:** decision. **Applies when:** Risky changes with observable traffic.

Choose cohort and ramp from risk, not a universal five percent; define metrics, abort thresholds and rollback ownership.

**Verify:** Inject an error and demonstrate rollout halt and recovery.

## R072 — Centralized logs

**Type:** control. **Applies when:** Distributed or production services.

Collect structured redacted logs with correlation IDs, access control, retention and actionable alerts.

**Verify:** Trace one failed flow across components without exposing secrets.

## R073 — Synthetic monitoring

**Type:** decision. **Applies when:** Deployed critical flows.

Use isolated test identities/data and safe sandbox payment flows; alert on actionable availability and latency failures.

**Verify:** Break a dependency and verify alert routing and cleanup.

## R074 — Graceful shutdown

**Type:** control. **Applies when:** Long-running servers or workers.

Stop accepting new work, drain requests, acknowledge jobs only after durable completion and bound termination time.

**Verify:** Terminate during requests/jobs and verify safe retry behavior.

## R075 — Backups and recovery

**Type:** control. **Applies when:** Durable business data.

Choose RPO/RTO, backup frequency and point-in-time logging accordingly. Encrypt backups and regularly restore to an isolated environment.

**Verify:** Restore to a chosen time and measure actual data loss and recovery duration.

## R076 — Multi-region recovery

**Type:** decision. **Applies when:** Business-justified regional outage risk.

Define replication consistency, failover authority, residency constraints and split-brain prevention. Simpler tested backups may fit smaller systems.

**Verify:** Rehearse failover/failback and reconciliation under a documented scenario.

## R077 — Circuit breakers

**Type:** control. **Applies when:** Unreliable remote dependencies.

Set timeouts, bounded retries with jitter and safe fallbacks; use circuit breakers when they improve failure isolation.

**Verify:** Simulate latency/errors and ensure requests and retries remain bounded.

## R078 — Reproducible runtime

**Type:** decision. **Applies when:** Applications with environment drift.

Use lockfiles and reproducible builds; containers are optional. If used, run minimal nonroot images, scan them and keep secrets out of layers.

**Verify:** Build cleanly and run under intended permissions/runtime constraints.

