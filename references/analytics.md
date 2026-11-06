# Analytics rules

Rules retain the original numbering. Apply only after checking the condition. Decisions are not mandatory features; controls are required when applicable.

## Contents

- R079: Client analytics
- R080: Feature flags
- R081: A/B experiments
- R082: Server-side analytics
- R083: Idempotent data synchronization
- R084: Analytics data minimization
- R085: Identity merging

## R079 — Client analytics

**Type:** decision. **Applies when:** Purpose-justified telemetry.

Collect minimal events with documented retention and appropriate user choices; avoid raw input capture and unnecessary identifiers.

**Verify:** Inspect event payloads and verify collection follows preferences.

## R080 — Feature flags

**Type:** decision. **Applies when:** Staged or remotely controlled behavior.

Evaluate access-sensitive logic server-side; assign owners, expiry and fallback. Flags are not authorization.

**Verify:** Test missing flag service, both branches and eventual removal.

## R081 — A/B experiments

**Type:** decision. **Applies when:** Measurable product hypotheses.

Define outcome, sample strategy and guardrails before launch; assign stable cohorts and respect data choices.

**Verify:** Check allocation, contamination and stopping criteria.

## R082 — Server-side analytics

**Type:** decision. **Applies when:** Approved conversion measurement.

Preserve consent/opt-outs and minimize payloads; never use server tracking to defeat expressed privacy choices. Deduplicate browser/server events.

**Verify:** Verify opted-out events stay suppressed and duplicate conversions collapse.

## R083 — Idempotent data synchronization

**Type:** control. **Applies when:** Retried imports or integrations.

Use stable source keys, unique constraints, checkpoints and explicit conflict policy; handle deletions as well as inserts.

**Verify:** Replay imports and interrupt/restart midway without duplicate rows.

## R084 — Analytics data minimization

**Type:** control. **Applies when:** Telemetry with sensitive attributes.

Remove or aggregate unnecessary data before collection; pseudonymization is not anonymization. Limit join keys and access.

**Verify:** Inspect exported data and attempt unauthorized reidentification joins.

## R085 — Identity merging

**Type:** decision. **Applies when:** Guest-to-account attribution.

Merge only with verified identity and allowed purpose; maintain logout boundaries and avoid merging shared-device users incorrectly.

**Verify:** Test account switching, shared devices and deletion propagation.

