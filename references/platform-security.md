# Platform security and usability review

Use the relevant sections alongside R001-R100. Record each platform check with evidence or an exclusion in a companion review; these checks are outside the numbered CLI gate. This is a review aid, not a complete standard. Prefer the smallest implementation that meets the product's actual risks.

## HTTP and HTTPS web apps and APIs

- **Transport:** use HTTPS for production credentials and sensitive data. HTTP is suitable for explicitly scoped local development or documented non-sensitive uses; do not send tokens before a redirect. Test HTTP redirects, mixed content, certificate renewal and TLS termination through the actual proxy. Do not enable HSTS preload or includeSubDomains until every affected hostname is ready. Keep development certificate exceptions out of release configuration.
- **Request boundaries:** bound body/upload size, parsing depth, execution time and pagination. Configure trusted proxies explicitly; do not trust arbitrary Host or forwarding headers for password-reset links, redirects or origin checks. Test hostile headers and request limits through the deployed proxy and application together.
- **Authorization and inputs:** scope objects, fields, exports, caches and background work to the caller and tenant. Reject unexpected writable fields. Test account A against account B and anonymous requests. CORS, hidden controls and unguessable IDs do not replace authorization.
- **Browser state:** protect cookie-authenticated writes from CSRF; use secure session cookies, suitable CSP and framing policy. Prevent private pages and API responses from entering shared CDN or service-worker caches. Test logout/account switching, browser back navigation and offline caches. Never place secrets in URLs or frontend bundles.
- **Uploads and outbound URLs:** constrain types and sizes, isolate untrusted content and authorize downloads. Prevent traversal, archive bombs and SSRF across redirects and DNS changes. Test cloud metadata/private-network destinations with synthetic fixtures.
- **Usability:** verify keyboard/focus, screen-reader labels, zoom, validation messages, password-manager support, loading/error/empty states and slow connections. Preserve safe form progress after recoverable errors; make retryable writes idempotent. Use WCAG 2.2 as a web reference and record manual checks.

## Android

- Inspect the merged **release** manifest and Network Security Configuration. Disable unintended cleartext traffic; keep debug trust anchors and test endpoints scoped to debug builds. Never fix TLS failures with permissive trust managers or hostname verifiers. Test a release build against invalid certificates and unintended HTTP endpoints.
- Use Android Keystore-backed key protection for sensitive local credentials where appropriate; keys and encrypted data have distinct storage requirements. Review backup/data-extraction rules, logs, clipboard, screenshots and notifications for leakage. Test logout, account switching, reinstall/restore and device-lock behavior.
- Minimize exported activities/services/receivers/providers and permissions. Validate incoming intents, content URIs and Android App Links, and recheck server authorization after navigation. Test hostile external intents and links without assuming verified links make their parameters trusted.
- Restrict WebView navigation and content origins; expose native bridges only to explicitly trusted content. Avoid loading untrusted HTML into privileged WebViews. Test redirects, file/content access and unexpected origins.
- Test runtime permission denial/revocation, TalkBack, font scaling, rotation, process death, back navigation, loss of connectivity and queued-write replay. Keep sensitive data out of saved UI state. Declare actual SDK data collection and protect signing keys outside the repository.

## iOS

- Review App Transport Security settings in the built app; avoid broad arbitrary-load exceptions. Document narrow exceptions and test that unintended HTTP and invalid certificates fail. Do not disable certificate validation to solve development issues.
- Store credentials using Keychain with protection/accessibility choices appropriate to background access, device locking and migration. Review file protection, backups, logs, pasteboard, app-switcher snapshots and notifications. Test logout, account switching and restore; do not assume uninstall alone clears all credentials.
- Minimize entitlements and permission usage descriptions. Validate universal links, custom URL schemes and document/import handlers; treat all parameters as untrusted. Reauthorize sensitive operations on the backend.
- Restrict WKWebView navigation and script message handlers to required trusted content. Avoid exposing privileged native actions to arbitrary pages. Review app extensions and shared containers for cross-component data access.
- Test VoiceOver, Dynamic Type, permission denial/revocation, background/foreground transitions, interrupted sign-in, offline retries and supported device sizes. Verify privacy declarations against actual SDK behavior and protect distribution credentials.

## Shared native and hybrid app decisions

Use system-browser authorization and authorization-code/PKCE for OAuth public clients; embedded app secrets cannot establish client confidentiality. Bind and validate authorization responses with the chosen maintained SDK. Test cancellation, replay, wrong redirects and account switching. Biometrics can unlock local access; backend authorization still applies.

For offline writes, define conflict handling, queue ownership, retry bounds and server idempotency. Purge or rebind pending work on logout so one account cannot submit another's data. Plan backward-compatible APIs for older installed app versions, migrations and minimum-supported-version behavior. Review store payment rules for the actual digital/physical product before choosing checkout.

Verify production artifacts, not only emulator/debug behavior. Record target OS versions, build variant, real-device checks and unavailable checks. Jailbreak/root detection, attestation and certificate pinning are risk-based layers with failure and rotation costs; they never replace server authorization. Consult OWASP MASVS/MASTG for a broader native security review.

## Primary references

- [Android Network Security Configuration](https://developer.android.com/privacy-and-security/security-config)
- [Apple App Transport Security](https://developer.apple.com/documentation/security/preventing-insecure-network-connections)
- [Apple Keychain Services](https://developer.apple.com/documentation/security/keychain-services)
- [OAuth for Native Apps, RFC 8252](https://www.rfc-editor.org/rfc/rfc8252)
- [OWASP MASVS](https://mas.owasp.org/MASVS/) and [MASTG](https://mas.owasp.org/MASTG/)
- [WCAG 2.2](https://www.w3.org/TR/WCAG22/)

Check current platform documentation for target SDK behavior and store requirements; this guide deliberately avoids fixed submission-policy claims.
