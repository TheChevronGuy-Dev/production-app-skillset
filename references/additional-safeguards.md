# Beyond the original 100

The numbered catalog preserves the user's original scope. It is not exhaustive. Evaluate these additional safeguards whenever relevant:

- **Native mobile:** store credentials in platform Keychain/Keystore facilities, use system-browser authorization with authorization-code/PKCE where supported, validate deep links and universal/app links, minimize permissions and avoid secrets in shipped binaries. Test logout and account switching. Plan offline conflict resolution and safe updates; web cookies/CSP do not automatically apply to native screens. Use current platform guidance and OWASP MASVS.
- **Authorization:** check object, field, action and tenant boundaries in APIs, search, caches, exports, background jobs and storage URLs. Never trust hidden UI controls.
- **Uploads:** constrain size/type, generate storage names, isolate serving origins, authorize downloads and apply scanning according to risk. Prevent traversal and archive expansion attacks.
- **Outbound requests:** constrain allowed destinations and redirects, prevent access to private networks/metadata services, and defend DNS resolution/connect races. Apply to webhooks and URL previews.
- **Account lifecycle:** rate-limit recovery, invalidate relevant sessions after security changes and prevent account enumeration. Protect administrative and support impersonation actions with auditing.
- **Supply chain:** review licenses and provenance, constrain CI permissions and protect signing/release credentials. Validate dependency changes before executing untrusted install scripts.
- **Business state:** enforce legal order transitions, bounded retries, immutable audit events and database constraints. Distinguish authenticated requests from authorized business actions.
- **Operations:** assign incident ownership, alerts, escalation, migration recovery and explicit availability objectives. Test restoration, not just backup creation.

Document which additional items apply in the assessment scope or an accompanying review. They are not silently included in the 100-rule CLI gate.
