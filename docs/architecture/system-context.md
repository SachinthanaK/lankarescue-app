# System Context

Status: **Approved design; not implemented**

```mermaid
flowchart LR
    CIT[Citizen] --> LR[LankaRescue]
    STAFF[Volunteer / Relief Center / Coordinator] --> LR
    OP[Platform Operator] --> LR
    EXT[Mock / Weather / Public Sources] --> LR
    LR --> EMAIL[Email / Operational Webhook]
    LR --> AZ[Azure Platform Services]
    DEV[Developer] --> DP[Backstage / GitHub / lankaops]
    DP --> LR
```

LankaRescue accepts relief requests, supports staff verification/assignment, ingests non-authoritative alert information, proposes resource matches, produces notifications, and records auditable actions. It is an educational portfolio workload, not an official emergency service.

Trust assumptions:

- External provider data is untrusted, attributed, time stamped, and non-critical to platform availability.
- Citizens do not require accounts; secure tracking tokens protect lookup.
- Staff authenticate through Microsoft Entra and receive explicit application roles.
- Portfolio environments contain synthetic data only.
