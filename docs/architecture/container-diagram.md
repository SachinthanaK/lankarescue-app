# Container Architecture

Status: **Approved design; not implemented**

```mermaid
flowchart TB
    U[Browser] --> GW[Gateway API]
    GW --> W[web: Next.js PWA]
    GW --> API[incident-api: FastAPI]
    API --> PG[(PostgreSQL)]
    API --> BL[Blob Storage]
    API --> OB[(outbox_events)]
    OB --> SB[Service Bus Topic]
    P[Alert Providers] --> AI[alert-ingestor]
    AI --> SB
    SB --> RM[resource-matcher]
    SB --> NW[notification-worker]
    RM --> SB
    NW --> SB
    API --> OT[OpenTelemetry]
    AI --> OT
    RM --> OT
    NW --> OT
```

Service boundary rules:

- `incident-api` owns incidents, requests, lifecycle, centers/resources, assignments, audit records, and the outbox publisher.
- `alert-ingestor` owns provider adapters, normalization, attribution, and alert publication.
- `resource-matcher` owns deterministic match proposals, not final assignment authority.
- `notification-worker` owns delivery adapters and outcomes.
- No separate audit, authentication, reporting, profile, attachment, scheduling, or analytics service is planned.
