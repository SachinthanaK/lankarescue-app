# ADR-011: Separate implemented and enterprise reference architectures

Status: Accepted  
Date: 2026-08-20

## Context

An enterprise topology with Front Door, WAF, Application Gateway for Containers, private clusters/endpoints, separate subscriptions, multi-region DR, Defender, and HA data services is valuable design evidence but expensive to run continuously.

## Decision

Maintain two explicitly labelled architectures. The implemented portfolio architecture uses one AKS cluster and affordable managed services. The enterprise architecture is labelled reference unless individually provisioned and tested.

## Consequences

- Maximizes architecture value without false claims or permanent expense.
- README/evidence must use honest capability labels.
- A reference target such as RPO/RTO is not presented as achieved until actual test records exist.
