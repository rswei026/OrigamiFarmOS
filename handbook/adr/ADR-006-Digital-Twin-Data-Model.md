---
title: ADR-006 Digital Twin Data Model
adr: 006
status: Accepted
date: 2026-07-01
owner: Product Architecture
tags:
  - ontology
  - digital-twin
  - database
---

# ADR-006 — Digital Twin Data Model

## Status

Accepted

## Context

Origami Farms manages multiple species (cows, sheep, goats, horses, chickens, ducks, turkeys) plus fields, feed, medicine, and products. A naive design might create a separate table/module per species or per resource type, duplicating logic and making cross-cutting features (timelines, recommendations, cost allocation) inconsistent.

## Decision

FarmOS models every real-world object as exactly one digital twin ([Ontology §2.5](../02-Ontology.md#25-the-digital-twin-rule)), using shared entity types with a discriminator rather than per-species/per-type tables: `Animal` (with a `species` field) covers cows, sheep, goats, and horses; `Flock` (with a `species` field) covers chickens, ducks, and turkeys; a single generic Inventory Lot pattern ([Chapter 10](../10-Inventory/10-Inventory-Management.md), RULE-INV-101) covers feed, medicine, and product stock.

## Consequences

- No `cow`, `sheep`, `goat`, `horse`, `chicken`, `duck`, `turkey` tables; one `Animal` and one `Flock` table each, per RULE-ONT-102/104.
- Shared UI components (timeline, recommendation card, observation form — Chapter 13) apply uniformly across species without per-species branching.
- New species can be added by extending an enum/reference table, not by adding new tables, modules, or duplicated business logic — directly supporting Constitution Principle 16 (Mixed Farm by Design).
- Everything (observations, costs, media) attaches to the twin's single ID, satisfying RULE-ONT-101/102 and making the "Five-Minute Test" (§2.6) achievable via one timeline component.

## Alternatives Considered

### Per-Species Tables and Modules

Rejected: would require every cross-cutting feature (Chapter 4 Knowledge Model, Chapter 13 UI components, Chapter 14 schema conventions) to be reimplemented per species, directly contradicting Constitution Principle 16 and inflating the MVP scope.

### Fully Generic "Entity" Table with No Species-Specific Structure

Rejected: over-generalization would push species-specific fields (e.g., egg production percentage vs. milk yield) into unstructured JSON blobs, weakening validation (§4.3.8) and query performance (§14.6). The chosen model keeps `Animal`/`Flock` as first-class typed entities with per-domain event tables (Chapters 6-12) attached by reference.

## Related Documents

- ../02-Ontology.md
- ../05-Animal-Digital-Twin/05-Animal-Digital-Twin.md
- ../08-Poultry/08-Poultry-Management.md
- ../10-Inventory/10-Inventory-Management.md
- ../../CONSTITUTION.md
