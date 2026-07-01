---
title: ADR-002 Offline-First and Tablet-First Architecture
adr: 002
status: Accepted
date: 2026-07-01
owner: Product Architecture
tags:
  - architecture
  - offline
  - mobile
---

# ADR-002 — Offline-First and Tablet-First Architecture

## Status

Accepted

## Context

Origami Farms' barns, stables, and fields frequently lack reliable connectivity. A cloud-dependent architecture would make FarmOS unusable exactly when and where it is needed most. The primary device is also a tablet used standing up, often one-handed, not a desktop or a phone.

## Decision

FarmOS is built local-first: a local SQLite database on the tablet is the primary read/write target for all critical workflows (feeding, milking, egg collection, health observation, treatment, inventory, sales, expenses — concept note §4.2), with an event-based sync queue reconciling to a central PostgreSQL database whenever connectivity is available ([Chapter 16 — Offline Synchronization](../16-Offline-Synchronization/16-Offline-Synchronization.md)). The mobile client targets Android tablets first (Flutter or equivalent cross-platform framework, per concept note §14), with every screen required to pass the one-hand barn test ([Chapter 13 §13.2](../13-UI-UX-Design-System/13-UI-UX-Design-System.md#132-the-one-hand-barn-test)).

## Consequences

- No workflow screen may block on a network call to confirm a save (§16.2 RULE-SYNC-101).
- All entity IDs must be client-generatable (§14.5 RULE-DB-103) so offline creation never needs a server round-trip.
- Conflict resolution favors preserving both conflicting events over silent overwrite (§16.4 RULE-SYNC-102), since offline-first architectures cannot assume a single linear write order.
- UI components default to large touch targets, minimal typing, and QR-first lookup (Chapter 13) rather than desktop-style dense information layouts.

## Alternatives Considered

### Cloud-First with Offline Caching as an Afterthought

Rejected: caching read data offline does not solve the core problem of recording new events (feeding, milking, treatments) without connectivity, which is the majority of daily farm activity.

### Native Android-Only (No Cross-Platform Framework)

Rejected for the MVP: a cross-platform framework (Flutter) supports the desktop/web secondary access channel (concept note §14) without a second codebase, while Android tablet remains the primary target.

## Related Documents

- ../01-Vision.md
- ../03-Behavioral-Model.md
- ../16-Offline-Synchronization/16-Offline-Synchronization.md
- ../13-UI-UX-Design-System/13-UI-UX-Design-System.md
- ../../CONSTITUTION.md
