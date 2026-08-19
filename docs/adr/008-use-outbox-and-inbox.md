# ADR-008: Use transactional outbox and idempotent inbox

Status: Accepted  
Date: 2026-08-20

## Context

A database commit and message publication cannot be made atomic through an unsafe dual write. Service Bus redelivery can repeat processing.

## Decision

Write domain state and `outbox_events` in one PostgreSQL transaction. Publish asynchronously with retries/metrics/retention. Consumers record `processed_messages(event_id, consumer_name, processed_at)` in the same transaction as their business effect and acknowledge afterward.

## Consequences

- A committed request retains an event pending publication.
- Duplicate delivery produces one effective business result.
- Operational work includes backlog metrics, cleanup, DLQ/replay controls, and failure tests.
- Claims use “at least once” and “effectively once business processing,” never “exactly once delivery.”
