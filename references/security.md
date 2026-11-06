# Security rules

Rules retain the original numbering. Apply only after checking the condition. Decisions are not mandatory features; controls are required when applicable.

## Contents

- R001: HTTPS enforcement
- R002: Session authentication
- R003: Secure cookie sessions
- R004: CSRF protection
- R005: CORS policy
- R006: SQL injection prevention
- R007: XSS prevention
- R008: Rate limiting
- R009: Password hashing
- R010: Multi-factor authentication
- R011: Content Security Policy
- R012: Least privilege and authorization
- R013: Encryption at rest
- R014: Transport encryption
- R015: Privacy obligations
- R016: Payment compliance scope
- R017: Boundary input validation
- R018: Safe errors and logs
- R019: Secret management and rotation
- R020: Security response headers

## R001 — HTTPS enforcement

**Type:** control. **Applies when:** Network services.

Redirect HTTP at the edge; send HSTS on HTTPS after validating subdomain readiness. HSTS alone does not secure the first visit.

**Verify:** Check HTTP redirect and HTTPS headers; reject mixed content.

## R002 — Session authentication

**Type:** control. **Applies when:** Authenticated services.

Choose managed identity or server sessions by default where suitable. If JWTs are justified, validate signature, algorithm allowlist, issuer, audience and expiry; plan revocation.

**Verify:** Reject expired, tampered and wrong-audience credentials; verify logout semantics.

## R003 — Secure cookie sessions

**Type:** control. **Applies when:** Browser cookie authentication.

Use HttpOnly and Secure session cookies with narrow scope. Choose Strict or Lax from actual redirect flows; None requires Secure and explicit cross-site justification. HttpOnly does not prevent XSS actions.

**Verify:** Inspect cookies and test external sign-in, checkout return and session theft exposure.

## R004 — CSRF protection

**Type:** control. **Applies when:** Browser ambient credentials.

Use framework CSRF defenses on unsafe requests including PATCH; verify origin as appropriate. SameSite is defense in depth. Never mutate on GET.

**Verify:** Reject missing or invalid CSRF proof; test cross-site submissions.

## R005 — CORS policy

**Type:** control. **Applies when:** Cross-origin browser access.

Allow only required origins for private APIs; never reflect arbitrary origins with credentials. Public credential-free resources may use wildcard. CORS is not authorization.

**Verify:** Test allowed and hostile origins plus direct nonbrowser requests.

## R006 — SQL injection prevention

**Type:** control. **Applies when:** SQL data access.

Parameterize values; allowlist dynamic identifiers and sort clauses. ORMs do not protect unsafe raw SQL.

**Verify:** Test malicious values and sort keys; inspect raw query paths.

## R007 — XSS prevention

**Type:** control. **Applies when:** Rendered untrusted content.

Use context-aware output encoding and safe DOM APIs. Sanitize deliberately supported HTML with a maintained sanitizer; avoid blanket input mangling.

**Verify:** Exercise HTML, attribute, URL and script-context payloads.

## R008 — Rate limiting

**Type:** control. **Applies when:** Exposed endpoints.

Apply endpoint, account and network limits with shared state where needed. Configure proxy trust; combine with upstream abuse defenses rather than claiming DDoS immunity.

**Verify:** Exercise bursts, multiple instances and spoofed forwarding headers.

## R009 — Password hashing

**Type:** control. **Applies when:** Application-owned passwords.

Prefer Argon2id with current reviewed cost settings; use maintained libraries and unique salts. Treat bcrypt as a compatibility choice and respect byte-length limits.

**Verify:** Verify hashes differ for identical passwords and rehash migration works.

## R010 — Multi-factor authentication

**Type:** control. **Applies when:** Sensitive authenticated actions.

Offer passkeys or TOTP and protect enrollment, recovery and factor replacement. Determine assurance from the actual authentication ceremony.

**Verify:** Test recovery abuse, reused codes and stolen-session enrollment.

## R011 — Content Security Policy

**Type:** control. **Applies when:** Browser documents.

Deploy a policy fitted to actual resources; use nonce or hash based scripts where possible. Roll out reporting, then enforcement; avoid broad unsafe exceptions.

**Verify:** Verify violations are blocked and sign-in/payment integrations still work.

## R012 — Least privilege and authorization

**Type:** control. **Applies when:** Protected resources.

Deny by default; enforce object and tenant access on every request and worker task. Restrict service accounts separately from end-user permissions.

**Verify:** Attempt cross-user and cross-tenant reads and writes including exports.

## R013 — Encryption at rest

**Type:** control. **Applies when:** Sensitive stored data.

Classify data; use managed storage encryption and additional field encryption where threat model warrants. Use authenticated encryption and managed key rotation, not hand-built crypto.

**Verify:** Test key access boundaries, rotation and recovery without exposing plaintext.

## R014 — Transport encryption

**Type:** control. **Applies when:** Network communication.

Prefer TLS 1.3 and retain securely configured TLS 1.2 only when required. Validate certificates; consider service identity and mTLS across trust boundaries.

**Verify:** Reject invalid certificates and obsolete protocols; inspect internal hops.

## R015 — Privacy obligations

**Type:** control. **Applies when:** Personal data processing.

Map data, purposes, retention and applicable obligations; implement deletion/export and consent controls where required. A banner alone is not compliance.

**Verify:** Trace a deletion through replicas and processors; verify optional collection choices.

## R016 — Payment compliance scope

**Type:** control. **Applies when:** Card payments.

Use hosted payment collection; keep card numbers and security codes out of app servers and logs. Confirm actual obligations with the provider and qualified reviewers.

**Verify:** Inspect traffic/logs for card data and document integration scope.

## R017 — Boundary input validation

**Type:** control. **Applies when:** APIs and untrusted data.

Validate schemas, sizes and semantics at server trust boundaries, including worker inputs. Authorize fields to prevent mass assignment; client types are insufficient.

**Verify:** Reject oversized, unknown privileged and malformed fields.

## R018 — Safe errors and logs

**Type:** control. **Applies when:** Applications with logs.

Return generic client errors plus correlation IDs; keep restricted diagnostic logs with redaction, retention and access controls. Do not log secrets or unnecessary PII.

**Verify:** Trigger failures and inspect both client output and stored logs.

## R019 — Secret management and rotation

**Type:** control. **Applies when:** Service credentials.

Keep secrets in managed stores, never bundles or git. Prefer short-lived credentials; rotate with overlap, revocation and rollback procedures.

**Verify:** Rotate a test secret and verify old credentials cease working.

## R020 — Security response headers

**Type:** control. **Applies when:** Browser-facing services.

Set nosniff and appropriate referrer policy. Use CSP frame-ancestors; apply X-Frame-Options when compatible with intentional embedding.

**Verify:** Check actual edge responses and legitimate embed behavior.

