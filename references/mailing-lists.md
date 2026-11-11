# Mailing lists: subscription through suppression

Use for newsletters, product updates and marketing campaigns. Relevant rules: R015, R079, R082, R084, R086-R087. Keep marketing choices separate from required account/order notices. A purchased or scraped list is not evidence of permission. Choose a maintained email provider with suppression, delivery events, export and suitable regional processing.

## Setup and ownership

Use an owner-controlled sending domain and documented provider account. Configure SPF/DKIM and appropriate DMARC alignment with the provider's current DNS instructions; verify delivery to test inboxes. Preserve existing DNS records and avoid duplicate SPF records. Record expected volume, cost limits, retention, sender identity and support contact. Keep API credentials server-side and use provider sandbox/test audiences initially.

## Subscription lifecycle

A useful model is subscriber + list membership + consent events + suppression + campaign/delivery records. Record source, time and the notice/version presented. Minimize personal data. Lists and segments do not override global or applicable list suppression.

1. Show a short, accessible form describing what people will receive and how often. Do not preselect optional marketing or make unrelated purchases contingent on it. Validate and rate-limit on the server; avoid revealing whether another address is subscribed.
2. Use confirmation where appropriate, particularly for public signup forms: create pending membership, send a bounded confirmation message, and activate only after explicit proof. Use random expiring tokens and idempotent transitions. Scanner GETs should show a confirmation page rather than silently activate membership.
3. Provide preferences and unsubscribe without requiring login. Implement provider-supported one-click unsubscribe headers and POST behavior where required. A human-facing GET may show a confirmation/preferences page; keep destructive actions out of scanner GETs. Tokens must be scoped to the subscription operation and must not expose account access.
4. Record unsubscribes, hard bounces and complaints promptly. Verify event authenticity and handle duplicate/reordered provider events. Later delivery events must not re-enable a suppressed address. Require a new valid opt-in process for re-subscription.
5. Before each send, recheck applicable suppression and consent, including queued campaigns and retries. Deduplicate per campaign/recipient. Set frequency limits and a pause/kill control for campaigns. Already handed-off mail may not be retractable; document this boundary.
6. For imports, preview and validate rows, record permission provenance, deduplicate safely, preserve suppression and reject unsupported records. Exports need authorization and protection against spreadsheet formula injection. Segment only on permitted data; provide deletion/export and retention handling.

## Ease of use and verification

Provide form preview, sender/subject preview, test sends to designated test recipients, clear audience counts, schedule timezone, and a final campaign summary before an authorized real send. Show delivery/bounce/complaint results without claiming open tracking proves readership. Keep tracking minimal and respect preferences.

Test double signup, token expiry/replay, link scanners, unsubscribe without an account, queued send after unsubscribe, provider webhook forgery, complaints, suppression during reimport, retry duplicates and permission boundaries. Review actual message headers, DNS authentication and inbox rendering in the provider sandbox or controlled test audience. Do not send campaigns merely because the skill is invoked.

Sources: [Gmail sender guidance](https://support.google.com/mail/answer/81126), [RFC 8058 one-click unsubscribe](https://www.rfc-editor.org/rfc/rfc8058), and the chosen provider's current API and jurisdiction-specific requirements. Sender thresholds and policies change; verify them for the planned volume.
