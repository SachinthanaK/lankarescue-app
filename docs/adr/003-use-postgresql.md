# ADR-003: Use PostgreSQL Flexible Server

Status: Accepted  
Date: 2026-08-20

## Context

The core domain is relational and requires transactions across request state, history, audit records, outbox events, and consumer inbox records.

## Decision

Use PostgreSQL locally and Azure Database for PostgreSQL Flexible Server in Azure. Use Alembic migrations, explicit transaction boundaries, constraints, optimistic concurrency, and separate environment databases/schemas.

## Consequences

- Strong consistency and transactional outbox/inbox support.
- Managed backups and a path to zone-redundant enterprise HA.
- Portfolio cost uses an affordable tier; enterprise HA is documented separately until implemented/tested.
