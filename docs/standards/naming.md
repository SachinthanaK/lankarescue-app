# Naming Standards

## Git and code

- Repositories: `lankarescue-<responsibility>`.
- Branches: `feature/<topic>`, `fix/<topic>`, `docs/<topic>`, `chore/<topic>`.
- Python packages/modules: lower snake case; classes: PascalCase.
- Events: `<BusinessEvent>.v<major>`, for example `ReliefRequestCreated.v1`.
- Container repositories: lower kebab case; tags: `sha-<short-commit>`; deployments prefer digest.

## Kubernetes

- Namespaces: `lankarescue-dev`, `lankarescue-staging`, `lankarescue-prod`.
- Workloads/Services/ServiceAccounts use the component name.
- Required labels include application, component, environment, owner, and managed-by.

## Azure

Use deterministic names within service limits and a common model: resource type, project, environment, region/instance where required. Final abbreviations/region codes are approved before Terraform implementation. Required tags: project, environment, owner, managed-by, purpose, cost-center, and relevant data classification.
