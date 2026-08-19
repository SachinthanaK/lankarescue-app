# Planned Application RBAC Matrix

| Capability | Citizen | Volunteer | ReliefCenterOperator | Coordinator | PlatformOperator |
|---|:---:|:---:|:---:|:---:|:---:|
| Submit request | Yes | Yes | Yes | Yes | No operational need |
| Track own request with token | Yes | Yes | Yes | Yes | No operational need |
| View verified public-safe request | Limited | Yes | Yes | Yes | Diagnostic metadata only |
| Update assigned progress | No | Assigned only | Center assignments | Yes | No |
| Manage center inventory/capacity | No | No | Own center | Yes | No |
| Verify/triage/assign/cancel | No | No | No | Yes | No |
| Verify external alerts | No | No | No | Yes | No |
| View application audit | No | No | Limited own-center events | Yes | Security/operational need only |
| View platform health/telemetry | No | No | Limited service status | Limited | Yes |
| Perform deployment/recovery operation | No | No | No | No | Guarded, authorized operations |

The matrix is deny by default and becomes enforceable/tested in Phase 11. PlatformOperator is not automatically a Coordinator; separation of duties is intentional.
