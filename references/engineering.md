# Engineering rules

Rules retain the original numbering. Apply only after checking the condition. Decisions are not mandatory features; controls are required when applicable.

## Contents

- R094: Linting and formatting
- R095: Unit testing
- R096: End-to-end testing
- R097: Interface contracts
- R098: Development parity
- R099: Dependency security
- R100: Readable maintainable code

## R094 — Linting and formatting

**Type:** control. **Applies when:** Maintained codebase.

Adopt stack-appropriate lint/format rules in CI; local hooks are convenience rather than the enforcement boundary.

**Verify:** Submit a deliberate violation and verify CI reports it.

## R095 — Unit testing

**Type:** control. **Applies when:** Business logic and invariants.

Prioritize meaningful boundary/error tests and critical math; avoid coverage targets that reward implementation-mirroring tests.

**Verify:** Demonstrate representative logic faults fail tests.

## R096 — End-to-end testing

**Type:** control. **Applies when:** Critical user journeys.

Test meaningful behavior and recovery using isolated data; include accessibility and real supported browsers where feasible.

**Verify:** Run success and failure paths without dependence on production credentials.

## R097 — Interface contracts

**Type:** control. **Applies when:** Separate client/server boundaries.

Use versioned runtime schemas and generated types where helpful; type safety alone does not validate hostile input.

**Verify:** Test incompatible payloads and backward compatibility of deployed clients.

## R098 — Development parity

**Type:** control. **Applies when:** Multiple deployment environments.

Match relevant versions/configuration shape using synthetic data; never copy production secrets or personal data into local development.

**Verify:** Start from documented setup and compare required config keys.

## R099 — Dependency security

**Type:** control. **Applies when:** Third-party code.

Use lockfiles, automated vulnerability and secret scanning, update policy and reviewed advisories; triage exploitability and document time-bounded exceptions.

**Verify:** Introduce a test finding and verify triage/remediation workflow.

## R100 — Readable maintainable code

**Type:** control. **Applies when:** All application code.

Use domain names, small cohesive modules and explanations for nonobvious decisions; document operations and public interfaces where names alone are insufficient.

**Verify:** Have a reviewer trace a core workflow and locate its failure/recovery paths.

