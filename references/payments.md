# Payments rules

Rules retain the original numbering. Apply only after checking the condition. Decisions are not mandatory features; controls are required when applicable.

## Contents

- R021: Tokenized payment collection
- R022: Idempotent payment webhooks
- R023: Atomic inventory reservations
- R024: Multi-currency pricing
- R025: Guest checkout
- R026: Optimistic cart updates
- R027: Persistent cart
- R028: Address assistance
- R029: Tax calculation
- R030: Refund reconciliation
- R031: 3DS and payment challenges
- R032: Cart recovery messages
- R033: Server-side discounts

## R021 — Tokenized payment collection

**Type:** control. **Applies when:** Card checkout.

Collect payment details with provider-hosted fields or checkout; create payment amounts and order identifiers on the server.

**Verify:** Tamper with client totals and confirm server pricing prevails.

## R022 — Idempotent payment webhooks

**Type:** control. **Applies when:** Payment events.

Verify signatures on raw bytes using the provider SDK, durably record events, and make business effects idempotent. Handle retries and out-of-order delivery.

**Verify:** Replay events, deliver concurrently/out of order, and crash between persistence and processing.

## R023 — Atomic inventory reservations

**Type:** control. **Applies when:** Limited stock checkout.

Reserve stock using conditional writes or transactions; expire abandoned reservations. Do not hold DB locks while waiting for payment network calls.

**Verify:** Race buyers for the last unit and test expiry/payment arrival races.

## R024 — Multi-currency pricing

**Type:** decision. **Applies when:** Multiple selling currencies.

Store explicit currency and integer minor units or suitable decimals; respect zero/three-decimal currencies. Confirm currency before purchase; locale is only a hint.

**Verify:** Test rounding, currency changes, refunds and server/provider amount equality.

## R025 — Guest checkout

**Type:** decision. **Applies when:** Consumer commerce.

Allow guest purchase where business rules permit; provide secure order access and optional account linking without exposing orders by email alone.

**Verify:** Buy as a guest and attempt unauthorized order lookup.

## R026 — Optimistic cart updates

**Type:** control. **Applies when:** Interactive cart.

Update provisionally with rollback and server reconciliation; communicate rejected stock/price changes. Do not present payment as successful optimistically.

**Verify:** Simulate failure, slow responses and edits arriving out of order.

## R027 — Persistent cart

**Type:** control. **Applies when:** Returning shoppers.

Persist nonsensitive cart identifiers/items; reconcile server prices, quantities and ownership after sign-in. Avoid storing session credentials in localStorage.

**Verify:** Merge guest/account carts and verify account switching cannot leak items.

## R028 — Address assistance

**Type:** decision. **Applies when:** Shipped goods.

Provide optional address suggestions and manual entry; validate shipping eligibility server-side and minimize data sent to vendors.

**Verify:** Test unsupported addresses, keyboard access and vendor failure.

## R029 — Tax calculation

**Type:** control. **Applies when:** Taxable sales.

Determine obligations and configured jurisdictions with appropriate expertise; compute tax server-side using current provider rules and retain calculation evidence.

**Verify:** Test inclusive/exclusive tax, discounts and refund adjustments in sandbox.

## R030 — Refund reconciliation

**Type:** control. **Applies when:** Refundable payments.

Model refunds as asynchronous states; use idempotency and reconcile provider results to the ledger. Never promise immediate bank settlement.

**Verify:** Test duplicate requests, partial refunds, provider failure and delayed completion.

## R031 — 3DS and payment challenges

**Type:** control. **Applies when:** Provider-required card authentication.

Use provider-supported challenge flows; handle pending, failed, canceled and resumed attempts. Confirm success server-side.

**Verify:** Exercise sandbox challenge, cancel, retry and asynchronous completion.

## R032 — Cart recovery messages

**Type:** decision. **Applies when:** Optional marketing follow-up.

Use lawful eligibility, consent/preferences where required, suppression lists and frequency limits; distinguish marketing from transactional messages.

**Verify:** Confirm opted-out and completed buyers receive no recovery campaign.

## R033 — Server-side discounts

**Type:** control. **Applies when:** Discounted sales.

Enforce eligibility, expiry, stacking and redemption limits atomically; recalculate totals on the server.

**Verify:** Race limited coupons and tamper with discount amounts and account identity.

