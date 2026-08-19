# Git Workflow and Repository Rules

- `main` must remain releasable and protected.
- No direct push, force push, or branch deletion on `main` after hosted rules are enabled.
- Pull requests require passing quality/security checks, resolved conversations, and at least one approval where the GitHub plan permits it.
- Production GitOps paths require ownership approval.
- Conventional Commits communicate intent; releases use semantic versioning where applicable.
- Rebase or squash policy will be selected when the hosted organization is confirmed; history must retain issue/PR traceability.
- Exceptions require a linked issue with owner, reason, expiry, and remediation.

## Planned labels

```text
type:bug, type:feature, type:docs, type:security, type:infrastructure,
type:gitops, type:ci, type:platform, status:triage, status:ready,
status:blocked, priority:p0, priority:p1, priority:p2,
level:1 through level:6, capability:implemented, capability:tested,
capability:reference, capability:future
```
