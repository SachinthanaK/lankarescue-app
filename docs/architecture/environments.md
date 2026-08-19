# Environment Architecture

| Concern | Local | Dev | Staging | Portfolio prod | Enterprise reference |
|---|---|---|---|---|---|
| Runtime | Docker Compose | Shared AKS | Shared AKS | Shared AKS | Separate clusters/subscriptions |
| Namespace | local | `lankarescue-dev` | `lankarescue-staging` | `lankarescue-prod` | dedicated |
| Data | local synthetic | separate DB/schema | separate DB/schema | separate synthetic DB/schema | dedicated HA data services |
| Messaging | emulator | separate entities | separate entities | separate entities | dedicated as required |
| Deployment | local | Flux | same-digest promotion | approved same-digest promotion | enterprise controls |

Namespace isolation is a portfolio cost choice, not equivalent to enterprise subscription/cluster isolation. The implemented architecture omits Front Door, Application Gateway for Containers, multi-region, Redis, and Defender for Containers unless later approved.
