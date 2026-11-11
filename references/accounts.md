# Accounts: signup through recovery

Use for user accounts, administrative access and authenticated APIs. Relevant rules: R002-R012, R017-R020, R086, R089. Prefer a maintained identity integration; choose cookie sessions for suitable web apps and platform-appropriate native flows. A password is hashed for verification, not encrypted for later retrieval. HTTPS protects transport; it is not end-to-end encrypted user content.

## Decide and configure

Record who may register, required verification, roles/tenants, session lifetime, account linking, recovery and deletion policy. Avoid collecting identity data without a product need. Configure exact development, preview and production callback URLs in the provider; avoid wildcard redirects. Keep provider secrets on the server and separate environments. Explain expected cost and account ownership before provisioning a paid service.

## Implement the journey

- Signup: accessible labels, autofill and password-manager support; offer supported passkeys where appropriate. Do not block paste or invent arbitrary password composition rules. Validate server-side, rate-limit abuse and use neutral responses where account existence is sensitive.
- Verification: bounded, expiring proof of control; repeated sends must not enable mail bombing. Make resend, expired-token and already-verified states understandable. Email verification alone does not grant privileged access.
- Login: managed credential verification or maintained password hashing with current reviewed parameters; no plaintext passwords in logs, storage or support tools. Apply rate limits with recovery that avoids permanent denial of service. Require stronger authentication for sensitive actions based on risk.
- Sessions: rotate after authentication/privilege changes, invalidate on logout, and define reauthentication and revocation after password/email/factor changes. Enforce authorization on every object, field and tenant operation independently of login.
- Recovery: neutral request response, single-use expiring random tokens protected at rest, trusted-origin reset links, no token logging and no state change on a scanner's GET. Revoke or offer revocation of existing sessions according to risk. Notify the owner of meaningful security changes. Do not auto-link identities solely because email strings match.
- Account settings: verify changes to email and authentication factors, protect recovery codes, support deletion/export as applicable, and show useful session/device controls. Test data retention exceptions and revoked access after deletion.

## Acceptance checks

Test new and existing accounts; wrong/expired/replayed tokens; invalid callback targets; password reset races; logout on multiple devices; recovery with MFA; and user A reading/modifying user B's data. Test cookies and CSRF in browsers, native OAuth cancellation/PKCE and device storage, keyboard navigation and screen readers. Capture synthetic evidence without credential values.

Read current [OWASP Authentication](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html), [Forgot Password](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html), [Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html), and the selected provider's documentation when implementing.
