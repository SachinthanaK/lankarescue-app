# ADR-001: Use AKS as the implemented Kubernetes platform

Status: Accepted  
Date: 2026-08-20

## Context

The portfolio must demonstrate Azure, Kubernetes operations, workload identity, GitOps, observability, scaling, failure recovery, and infrastructure automation without building a Kubernetes distribution.

## Decision

Use Azure Kubernetes Service for the implemented cloud environment. Use a cost-aware Standard cluster design selected at Phase 8 after region, quota, and pricing validation.

## Consequences

- Strong Azure/Kubernetes portfolio evidence and integration with ACR, Workload Identity, Monitor, Prometheus, and Flux.
- Requires active cost, upgrade, node, network, and security management.
- EKS remains a small optional portability lab, not a second full platform.
