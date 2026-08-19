# ADR-005: Use Flux for GitOps delivery

Status: Accepted  
Date: 2026-08-20

## Context

Kubernetes desired state, environment promotion, drift reconciliation, and rollback need a reviewable source of truth separated from infrastructure provisioning and image builds.

## Decision

Use Flux v2 with the AKS-supported integration/configuration. The GitOps repository stores Kustomize desired state and immutable digests. Flux is the sole application deployment authority after Phase 10.

## Consequences

- Promotions and rollbacks are reviewable Git changes.
- CI does not need direct production cluster credentials.
- Flux availability/reconciliation, repository access, and ordering require monitoring/runbooks.
- Argo CD is not added because it duplicates the chosen deployment control plane.
