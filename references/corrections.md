# Qualifications to the original list

The original numbering and ten pillars are retained. Titles and instructions are revised, not quoted verbatim.

| Original shortcut | Package interpretation |
| --- | --- |
| HSTS redirects all HTTP | Configure the redirect separately; HSTS is learned over HTTPS and has a first-visit limitation. |
| JWT for every app | Choose a session model from requirements; include expiry, rotation and revocation. |
| HttpOnly blocks XSS | It prevents script access to that cookie, not malicious actions by injected scripts. |
| SameSite Strict everywhere | Choose deliberately; login/checkout redirects can require different settings. |
| CORS wildcard never allowed | Private credentialed APIs need constrained origins; public unauthenticated resources differ. |
| ORM strictly required | Parameterization and safe identifiers are the control; an ORM is optional. |
| AES-256 for every column | Classify data and manage keys; use appropriate authenticated encryption where required. |
| TLS 1.3 only | Prefer modern TLS; document necessary secure compatibility. |
| Banner means compliance | Consent, lawful processing, retention and rights depend on context; no certification is implied. |
| Instant refunds | Reconcile asynchronous provider and bank states; do not promise settlement time. |
| Hold stock lock during checkout | Reserve durably with expiry; keep network calls outside long transactions. |
| SSR means immediate updates | Choose rendering by route; measure response and client performance. |
| Redis/micro-frontends/multi-region required | Adopt only for demonstrated workload, team or recovery requirements. |
| WCAG 2.1 plus ARIA | Target WCAG 2.2 AA for web by default; verify semantics and human interaction. |
| Server tracking bypasses blockers | Preserve consent and opt-outs across every collection path. |
| Daily snapshots equal PITR | Point-in-time recovery typically needs additional logging and tested restoration. |
| Type safety means input safety | Validate runtime data at every untrusted boundary. |
| Every project needs every feature | Conditional controls and optional decisions have explicit applicability. |
