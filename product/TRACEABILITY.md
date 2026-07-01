---
title: Traceability Matrix
document: TRACEABILITY
status: Draft
version: 0.1.0
owner: Product Architecture
last_updated: 2026-07-01
depends_on:
  - ../handbook/18-Testing/18-Testing.md
---

# Traceability Matrix

Per [Chapter 18 — Testing §18.1](../handbook/18-Testing/18-Testing.md#181-purpose) (RULE-TEST-101), every handbook chapter's acceptance criteria must be traceable to implementation and test evidence. This document is that trace, maintained at chapter granularity; individual RULE-/REQ- identifiers are traced within each chapter's own "Acceptance Criteria" section.

A first vertical slice through Phases 1-3 was implemented and manually verified end-to-end (backend: `backend/app/`, frontend: `ui/src/`) in this pass. Automated tests (per [Chapter 18](../handbook/18-Testing/18-Testing.md) RULE-TEST-101/102) do not exist yet — "Verified" below means manually demonstrated (API calls and/or browser-driven), not automated-test-covered; this table should be updated again once the automated suite in Chapter 18 lands.

| Chapter | Document ID | Roadmap phase | Implementation | Test evidence | Status |
|---|---|---|---|---|---|
| 1. Vision | FM-HB-01 | Phase 0 | N/A (foundational) | N/A | Drafted |
| 2. Ontology | FM-HB-02 | Phase 1-2 | `backend/app/models/` (Farm, Location, Animal, Flock, Herd) | Manually verified via seed + API + UI | Verified (Animal/Flock/Location); Herd model only, no UI yet |
| 3. Behavioral Model | FM-HB-03 | Phase 1-3 | Event-sourced Observation/MilkRecord/EggCollection/FeedDistribution; role table (`app/api/deps.py`) | Manually verified (timeline replay, 403 for unauthorized role) | Implemented (offline conflict handling untested - single-writer only so far) |
| 4.1 Purpose and Philosophy | FM-HB-04.1 | Phase 6 | Realized by the Knowledge Engine below | Manually verified | Implemented |
| 4.2 Knowledge Lifecycle | FM-HB-04.2 | Phase 6 | `app/services/knowledge_engine.py` | Manually verified end-to-end (health-decline + egg-decline) | Verified |
| 4.3 Observation Model | FM-HB-04.3 | Phase 3 | `app/models/observation.py`, `app/services/observations.py` | Manually verified | Verified |
| 4.4 Correlation Engine | FM-HB-04.4 | Phase 6 | `app/services/correlation.py` (2 MVP patterns) | Manually verified via seed data + API | Verified |
| 4.5 Recommendation Engine | FM-HB-04.5 | Phase 6 | `app/services/recommendation.py` | Manually verified | Verified |
| 4.6 Decision Intelligence | FM-HB-04.6 | Phase 6 | `app/api/v1/recommendations.py` (accept/reject/monitor/...) | Manually verified via UI (accept flow) | Implemented (Reviews are just status filters so far - no dedicated Weekly/Monthly/Quarterly aggregation) |
| 4.7 Explainable AI | FM-HB-04.7 | Phase 6 | `app/services/ai_provider.py` (`RuleBasedProvider`) | Manually verified (explanation text rendered in UI) | Verified |
| 4.8 Knowledge Timeline | FM-HB-04.8 | Phase 2 | `app/services/timeline.py`, `ui/src/components/farmos/Timeline.tsx` | Manually verified in browser | Verified |
| 4.9 Knowledge Feedback Loop | FM-HB-04.9 | Phase 6 | — | — | Drafted (not implemented) |
| 4.10 AI Governance | FM-HB-04.10 | Ongoing (governance) | `app/services/ai_provider.py` (`OpenAICompatibleProvider`, disabled by default) | Structural review only | Implemented (governed provider abstraction in place, not exercised) |
| 5. Animal Digital Twin | FM-HB-05 | Phase 2 | `app/models/animal.py`, `app/api/v1/animals.py`, `ui/src/pages/Animal*.tsx` | Manually verified in browser (register, profile, timeline) | Verified |
| 6. Feed Management | FM-HB-06 | Phase 3 | `app/models/feed.py`, `app/services/feed.py`, `app/api/v1/feed.py`, `ui/.../FeedDialog.tsx` | Manually verified via seed data + forecast API; dialog implemented, not UI-clicked in this pass | Implemented |
| 7. Dairy Management | FM-HB-07 | Phase 3 | `app/models/production.py`, `app/api/v1/dairy.py`, `ui/.../MilkDialog.tsx` | Manually verified end-to-end in browser (recorded a milk session, saw it in timeline) | Verified |
| 8. Poultry Management | FM-HB-08 | Phase 3 | `app/api/v1/poultry.py`, `ui/.../EggDialog.tsx` | Manually verified via seed data + API (egg-decline recommendation); dialog implemented, not UI-clicked | Implemented |
| 9. Veterinary Management | FM-HB-09 | Phase 4 | — | — | Drafted (not implemented) |
| 10. Inventory Management | FM-HB-10 | Phase 5 | Feed-only slice implemented in Ch.6; generalized medicine/product model not yet built | — | Drafted (partially superseded by Ch.6 for feed) |
| 11. Produce Management | FM-HB-11 | Phase 5 | — | — | Drafted (not implemented) |
| 12. Sales and Finance | FM-HB-12 | Phase 5 | — | — | Drafted (not implemented) |
| 13. UI/UX Design System | FM-HB-13 | Phase 1 (foundation), all phases (application) | `ui/src/components/ui/`, `ui/src/components/farmos/`, Tailwind theme in `index.css` | Manually verified in browser incl. RTL/Arabic | Verified |
| 14. Database Architecture | FM-HB-14 | Phase 1 | `backend/app/db/`, `backend/alembic/` | Migration applied, schema inspected | Verified |
| 15. API Architecture | FM-HB-15 | Phase 1 | `backend/app/main.py`, `app/api/idempotent.py` | Manually verified (idempotent writes, error envelope) | Verified |
| 16. Offline Synchronization | FM-HB-16 | Phase 1 | `ui/src/offline/` (Dexie queue, `writeOrQueue`, `flushQueue`) | Implemented; offline/reconnect scenario not yet exercised in this pass | Implemented |
| 17. Security | FM-HB-17 | Phase 1 | `app/core/security.py`, `app/api/deps.py` (JWT + role dependency) | Manually verified (403 for Worker role on decisions) | Verified (RBAC); device/backup hardening still open |
| 18. Testing | FM-HB-18 | Ongoing (all phases) | — | — | Drafted (no automated suite yet) |
| 19. Deployment | FM-HB-19 | Phase 1 (pipeline), Phase 7 (pilot gate) | Local dev run only (no container runtime available this pass, see ADR-009) | — | Drafted (not implemented) |

## Status Legend

- **Drafted** — handbook chapter written and reviewed as architecture (Constitution Principle 19 satisfied for this chapter).
- **In Progress** — implementation underway against this chapter.
- **Implemented** — implementation complete, acceptance criteria not yet fully test-verified.
- **Verified** — acceptance criteria demonstrated via passing tests per [Chapter 18](../handbook/18-Testing/18-Testing.md).

## Maintenance Rule

Update this table whenever a chapter's status changes, and whenever [product/ROADMAP.md](ROADMAP.md) phase checklists are updated. A phase item in the roadmap should not be marked complete unless the corresponding row(s) here reach **Verified**.
