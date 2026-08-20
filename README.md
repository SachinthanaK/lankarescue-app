# LankaRescue Application

Status: **Phase 1 local MVP implemented and tested**

LankaRescue is an educational DevOps, platform-engineering, and SRE portfolio workload for community disaster-relief coordination in Sri Lanka. It is not an official emergency-response service and is not affiliated with Sri Lanka's Disaster Management Centre.

## Implemented in Phase 1

- compact mobile-first Next.js PWA;
- citizen relief-request form and private status tracking;
- FastAPI services for incidents, alert ingestion, resource matching, and notifications;
- secure token hashing, correlation IDs, JSON logs, health endpoints, metadata, and OpenAPI;
- local-only staff queue and mock alert provider;
- automated Python and web quality gates.

## Repository structure

```text
apps/web/                         Next.js frontend
services/incident-api/            Relief-request HTTP API
services/alert-ingestor/          Alert-provider adapters
services/resource-matcher/        Resource-matching worker
services/notification-worker/     Notification worker
libs/{events,observability,auth,database}/
scripts/                          Local run and verification commands
docs/                             Architecture, security, runbooks, and evidence
```

## Run locally

See [`docs/local-development.md`](docs/local-development.md). The short path after first setup is:

```powershell
.\scripts\run-local.ps1
```

Then open `http://localhost:3000` and `http://localhost:8000/docs`.

## Current boundaries

Phase 1 data is in memory, the UI is English-only, and staff access is a local demo. Do not use this application for real emergencies or real personal data. PostgreSQL, identity, asynchronous messaging, containers, Azure, Kubernetes, GitOps, and platform engineering are delivered in later phases.

## Evidence and roadmap

- [`docs/portfolio-evidence/phase-1-local-mvp.md`](docs/portfolio-evidence/phase-1-local-mvp.md)
- [`docs/backlog/roadmap.md`](docs/backlog/roadmap.md)
- [`docs/adr/README.md`](docs/adr/README.md)

## License

MIT. See [LICENSE](LICENSE).
