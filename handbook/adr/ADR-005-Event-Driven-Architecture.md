---
title: ADR-005 Event-Driven Architecture and State Derivation
adr: 005
status: Accepted
date: 2026-07-01
owner: Product Architecture
tags:
  - architecture
  - events
  - database
---

# ADR-005 — Event-Driven Architecture and State Derivation

## Status

Accepted

## Context

Farm state (an animal's health status, remaining feed stock, current production trend) changes constantly and is queried from many places (Morning Briefing, timelines, reports, recommendations). A conventional mutable-record model, where these values are directly updated in place, would make corrections indistinguishable from original entries and break the auditability required by Constitution Principle 4 (Event Driven) and Principle 15 (Traceability).

## Decision

FarmOS records all meaningful farm activity as immutable events (registration, feeding, milking, egg collection, observation, treatment, sale, expense, inventory movement — [Behavioral Model §3.2](../03-Behavioral-Model.md#32-the-governing-rule-nothing-changes-without-an-event)). Current-state values are always derived projections computed from event history, never independently mutable fields ([Database Architecture §14.4](../14-Database-Architecture/14-Database-Architecture.md#144-event-sourced-vs-projected-tables), RULE-BM-102, RULE-DB-102). Corrections are new events referencing the original, never edits or deletions (RULE-BM-101).

## Consequences

- Every event table is append-only; UPDATE is not used for business-meaning fields (§14.3).
- Every derived/current-state value must be reproducible by replaying its source event(s); if it cannot be, the schema is wrong (RULE-DB-102).
- Offline-first synchronization becomes simpler because most writes are additive events, sidestepping most last-write-wins conflicts (§16.4).
- The event log itself serves as the audit trail (Chapter 17 §17.7), avoiding a separately maintained audit-log system.

## Alternatives Considered

### Mutable Records with a Bolted-On Audit Log

Rejected: a parallel audit log can drift from the actual mutable state and does not naturally support offline sync or knowledge-lifecycle traceability (Chapter 4).

### Full Event Sourcing with Replay-Only State (No Materialized Projections)

Rejected for the MVP: recomputing every view from the full event log on every read would be too slow for tablet-scale queries (e.g., a multi-year animal timeline). Materialized/cached projections are allowed, provided they remain recomputable from source events (§14.4).

## Related Documents

- ../03-Behavioral-Model.md
- ../14-Database-Architecture/14-Database-Architecture.md
- ../16-Offline-Synchronization/16-Offline-Synchronization.md
- ../../CONSTITUTION.md
