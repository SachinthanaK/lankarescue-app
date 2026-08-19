# Initial Threat Model

Status: Phase 0 baseline; update when trust boundaries or data flows change.

## Assets

- Citizen request/contact/location data and secure tracking tokens.
- Staff identities, roles, sessions, and audit history.
- PostgreSQL state, outbox/inbox records, messages, DLQs, and Blob objects.
- Git repositories, workflows, artifacts, SBOMs, ACR images, Terraform state, GitOps state, and cloud identities.
- Observability data, Backstage integrations, and `lankaops` operator context.

## Trust boundaries

- Public Internet to Gateway/API/PWA.
- Staff browser to Entra and application authorization.
- External provider data to alert ingestor.
- Pod ServiceAccount to Entra Workload Identity/Azure service.
- GitHub Actions OIDC to Azure.
- CI-produced artifact to GitOps repository and Flux.
- Operator/Backstage/CLI access to GitHub, Kubernetes, Azure, and messaging metadata.

## Principal threats and planned controls

| Threat | Planned controls |
|---|---|
| Sequential request enumeration | Separate public reference and high-entropy token; token hash at rest; generic errors/rate limits |
| Submission abuse | Validation, size limits, rate limiting, synthetic demo use, later WAF reference |
| Staff privilege escalation | Entra authentication, deny-by-default application RBAC, authorization matrix tests, audit trail |
| External alert spoofing/outage | Provider interface, attribution/timestamp, untrusted validation, coordinator verification, timeouts/fallback |
| Database/event dual-write loss | Transactional outbox, backlog metrics, retries, outage experiment |
| Duplicate business effects | Inbox uniqueness and transaction-before-acknowledgement |
| Poison messages | Schema validation, bounded retries, DLQ, alert/runbook, guarded replay |
| Secret/credential leakage | OIDC, Workload Identity, Key Vault, secret scanning, redaction, no real data |
| Overprivileged workload | Separate identities/ServiceAccounts and least-privilege RBAC with negative tests |
| Supply-chain compromise | Protected PRs, pinned actions, SAST/dependency/container/IaC scans, SBOM, immutable digest traceability |
| Unauthorized deployment | Flux authority, protected GitOps paths, no production kubectl from CI, Git audit |
| Telemetry PII/cost explosion | Field denylist, sampling/retention/cardinality rules, budgets/alerts |
| Backstage/scaffolder abuse | Authentication, minimal integrations, validated destinations/inputs, reviewed IaC/GitOps PRs |
| Unsafe CLI mutation | Read-only first, environment display, dry-run, confirmation, role checks, GitOps operation, audit output |

## Out of scope in Phase 0

Formal compliance certification, real emergency operations, government/DMC integration, active multi-region, public penetration testing, and production incident handling. These exclusions must remain visible.
