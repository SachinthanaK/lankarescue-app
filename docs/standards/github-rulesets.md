# Planned GitHub Organization and Rulesets

Status: local specification; activation awaits GitHub organization, visibility, and owner/team confirmation.

## All repositories

- Default branch: `main`.
- Block deletion and force push to `main`.
- Require pull request before merge.
- Require one approval where the selected GitHub plan supports it.
- Dismiss stale approvals after new commits.
- Require conversation resolution.
- Require configured status checks and the branch to be current where appropriate.
- Require CODEOWNERS review after real user/team handles replace commented placeholders.
- Allow bypass only for a named emergency role, with an issue/audit trail.
- Enable Dependabot/security advisories, secret scanning, and push protection where the selected plan supports them.
- Disable Actions from unapproved sources and default workflow token to read-only.

## Repository-specific protected areas

| Repository/path | Intended owner |
|---|---|
| `lankarescue-app/services/` | backend maintainers |
| `lankarescue-app/apps/web/` | frontend maintainers |
| `lankarescue-infrastructure/bootstrap`, `modules/identity`, `environments` | platform/security maintainers |
| `lankarescue-gitops/clusters/portfolio-prod` | production approvers |
| `lankarescue-gitops/platform` | platform maintainers |
| `lankarescue-developer-platform/templates`, `lankaops` | developer-experience/platform maintainers |
| `lankarescue-workflows/.github/workflows` | platform maintainers |

## Planned required checks

- Application: Python/Node quality, unit/contract/integration selection, security, container build/scan/SBOM.
- Infrastructure: fmt, validate, TFLint, Checkov, trusted reviewed plan/cost when available.
- GitOps: Kustomize render, schema/policy validation, immutable image check.
- Developer platform: applicable Node/Python quality/security/build and golden-path/CLI tests.
- Workflows: YAML/action validation plus controlled consumer success/failure/security tests.

## Environments

- `dev`: trusted merge automation with minimal OIDC/RBAC.
- `staging`: promotion checks and environment-scoped identity.
- `portfolio-prod`: explicit approval, restricted branches, separate federated credential/RBAC, no direct Kubernetes apply.

## Pending decisions

- GitHub organization/owner name.
- Public versus private status during development and public-release timing.
- Actual user/team handles and emergency bypass owner.
- Available GitHub plan features.
- Merge strategy and commit-signing requirement.
- Status-check names after reusable workflows exist in Phase 7.
