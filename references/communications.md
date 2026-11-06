# Communications rules

Rules retain the original numbering. Apply only after checking the condition. Decisions are not mandatory features; controls are required when applicable.

## Contents

- R086: Transactional email
- R087: SMS alerts
- R088: Push notifications
- R089: Magic sign-in links
- R090: In-app inbox

## R086 — Transactional email

**Type:** control. **Applies when:** Required account/order notices.

Use a reliable provider, durable enqueue, idempotency and bounce handling; configure sender authentication and separate marketing preferences.

**Verify:** Retry jobs and test bounces without duplicate sensitive notices.

## R087 — SMS alerts

**Type:** decision. **Applies when:** Opted-in SMS communication.

Respect channel permissions and relevant rules; validate provider webhooks, prevent abuse and avoid sensitive lock-screen content.

**Verify:** Test opt-out, invalid signatures, retries and spend limits.

## R088 — Push notifications

**Type:** decision. **Applies when:** Opted-in device messaging.

Bind tokens to the correct account/device, revoke on logout and clean invalid tokens; minimize visible sensitive data.

**Verify:** Switch accounts on one device and verify old-account pushes stop.

## R089 — Magic sign-in links

**Type:** control. **Applies when:** Passwordless email authentication.

Use high-entropy, short-lived single-use tokens stored hashed; rate-limit requests and restrict redirects. Avoid consuming credentials on email-scanner GET requests.

**Verify:** Test replay, expiry, link scanners, redirect tampering and account enumeration.

## R090 — In-app inbox

**Type:** decision. **Applies when:** Persistent user notices.

Authorize per-user messages, paginate and synchronize read state; localize content and retain only as needed.

**Verify:** Try another user's message ID and concurrent read updates.

