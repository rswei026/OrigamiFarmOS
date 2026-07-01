---
title: Engineering Roadmap
document: ROADMAP
status: Draft
version: 0.1.0
owner: Product Architecture
last_updated: 2026-07-01
depends_on:
  - ../CONCEPT_NOTE.md
  - MVP_SCOPE.md
---

# Engineering Roadmap

This is the phase-by-phase engineering delivery roadmap from [CONCEPT_NOTE.md §22](../CONCEPT_NOTE.md#22-implementation-roadmap), tracked against actual repository state.

> This document tracks *delivery phases* (what gets built, in what order). The root [ROADMAP.md](../ROADMAP.md) describes the *product-market phases* (Origami Farms MVP → Optimized → Commercial → Professional → Platform) at a coarser grain. The two are complementary: Phase 0-7 here roughly correspond to root ROADMAP.md's "Phase 1 — Origami Farms Internal MVP"; Phase 8 here corresponds to root ROADMAP.md's "Phase 3 — Commercial Readiness."

## Phase 0 — Engineering Repository Setup

**Status: In Progress**

Outputs: GitHub repository, [Constitution](../CONSTITUTION.md), [Concept Note](../CONCEPT_NOTE.md), engineering handbook structure, ADR folder, [MVP scope](MVP_SCOPE.md), this roadmap, initial glossary.

- [x] GitHub repository
- [x] Constitution ratified
- [x] Concept note committed
- [x] Engineering handbook structure (Chapters 1-19)
- [x] ADR folder with initial decisions
- [x] MVP scope document
- [x] Roadmap (this document)
- [x] Initial glossary
- [ ] Backend/mobile/database scaffolding (Phase 1, deliberately not started — see [handbook/CONSTITUTION.md Principle 19](../CONSTITUTION.md))

## Phase 1 — Core Farm Setup

**Status: Planned**

Outputs: Farm profile, users and roles, locations, basic offline database, language structure, initial sync architecture.

References: [Ontology (Ch. 2)](../handbook/02-Ontology.md), [Security (Ch. 17)](../handbook/17-Security/17-Security.md), [Database Architecture (Ch. 14)](../handbook/14-Database-Architecture/14-Database-Architecture.md), [Offline Synchronization (Ch. 16)](../handbook/16-Offline-Synchronization/16-Offline-Synchronization.md).

## Phase 2 — Animal and Flock Foundation

**Status: Planned**

Outputs: Animal registry, flock registry, QR code support, animal profile, timeline, basic health status.

References: [Animal Digital Twin (Ch. 5)](../handbook/05-Animal-Digital-Twin/05-Animal-Digital-Twin.md), [Knowledge Timeline (4.8)](../handbook/04-Knowledge-Model/04.8-Knowledge-Timeline.md).

## Phase 3 — Morning Routine MVP

**Status: Planned**

Outputs: Morning briefing, feeding workflow, milk workflow, egg workflow, observation workflow, task completion.

References: [Behavioral Model §3.4](../handbook/03-Behavioral-Model.md#34-the-daily-behavioral-loop), [Feed (Ch. 6)](../handbook/06-Feed/06-Feed-Management.md), [Dairy (Ch. 7)](../handbook/07-Dairy/07-Dairy-Management.md), [Poultry (Ch. 8)](../handbook/08-Poultry/08-Poultry-Management.md).

## Phase 4 — Health and Veterinary

**Status: Planned**

Outputs: Medical records, treatments, vaccinations, withdrawal periods, health recommendations, follow-up reminders.

References: [Veterinary (Ch. 9)](../handbook/09-Veterinary/09-Veterinary-Management.md), [Recommendation Engine (4.5)](../handbook/04-Knowledge-Model/04.5-Recommendation-Engine.md).

## Phase 5 — Inventory, Produce, Sales, Expenses

**Status: Planned**

Outputs: Feed stock, medicine stock, product inventory, fresh produce harvest, simple sales, simple expenses, basic profitability.

References: [Inventory (Ch. 10)](../handbook/10-Inventory/10-Inventory-Management.md), [Produce (Ch. 11)](../handbook/11-Produce/11-Produce-Management.md), [Sales and Finance (Ch. 12)](../handbook/12-Sales-Finance/12-Sales-and-Finance.md).

## Phase 6 — Intelligence and Reports

**Status: Planned**

Outputs: Rule-based alerts, health recommendations, feed shortage forecast, production trends, daily/weekly/monthly reports, recommendation feedback loop.

References: [Knowledge Model (Ch. 4)](../handbook/04-Knowledge-Model/README.md), [Decision Intelligence (4.6)](../handbook/04-Knowledge-Model/04.6-Decision-Intelligence.md), [Knowledge Feedback Loop (4.9)](../handbook/04-Knowledge-Model/04.9-Knowledge-Feedback-Loop.md).

## Phase 7 — Origami Farms Pilot

**Status: Planned**

Outputs: Daily use on farm, worker feedback, bug fixing, workflow refinement, feature removal where unused, MVP stabilization.

References: [Testing (Ch. 18)](../handbook/18-Testing/18-Testing.md), [Deployment (Ch. 19)](../handbook/19-Deployment/19-Deployment.md).

## Phase 8 — Commercial Readiness

**Status: Not Started**

Outputs: Multi-farm support, onboarding flow, farm templates, subscription model, customer support model, commercial documentation.

This phase begins only after Phase 7 validates real value at Origami Farms, per [Constitution Principle 2](../CONSTITUTION.md) and [Vision §1.6.1](../handbook/01-Vision.md#161-origami-farms-first).

## Updating This Roadmap

Mark a phase item complete only when its handbook chapter has both an implementation and passing acceptance-criteria tests (see [Chapter 18 — Testing](../handbook/18-Testing/18-Testing.md) and [product/TRACEABILITY.md](TRACEABILITY.md)), not when code merely exists.
