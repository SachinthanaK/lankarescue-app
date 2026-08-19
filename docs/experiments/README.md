# Reliability Experiments

Mandatory controlled experiments begin in Phase 13:

- API pod deletion and capacity recovery.
- k6 load spike and HPA behavior.
- notification worker outage and backlog drain.
- poison event retry, DLQ, and alert.
- Service Bus outage and outbox recovery.
- bad deployment, alert, Git rollback, and recovery.
- PostgreSQL backup restore with actual RPO/RTO measurements.

Experiments use synthetic data, approved namespaces, time/cost limits, and retained safe evidence.
