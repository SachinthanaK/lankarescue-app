# ADR-002: Use Azure Service Bus for durable events

Status: Accepted  
Date: 2026-08-20

## Context

Requests, matching, alerts, and notifications need durable asynchronous processing, topic subscriptions, retry, redelivery, and DLQ behavior at modest portfolio scale.

## Decision

Use Azure Service Bus Standard or an approved higher tier, with a domain-events topic, filtered subscriptions, peek-lock processing, DLQs, duplicate-aware producers, and idempotent consumers.

## Consequences

- Demonstrates managed Azure messaging and failure handling with less operational work than a broker cluster.
- Delivery is at least once; application design must tolerate redelivery.
- Local development can use the supported emulator where feature-compatible.
