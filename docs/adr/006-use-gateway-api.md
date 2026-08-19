# ADR-006: Use Kubernetes Gateway API

Status: Accepted  
Date: 2026-08-20

## Context

The platform needs portable Kubernetes-native HTTP routing aligned with the current AKS direction and must not begin a new implementation on retiring ingress-nginx patterns.

## Decision

Use Kubernetes Gateway API and the affordable AKS application-routing implementation for the portfolio environment. Document Application Gateway for Containers plus WAF as an enterprise reference option.

## Consequences

- Uses current role-oriented Gateway/HTTPRoute resources.
- GatewayClass/provider-specific capabilities must be isolated and documented.
- Front Door and Application Gateway for Containers are not continuous portfolio requirements.
