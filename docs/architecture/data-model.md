# Phase 2 Operational Data Model

Status: **Implemented**

```mermaid
erDiagram
    DISTRICTS ||--o{ RELIEF_REQUESTS : locates
    DISTRICTS ||--o{ RELIEF_CENTERS : locates
    DISTRICTS ||--o{ VOLUNTEERS : locates
    INCIDENTS ||--o{ RELIEF_REQUESTS : groups
    RELIEF_REQUESTS ||--o{ REQUEST_STATUS_HISTORY : records
    RELIEF_REQUESTS ||--o{ ASSIGNMENTS : receives
    RELIEF_CENTERS ||--o{ RESOURCE_INVENTORY : holds
    RELIEF_CENTERS o|--o{ ASSIGNMENTS : fulfills
    VOLUNTEERS o|--o{ ASSIGNMENTS : fulfills
    APPLICATION_ROLES ||--o{ ROLE_BINDINGS : grants

    RELIEF_REQUESTS {
        uuid id PK
        string reference UK
        string token_hash
        uuid incident_id FK
        string district_code FK
        string status
        int version
        datetime created_at
        datetime updated_at
    }
    REQUEST_STATUS_HISTORY {
        uuid id PK
        uuid request_id FK
        string from_status
        string to_status
        string actor
        string reason
        int request_version
        datetime changed_at
    }
    AUDIT_EVENTS {
        uuid id PK
        string actor
        string action
        string entity_type
        string entity_id
        json previous_state
        json new_state
        string correlation_id
        datetime created_at
    }
```

## Ownership and transactions

The Incident API owns every table in this diagram. Creating a request commits the request, initial history entry, and audit event together. A lifecycle update uses an expected version and commits the state, history, and audit event in one transaction. Assigning a request commits the assignment, `ASSIGNED` transition, history, and audit together.

## Lifecycle

```text
SUBMITTED -> TRIAGED -> VERIFIED -> ASSIGNED -> IN_PROGRESS -> COMPLETED
     |          |          |           |              |
     +----------+----------+-----------+--------------+-> CANCELLED
                +----------+-> REJECTED
```

Completed, rejected, and cancelled requests are terminal. Rejection and cancellation require a reason.

## Index intent

- `reference` is unique for citizen lookup.
- `(status, priority, created_at)` supports the operational queue.
- `(district_code, status)` supports district coordination.
- `(request_id, changed_at)` supports ordered history.
- center/resource, volunteer availability, assignment, role binding, and audit lookup indexes match their compact Phase 2 endpoints.

