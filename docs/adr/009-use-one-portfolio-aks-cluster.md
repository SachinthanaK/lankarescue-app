# ADR-009: Use one AKS cluster for portfolio environments

Status: Accepted  
Date: 2026-08-20

## Context

Three continuously running clusters would impose disproportionate cost on an individual portfolio while dev, staging, and promotion behavior still need demonstration.

## Decision

Use one AKS cluster with `lankarescue-dev`, `lankarescue-staging`, and `lankarescue-prod` namespaces plus separate service accounts, identities, configuration, data/schema, messaging entities, storage scope, and telemetry dimensions where practical.

## Consequences

- Affordable environment-promotion demonstration.
- Cluster/control-plane failures affect all environments and namespace isolation is not an enterprise boundary.
- The enterprise reference architecture uses stronger subscription/cluster/private isolation.
