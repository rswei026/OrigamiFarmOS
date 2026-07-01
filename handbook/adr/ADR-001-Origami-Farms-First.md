---
title: ADR-001 Origami Farms First
adr: 001
status: Accepted
date: 2026-07-01
owner: Product Architecture
tags:
  - scope
  - product-strategy
---

# ADR-001 — Origami Farms First

## Status

Accepted

## Context

FarmOS could be designed from the outset as a generic, configurable, multi-farm commercial product, or as a focused system solving Origami Farms' real operational problems first. Designing for hypothetical future customers before the first customer is proven risks scope creep, delayed delivery, and a product shaped by guesses rather than real use (concept note §21, Risk 1).

## Decision

FarmOS shall be built first, and specifically, for Origami Farms. Every MVP feature must pass the test in [handbook/01-Vision.md §1.3](../01-Vision.md#13-the-guiding-question): would this help run Origami Farms better tomorrow morning? Commercialization (multi-farm support, onboarding, subscription billing) is deferred to Phase 8 ([product/ROADMAP.md](../../product/ROADMAP.md)) and only pursued after Phase 7 (Origami Farms Pilot) validates real value.

## Consequences

- No MVP feature is justified by "other farms might want this" alone.
- The schema carries `farm_id` from day one (§14.3) to avoid a costly migration later, without building multi-tenant features early.
- The MVP scope document ([product/MVP_SCOPE.md](../../product/MVP_SCOPE.md)) is the arbiter of what belongs in this phase.
- Product decisions favor Origami Farms' actual mixed-species operation over generic configurability.

## Alternatives Considered

### Build a Generic Multi-Farm Product from Day One

Rejected: adds configuration complexity and delays real-world validation, with no farm yet proven to need it.

### Build Origami-Specific, Hard-Coded Assumptions Everywhere

Rejected: would make the eventual Phase 8 commercialization effectively a rewrite. The mixed-farm ontology (Constitution Principle 16) is generalized enough to serve other farms later without being built *for* them now.

## Related Documents

- ../01-Vision.md
- ../../CONSTITUTION.md
- ../../product/MVP_SCOPE.md
- ../../product/ROADMAP.md
