# Event and Reliability Flow

Status: **Approved design; not implemented**

```mermaid
sequenceDiagram
    participant C as Citizen
    participant API as incident-api
    participant DB as PostgreSQL
    participant P as Outbox Publisher
    participant SB as Service Bus
    participant M as Matcher
    participant N as Notification

    C->>API: Submit request
    API->>DB: Begin transaction
    API->>DB: Save request + audit + outbox
    API->>DB: Commit
    API-->>C: Reference + tracking token
    P->>DB: Claim unpublished event
    P->>SB: Publish ReliefRequestCreated.v1
    SB->>M: At-least-once delivery
    M->>DB: Business effect + inbox record
    M->>SB: Acknowledge after commit
    SB->>N: NotificationRequested.v1
```

Guarantees:

- A committed request cannot silently lose its intended event because request/outbox share a transaction.
- Consumers use `processed_messages(event_id, consumer_name, processed_at)` and acknowledge after their database transaction.
- The platform claims effectively-once business processing over at-least-once messaging, never exactly-once delivery.
- Event contracts use small versioned JSON Schemas and automated compatibility tests; no schema registry is planned.
