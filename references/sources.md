# Primary source index

Editorial review date: 2026-11-06. This package's prose is an original synthesis, not copied standards text. The numbered rules originate from the supplied 100-topic outline. Links support implementation review; they do not mean every rule has been independently audited or that this package meets a standard.

## Sources checked during preparation

- [OWASP Session Management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html): cookie/session design (R002–R004).
- [OWASP CSRF Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html): ambient credentials and defense in depth (R004).
- [OWASP Authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html): deny by default and per-request access control (R012).
- [OWASP Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html): maintained password hashing choices (R009).
- [OWASP Content Security Policy](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html): policy design and deployment (R011).
- [MDN Strict-Transport-Security](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Strict-Transport-Security): HTTPS-only policy and separate redirects (R001).
- [MDN TLS configuration](https://developer.mozilla.org/en-US/docs/Web/Security/Practical_implementation_guides/TLS): secure transport configuration (R014).
- [Stripe webhooks](https://docs.stripe.com/webhooks): provider verification, duplicate events and event ordering (R022).
- [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/): accessibility target and conformance criteria (R048–R049).

## Additional starting points to check for the target project

- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) for a broader application verification program.
- [OWASP MASVS](https://mas.owasp.org/MASVS/) for native mobile requirements.
- [Google Search Central](https://developers.google.com/search/docs) for metadata and indexing behavior.
- [GitHub Actions security](https://docs.github.com/en/actions/security-for-github-actions) for workflow permissions and third-party actions.
- The project's identity provider, payment provider, database, hosting and platform documentation for version-specific behavior.

Privacy, taxes, payment compliance and communications obligations must be assessed for the actual jurisdiction, business and integration. This package deliberately does not assert legal compliance or supply jurisdiction-specific legal advice.
