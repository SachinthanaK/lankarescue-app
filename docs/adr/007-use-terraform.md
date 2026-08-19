# ADR-007: Use Terraform for cloud infrastructure

Status: Accepted  
Date: 2026-08-20

## Context

Azure infrastructure must be reproducible, reviewable, modular, policy checked, and separate from Kubernetes workload state.

## Decision

Use Terraform modules and environment compositions. Bootstrap Azure Blob remote state separately, use Microsoft Entra data-plane authentication/RBAC, distinct state keys, locking, versioning/protection, and reviewed plans.

## Consequences

- Infrastructure changes gain traceability, drift detection, and reusable modules.
- State is sensitive and requires strong access/backup controls.
- Unavoidable manual actions must be documented and reconciled.
- Terraform does not manage application Deployments owned by Flux.
