# ADR-004: Use reusable GitHub Actions

Status: Accepted  
Date: 2026-08-20

## Context

The project must demonstrate CI/CD, security gates, reusable developer tooling, OIDC, immutable artifact traceability, and support for multiple repositories.

## Decision

Use versioned reusable workflows in `lankarescue-workflows` and thin caller workflows in consumers. Use least permissions, safe triggers, OIDC for trusted Azure access, protected environments, and required checks.

## Consequences

- Shows internal CI platform design rather than copied pipelines.
- Workflow interfaces require versioning, testing, and consumer migration discipline.
- GitHub Actions builds/promotes artifacts but never owns live production Kubernetes apply authority.
