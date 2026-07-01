---
title: MVP Scope
document: MVP_SCOPE
status: Draft
version: 0.1.0
owner: Product Architecture
last_updated: 2026-07-01
depends_on:
  - ../CONCEPT_NOTE.md
  - ../handbook/01-Vision.md
---

# MVP Scope

This document is the scope-control mechanism referenced in [CONSTITUTION.md](../CONSTITUTION.md) Principle 2 and [Risk 1: Scope Creep](../CONCEPT_NOTE.md#21-risks-and-mitigation) mitigation. It is the arbiter for "is this feature in the MVP?" — not individual judgment calls made per pull request.

## The Decision Filter

Every proposed feature must pass the guiding question from [Vision §1.3](../handbook/01-Vision.md#13-the-guiding-question):

> What does the farm manager need to know and do tomorrow morning?

If a feature does not help answer this question for Origami Farms specifically, it belongs in **Later Phases** below, not in the MVP, regardless of how easy or interesting it is to build.

## Included in MVP

| Area | Handbook chapter |
|---|---|
| Farm profile, barns and locations | [Ontology (Ch. 2)](../handbook/02-Ontology.md) |
| Animal registry — cows, sheep, goats, horses | [Animal Digital Twin (Ch. 5)](../handbook/05-Animal-Digital-Twin/05-Animal-Digital-Twin.md) |
| Flock records — chickens, ducks, turkeys | [Poultry (Ch. 8)](../handbook/08-Poultry/08-Poultry-Management.md) |
| Feed inventory and distribution | [Feed (Ch. 6)](../handbook/06-Feed/06-Feed-Management.md) |
| Milk production | [Dairy (Ch. 7)](../handbook/07-Dairy/07-Dairy-Management.md) |
| Egg collection | [Poultry (Ch. 8)](../handbook/08-Poultry/08-Poultry-Management.md) |
| Health observations, treatments, vaccinations, withdrawal periods | [Veterinary (Ch. 9)](../handbook/09-Veterinary/09-Veterinary-Management.md) |
| Fresh produce harvest, product inventory | [Produce (Ch. 11)](../handbook/11-Produce/11-Produce-Management.md), [Inventory (Ch. 10)](../handbook/10-Inventory/10-Inventory-Management.md) |
| Sales, expenses, customers, suppliers | [Sales and Finance (Ch. 12)](../handbook/12-Sales-Finance/12-Sales-and-Finance.md) |
| Morning briefing, basic dashboard, basic reports | [Behavioral Model §3.4](../handbook/03-Behavioral-Model.md#34-the-daily-behavioral-loop), [Decision Intelligence §4.6](../handbook/04-Knowledge-Model/04.6-Decision-Intelligence.md) |
| Offline operation, synchronization | [Offline Synchronization (Ch. 16)](../handbook/16-Offline-Synchronization/16-Offline-Synchronization.md) |
| English and Arabic support | [UI/UX Design System §13.7](../handbook/13-UI-UX-Design-System/13-UI-UX-Design-System.md#137-bilingual-and-rtl-support) |
| Rule-based AI recommendations | [Knowledge Model (Ch. 4)](../handbook/04-Knowledge-Model/README.md) |

## MVP-Light (included only if low-cost)

- Animal photos
- Document attachments
- Basic asset register
- Simple weather note
- Product processing (cheese, labneh, yogurt, preserves)
- QR code generation
- Basic export to Excel or PDF

## Explicitly Excluded from MVP

| Excluded | Rationale | Target phase |
|---|---|---|
| Full payroll | Not needed to run daily operations; deep HR/compliance scope | Phase 4 (FarmOS Professional) |
| Full accounting system | MVP needs decision-grade profitability, not bookkeeping/tax compliance (§12.1 RULE-FIN-101) | Phase 4+ |
| IoT integration, smart collars, milk meter integration | Hardware dependency; MVP relies on manual/Level A-C observations | Phase 5 (FarmOS Platform) |
| Satellite imagery, drone monitoring | Not needed to answer "what to do tomorrow morning" | Phase 5 |
| Marketplace | Requires multi-farm/commercial infrastructure not yet built | Phase 8 (Commercial Readiness) |
| Commercial SaaS billing, multi-country compliance | Origami Farms is the only tenant in the MVP (Constitution Principle 2) | Phase 8 |
| Advanced machine learning | Rule-based recommendations must be validated first (§4.5.6 RULE-KM-502, §4.10 AI Governance) | Phase 6+ |
| Veterinary telemedicine | Out of scope; veterinarian workflow assumes in-person/phone consultation | Not currently roadmapped |
| Blockchain traceability | No demonstrated Origami Farms need | Not currently roadmapped |

See [product/ROADMAP.md](ROADMAP.md) for how these map to delivery phases.

## Changing This Document

Any addition to "Included in MVP" requires:

1. Passing the decision filter above.
2. A corresponding handbook chapter/section update (architecture before implementation, Constitution Principle 19).
3. An update to [product/TRACEABILITY.md](TRACEABILITY.md).

Removing scope from the MVP does not require the same process — reducing scope in service of shipping a focused product is always acceptable.
