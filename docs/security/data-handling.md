# Data Handling Baseline

- Portfolio environments use synthetic data only.
- Collect only the minimum contact, location, need, people count, and description needed by the demo workflow.
- Never put tracking tokens, contact details, exact addresses, or sensitive free text into logs, events, screenshots, metrics labels, issue reports, or analytics.
- Store the citizen tracking token as a cryptographic hash; display the original only once at creation.
- Public/staff responses expose fields according to role and purpose.
- Audit records capture actor, action, previous/new state references, time, and correlation ID without duplicating unnecessary PII.
- DLQ/outbox access is restricted because payloads may contain operational data.
- Retention/deletion periods are finalized before portfolio-prod data is accepted; until then synthetic data is disposable.
- Attachments are deferred. If introduced, add type/size/content validation, access controls, retention, and malware-scanning design first.
