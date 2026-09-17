# Data Classification and Retention

## Classification

| Data | Classification | Examples | Handling |
|---|---|---|---|
| Public reference data | Public | districts, center name after approval | safe for public display when explicitly selected |
| Operational data | Internal | status, priority, inventory quantity, assignment state | staff-purpose access; avoid public analytics |
| Personal data | Confidential | contact value, precise location, volunteer identity | encrypt in transit/at rest, minimize responses, never log |
| Security credential | Restricted | citizen tracking token | show once, hash before storage, never log or place in URLs |
| Audit data | Restricted | actor, action, state references, correlation ID | append-oriented access, no duplicated contact/free text |

## Phase 2 retention policy

Portfolio environments accept synthetic data only. Their databases are disposable and should be reset after demonstrations. Before any non-synthetic environment is approved, the product owner must define jurisdiction-appropriate retention periods, deletion/legal-hold rules, data-subject handling, and access review.

Provisional design targets for later policy approval:

- citizen contact details: remove or irreversibly anonymize after the operational need and approved retention window end;
- request operational history: retain only as long as incident review and accountability require;
- audit events: retain longer than mutable operational records, with restricted access and integrity monitoring;
- expired role bindings and volunteer availability: remove promptly when access or engagement ends;
- backups and exported evidence: follow the same deletion schedule and contain synthetic/redacted data only.

These are design constraints, not a claim of legal compliance.

