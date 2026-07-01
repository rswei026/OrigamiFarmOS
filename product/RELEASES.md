---
title: Releases
document: RELEASES
status: Draft
version: 0.1.0
owner: Product Architecture
last_updated: 2026-07-01
---

# Releases

This log tracks each release against the phase it advances in [product/ROADMAP.md](ROADMAP.md), per [Chapter 19 — Deployment §19.5](../handbook/19-Deployment/19-Deployment.md#195-release-versioning).

## Unreleased

### Phase 0 — Engineering Repository Setup (complete)

- Ratified [CONSTITUTION.md](../CONSTITUTION.md).
- Added [CONCEPT_NOTE.md](../CONCEPT_NOTE.md).
- Completed Engineering Handbook Chapters 1-19 (Vision, Ontology, Behavioral Model, Knowledge Model 4.1-4.10, Animal Digital Twin, Feed, Dairy, Poultry, Veterinary, Inventory, Produce, Sales & Finance, UI/UX, Database, API, Offline Sync, Security, Testing, Deployment).
- Added [product/MVP_SCOPE.md](MVP_SCOPE.md), [product/ROADMAP.md](ROADMAP.md), [product/TRACEABILITY.md](TRACEABILITY.md).
- Fixed formatting defects in earlier drafts (stray code-fence wrappers, mojibake encoding, misnamed files).
- Added [ADR-009 (Technology Stack Selection)](../handbook/adr/ADR-009-Technology-Stack-Selection.md) and [ADR-010 (AI Integration Architecture)](../handbook/adr/ADR-010-AI-Integration-Architecture.md).

### Phase 1-3 — Core Farm Setup, Animal/Flock Foundation, Morning Routine MVP (first vertical slice)

Backend (`backend/`, FastAPI + PostgreSQL):

- Farm, Location, User/roles, Animal, Flock, Herd models and migrations (Ch.2, Ch.14).
- JWT auth with server-enforced role-based permissions (Ch.17).
- Generic Observation model with quality-level-derived confidence (Ch.4.3).
- Feed Item/Lot/Distribution with derived stock and a simple consumption-rate forecast (Ch.6).
- Milk recording and Egg collection, each emitting a companion Observation for correlation (Ch.7, Ch.8).
- Rule-based Knowledge Engine: Correlation Engine (health-decline and egg-decline patterns), Recommendation Engine, and a pluggable `AIProvider` (rule-based by default; a disabled-by-default OpenAI-compatible provider ready for a future hosted-or-on-premises LLM per [ADR-010](../handbook/adr/ADR-010-AI-Integration-Architecture.md)) (Ch.4.4, 4.5, 4.7, 4.10).
- Decision recording and Morning Briefing aggregation endpoint (Ch.4.6, Ch.3 §3.4).
- Seed script with realistic mixed-species Origami Farms data, including a demonstrable health-decline recommendation (Ch.18 §18.4).

Frontend (`ui/`, React + TypeScript PWA):

- Tailwind/shadcn-style design system, English/Arabic i18n with RTL layout mirroring (Ch.13).
- IndexedDB (Dexie) offline write queue with automatic sync on reconnect (Ch.16, per [ADR-009](../handbook/adr/ADR-009-Technology-Stack-Selection.md)).
- Login, Morning Briefing, Animal/Flock registration and profile with Timeline, Feed/Milk/Egg-collection/Observation quick-action dialogs, and the Recommendation review flow (accept/reject-with-reason/monitor).

Deferred to a later pass: Treatment/withdrawal periods (Ch.9), Sales & Finance (Ch.12), Produce (Ch.11), the generalized Inventory model for medicine/product (Ch.10), QR code lookup, task assignment, and the automated test suite (Ch.18). See [product/TRACEABILITY.md](TRACEABILITY.md).

## Release Template

When Phase 1 implementation begins, use this template for each release:

```
## vX.Y.Z — YYYY-MM-DD

Phase: <roadmap phase>

### Added
- ...

### Changed
- ...

### Fixed
- ...

### Handbook chapters touched
- Chapter N vX.Y.Z — <what changed and why>
```
