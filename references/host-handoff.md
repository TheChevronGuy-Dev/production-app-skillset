# Export, deployment and ownership

## Choose the delivery target

| Product | Typical deliverable | Verify before choosing a host |
| --- | --- | --- |
| Static site | Built HTML/CSS/JS/assets | Routes, forms, asset paths and caching; no server secrets |
| Server-rendered web app/API | Source plus reproducible build/start instructions, or container | Runtime versions, server functions, environment, jobs, limits and regions |
| Persistent app | App plus migrations, storage and recovery plan | Database connectivity, backups, object storage and authorization |
| Android/iOS | Source and platform-specific signed distribution build | Signing ownership, supported devices, privacy declarations and current store requirements |

Native apps also need hosted backends when they use remote services. An Android/iOS app is not deployed by uploading its source to a static website host. iOS builds require access to the supported Apple toolchain and signing/distribution setup; record that dependency early.

## Prepare a portable handoff

Deliver source, lockfiles, migration history, synthetic fixtures, asset/license attribution, configuration names in `.env.example`, clean setup/build/test commands and an architecture overview. Document provider-specific dependencies and an exit/data-export path. Do not bundle secrets, private assessments, real customer data, caches or local virtual environments into a public export. Keep application output separate from this skill package.

Create an owner-readable RUNBOOK describing domains, accounts, billing owner, administrative access, secret rotation, backup/restore, monitoring and support. Create a release record with revision, target, actual tests, unresolved work and rollback steps. Verify a clean checkout can build with documented commands; do not imply every framework supports a static export.

## Preview to production

1. Use an isolated preview environment with synthetic data and sandbox services. Confirm environment variables, callback URLs, DNS/TLS, database migrations, queues, object storage and email/webhook endpoints.
2. Test the core journey through the deployed URL or installed release build, including authorization failures and dependency outages. Verify accessibility, performance budgets, privacy preferences and redacted logs.
3. Back up persistent state and rehearse restoration. Use compatible migrations; application rollback may not undo database writes. Establish rollout/rollback triggers and an owner.
4. Confirm the user's intended deployment scope and any required account/billing decisions; existing explicit authorization is sufficient. Publish only the reviewed artifact. Do not create paid resources, register domains or send campaigns as an implied consequence of generating a plan.
5. Verify production configuration and a controlled smoke test, then check monitoring and support paths. Record which checks require later owner action. Keep test transactions controlled and authorized.

## After launch

Assign dependency updates, certificate/domain renewal, backup restore checks, abuse handling, payment reconciliation and email reputation monitoring. Link actionable alerts to an owner. Keep a small feedback backlog and revisit scope when adding features. A successful deployment is a milestone; ongoing operations and real evidence remain necessary.
