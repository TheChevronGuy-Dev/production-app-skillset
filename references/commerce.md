# Payments: checkout through reconciliation

Use for debit/credit card sales, subscriptions and refunds. Relevant rules: R016, R021-R033, R083. Start with provider-hosted checkout or hosted card fields. The application owns products, order authorization and fulfillment; the provider collects card details. Do not build a card vault or describe hosted checkout as automatic compliance.

## Product and provider decisions

Identify physical goods, digital goods, subscriptions or a marketplace. Record countries, currencies, tax/shipping needs, refund rules, fees and payout ownership. Native digital purchases may require store billing; check current store policies for the product and region before implementing external checkout. Marketplace payouts and identity verification require an appropriate provider product. Keep sandbox and live resources separate.

## Build the flow

1. Define order, payment and fulfillment states and permitted transitions. Use currency-aware amounts, unique business keys and durable audit records. Keep sensitive payment data out of logs and analytics.
2. Accept item identifiers and quantities; calculate price, discounts, tax and availability on the server. Verify the order belongs to the caller. Reserve limited stock in a short transaction with expiry.
3. Create checkout server-side using a stable idempotency key for the operation. Configure allowed return URLs. Keep network calls outside long database transactions.
4. Display pending/canceled/failed/success states accurately. A success redirect does not prove payment. Verify authenticated provider events on raw bytes, durably accept them and reconcile amount, currency, account and order before fulfillment.
5. Use the inbox/outbox sequence in the implementation playbook for duplicate, delayed and reordered events. Two event IDs may describe one payment: deduplicate business effects as well as deliveries. Define compensation for late payment after stock expiry.
6. Authorize refunds separately, cap them to refundable balances, use idempotency and reconcile asynchronous outcomes. For subscriptions, handle failed renewals, cancellation timing, proration, entitlement changes and reconciliation. Handle disputes with an owner and audit trail.

## Acceptance checks

Run sandbox tests for declined cards, required authentication, abandoned checkout, manipulated prices, wrong-currency events, duplicate/reordered webhooks, worker crashes, double clicks, last-item races, partial refunds and subscription changes. Confirm no PAN/CVC enters application storage or logs. Verify operational access, webhook failures and support procedures before live mode. Never use real customer cards to test.

Implementation examples: [Stripe-hosted checkout](https://docs.stripe.com/checkout/quickstart) and [webhooks](https://docs.stripe.com/webhooks). These illustrate one provider; use the user's chosen provider and its current SDK rather than hard-coding a vendor requirement.
