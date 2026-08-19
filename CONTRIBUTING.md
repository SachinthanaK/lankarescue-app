# Contributing

## Workflow

1. Start from an approved backlog item with acceptance criteria.
2. Branch as `feature/<topic>`, `fix/<topic>`, `docs/<topic>`, or `chore/<topic>`.
3. Keep changes focused and update tests, contracts, ADRs, and operational docs when affected.
4. Use Conventional Commits such as `feat:`, `fix:`, `docs:`, `test:`, `build:`, `ci:`, `refactor:`, or `chore:`.
5. Open a pull request using the repository template.
6. Merge only after required quality/security checks and ownership review pass.

Do not commit credentials, citizen data, tracking tokens, `.env` files, Terraform state, or kubeconfig files. Use synthetic data only.

Architecture changes require an ADR. New tools/services require a demonstrated need, ownership, security/cost assessment, and approval.

See `docs/standards/definition-of-done.md` and `docs/standards/git-workflow.md`.
