# GitHub Organization and Active Repository Protection

Status: active across five public repositories owned by `@SachinthanaK` as of 2026-08-20.

## All repositories

- Default branch: `main`.
- Block deletion and force push to `main`.
- Require a pull request before merge; approval count is initially zero because one account cannot approve its own PR. Enable a second-person approval when collaborators exist.
- Dismiss stale approvals after new commits.
- Require conversation resolution.
- Require configured status checks and the branch to be current where appropriate.
- CODEOWNERS currently assigns `@SachinthanaK`; required CODEOWNERS review remains off until a separate reviewer/team exists.
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

## Deferred tightening

- Replace the temporary single owner with real teams if collaborators join.
- Require at least one independent approval when a second reviewer exists.
- Add named required status checks after reusable workflows exist in Phase 7.
- Re-evaluate commit-signing requirements before the first release.
- Configure protected GitHub environments and OIDC identities in their approved later phases.