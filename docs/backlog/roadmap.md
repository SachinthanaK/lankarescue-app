# Prioritized Roadmap

Status: Phase 0 planning baseline.

## Portfolio releases

| Release | End phase | Demonstrable outcome |
|---|---:|---|
| A | 5 | Working local application, events, reliability patterns, and containers |
| B | 10 | Terraform/Azure/AKS, reusable CI, Flux promotion, and rollback |
| C | 13 | Observability, SLOs, alerts, runbooks, failure/restore evidence |
| D | 16 | Backstage, golden path, and `lankaops`; DevOps-job-ready |
| E | selected 17 | Optional preview, WAF proof, AWS lab, or advanced DR |

## Delivery backlog

| Priority | Phase | Epic | Gate evidence |
|---|---:|---|---|
| P0 | 0 | Five repositories, standards, ADRs, architecture, backlog | clean local repos, docs render, ownership/rules spec |
| P0 | 1 | Compact English PWA and four service skeletons | submit/track demo and four health endpoints |
| P0 | 2 | PostgreSQL model and request lifecycle | migrations, state transition/audit tests |
| P0 | 3 | Versioned Service Bus event architecture | schemas, routing, correlation, provider failure |
| P0 | 4 | Transactional outbox and idempotent inbox | outage and duplicate/restart tests |
| P0 | 5 | Hardened containers and local Compose | non-root inspection and full local flow |
| P0 | 6 | Risk-based automated test platform | stable unit/integration/contract/E2E evidence |
| P0 | 7 | Reusable CI workflows and required checks | passing and intentionally failing security gates |
| P0 | 8 | Terraform bootstrap and affordable Azure platform | redacted plan, apply/idempotence, inventory/cost |
| P0 | 9 | AKS/Kustomize/Gateway deployment | healthy routes, security contexts, network denial |
| P0 | 10 | Flux, same-digest promotion, drift, rollback | reconciliation and bad-release recovery recording |
| P0 | 11 | OIDC, Workload Identity, Key Vault, RBAC | allowed/denied identity and rotation tests |
| P0 | 12 | Metrics, logs, traces, four dashboards | correlated trace and exported dashboards |
| P0 | 13 | SLOs, alerts, runbooks, experiments, restore | alert/runbook links, HPA/DLQ/outbox/restore evidence |
| P1 | 14 | Backstage service catalog and operational views | catalog/component/TechDocs/Kubernetes demo |
| P1 | 15 | Python-worker golden path | generated repo passes CI and validates manifests |
| P1 | 16 | Safe `lankaops` CLI | doctor/status and guarded GitOps recovery demo |
| P2 | 17 | Individually selected advanced feature | approved cost/security/cleanup/evidence gate |

P0 indicates required foundation/delivery/SRE work; P1 indicates core platform-engineering completion after stability; P2 is optional differentiation.

## Phase 0 checklist

- [x] Local repository directories and governance files created.
- [x] Responsibility boundaries documented.
- [x] Documentation taxonomy, initial diagrams, standards, threat model, cost model, and ADRs created.
- [x] Prioritized roadmap and capability labels defined.
- [ ] GitHub organization, visibility, owner/team handles, hosted repositories, labels, rulesets, issue boards, and security-advisory URLs confirmed/configured.
- [ ] Active CODEOWNERS patterns enabled after handles exist.
- [ ] Phase 0 evidence review accepted.

## Approval boundaries

Phase 0 authorizes no application implementation, external provider connection, cloud resource, GitHub-hosted repository, paid feature, load/failure test, destructive action, or Phase 17 work.
