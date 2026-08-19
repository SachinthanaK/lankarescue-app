# Cost Model

Status: qualitative Phase 0 baseline. Current regional price estimates and a spending ceiling are mandatory before Phase 8 apply.

## Minimal demo mode

- Docker Compose, local PostgreSQL, Service Bus emulator, local Backstage as needed.
- Azure disabled or restricted to short verification sessions.
- Purpose: application/event development and low-cost interview demos.

## Portfolio full-demo mode

- One AKS cluster with three logical namespaces.
- ACR, Service Bus Standard, PostgreSQL Flexible Server, Key Vault, Blob Storage, Azure Monitor/Application Insights/Log Analytics, Managed Prometheus/Grafana, DNS/TLS as approved.
- Purpose: Azure, Terraform, AKS, GitOps, security, observability, SRE, and platform-engineering evidence.

## Enterprise reference mode

- Architecture/cost model for Front Door/WAF, Application Gateway for Containers, private AKS/endpoints, separate subscriptions/clusters, zone redundancy, stronger monitoring, Defender, and multi-region DR.
- Short-lived proof only after separate approval; not a continuously funded requirement.

## Required controls

- Tags: project, environment, owner, managed-by, purpose, cost-center, and relevant data classification.
- Azure budget and alerts before resource apply.
- Short development log/trace retention and bounded cardinality/sampling.
- Node/pod autoscaling with defensible floors/ceilings and resource requests/limits.
- Image, artifact, backup, and log retention policies that preserve required rollback/evidence.
- Preview TTL/orphan cleanup if Phase 17 is selected.
- Documented start/stop/destroy procedures with explicit target validation.
- Daily/weekly actual cost evidence during full-demo operation.

Expensive services are never enabled only to place their logo in an architecture diagram.
