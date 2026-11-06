# Implementation playbooks

These are design sequences, not copy/paste production handlers. Bind them to the actual framework, provider and database, then test failure cases.

## Authentication and authorization

1. Identify browser, native and service clients. Prefer maintained identity/session integrations.
2. Define session lifetime, rotation, logout, recovery and elevated-action requirements.
3. Centralize deny-by-default permission evaluation; still scope queries to the authorized object and tenant.
4. Add CSRF protection for ambient browser credentials and independently validate all server inputs.
5. Test user A against user B's records and tenant A against tenant B through every path, including jobs and downloads.

## Payment event inbox and outbox

```text
Receive bounded raw request bytes
Verify provider signature and protocol-specific freshness with provider SDK
Reject invalid delivery without processing it
Begin database transaction
  Insert authenticated event into inbox with unique provider/account/event key
  If already durably accepted: do not enqueue duplicate work
Commit durable acceptance
Return success to provider only after durable acceptance
Worker claims pending inbox entry with crash-recoverable lease
  Resolve provider state when events can be stale or unordered
  Validate local order, account, amount, currency and allowed state transition
  In transaction: update order + insert unique fulfillment outbox record
  Mark event handled atomically with those database changes
Outbox worker performs retryable effects with downstream idempotency keys
```

A transaction cannot make an arbitrary remote side effect exactly-once. Use provider idempotency keys or reconciliation for payments, fulfillment and emails; protect business operations with unique keys as well as delivery event IDs. Two distinct provider events may describe the same underlying business change. Queue acknowledgment must follow durable work. Do not use an in-memory set as the processing record.

Tests: invalid signature, duplicate event, two different events for the same payment, out-of-order delivery, worker crash before/after commit, queue outage, fulfillment timeout and amount mismatch.

## Inventory reservations

1. Reprice trusted catalog items and validate quantities server-side.
2. In a short transaction, conditionally reserve available units with an expiration and unique checkout key. Reject insufficient stock atomically.
3. Create the provider payment outside the transaction with an idempotency key. Link it durably; reconcile failures between these operations.
4. Serialize reservation expiry and payment success transitions. Define compensation (refund/manual resolution) if payment arrives after stock release.
5. Fulfill once; retain financial and stock audit trails.

Test last-unit races, retries, payment cancellation, expiration races and crash recovery. Never trust the success redirect as proof of payment.

## Safe release

1. Identify migration compatibility, rollout owner, recovery target and monitoring.
2. Run scoped CI with least privilege and sandbox data.
3. Use backward-compatible schema expansion before readers/writers switch; defer destructive cleanup until old versions are retired.
4. Choose the simplest supported rollout that meets downtime/risk needs. Set rollback or roll-forward triggers.
5. Verify the deployed critical path and alerts. Rehearse restoration separately; do not treat a successful deployment as disaster-recovery evidence.
