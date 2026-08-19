# LankaRescue Application

Status: **Planned — Phase 0 foundation**

LankaRescue is an educational DevOps/platform/SRE portfolio workload for community disaster-relief coordination in Sri Lanka. It is not an official emergency-response service and is not affiliated with Sri Lanka's Disaster Management Centre.

## Responsibility

This repository owns:

- the compact Next.js PWA;
- `incident-api`, `alert-ingestor`, `resource-matcher`, and `notification-worker`;
- shared event, observability, authentication, and database libraries;
- API/event contracts, database migrations, and application tests;
- product, architecture, ADR, security, SLO, runbook, recovery, experiment, cost, and portfolio-evidence documentation.

It does not own Azure resource provisioning, the desired Kubernetes environment state, reusable CI implementation, or the Backstage/`lankaops` source.

## Planned structure

```text
apps/web/
services/{incident-api,alert-ingestor,resource-matcher,notification-worker}/
libs/{events,observability,auth,database}/
tests/{integration,contract,e2e,load}/
docs/
```

## Current phase

Phase 0 contains governance and architecture only. Application implementation starts only after the Phase 0 gate is accepted.

See [`docs/backlog/roadmap.md`](docs/backlog/roadmap.md) and [`docs/adr/README.md`](docs/adr/README.md).

## Capability labels

- **Implemented** — present and demonstrable.
- **Tested** — implemented and exercised with retained evidence.
- **Reference architecture** — designed but not continuously deployed.
- **Future enhancement** — intentionally deferred.

## License

MIT. See [LICENSE](LICENSE).
