# Optional end-to-end encrypted content

Use only when the product needs messages or files that its server/operator cannot decrypt. Most login, shopping and newsletter features need HTTPS, secure credential handling and controlled storage rather than end-to-end content encryption. Explain that distinction before selecting this module.

## Design before implementation

Define the participants, devices, adversaries and metadata that remain visible. Specify whether the promise covers messages, attachments, backups, search indexes, notifications and exports. List the loss/recovery experience and what happens after device compromise. If the server can silently recover plaintext, do not claim it cannot decrypt content.

Choose a maintained, externally reviewed protocol/library for the use case. Review its supported platforms, update policy and limitations; do not compose a new protocol from encryption primitives. Multi-party membership, device identity, key verification, authenticated encryption, nonce management, key rotation and replay resistance must come from a coherent design. Standards are not a substitute for a maintained implementation.

Define adding/removing devices, verifying new devices/contacts, revoking lost devices, member changes and history access. Explain that revocation cannot erase plaintext or keys a recipient already obtained. Decide whether users hold recovery keys or accept unrecoverable data loss; protect backup keys separately from ciphertext. Account password reset must not silently bypass the content-encryption promise.

Protect keys on endpoints using platform facilities; avoid keys/plaintext in analytics, crash logs, push messages or server-side previews. For browser clients, account for XSS and malicious code delivery: a server that changes client code can undermine endpoint secrecy. Document these limits clearly.

## Verification and release

Test interoperability with official test vectors, tampered/replayed ciphertext, unauthorized devices, lost-device recovery, member removal and backup restore. Inspect server storage and captured traffic for plaintext/key leakage using synthetic data. Have the protocol integration and threat model reviewed by someone qualified before making security claims. Keep this feature unresolved if that review or required tests are unavailable. Do not describe this toolkit's checklist as a cryptographic audit.

Starting points: [OWASP Cryptographic Storage](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html), [Messaging Layer Security RFC 9420](https://www.rfc-editor.org/rfc/rfc9420), and the selected protocol's maintained implementation documentation. MLS is a group-messaging protocol reference, not a universal file-encryption recipe.
