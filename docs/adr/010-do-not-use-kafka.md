# ADR-010: Do not use Kafka for the planned workload

Status: Accepted  
Date: 2026-08-20

## Context

The workload needs modest-volume durable pub/sub, retry, redelivery, filters, and DLQs—not large-scale event streaming, long retention, replay analytics, or broker-platform operations.

## Decision

Use Azure Service Bus and do not add Kafka.

## Consequences

- Lower operational/cognitive cost and tighter Azure integration.
- The project cannot claim Kafka operations experience from this workload.
- Revisit only if measured requirements emerge that Service Bus cannot satisfy; a CV keyword alone is not a requirement.
