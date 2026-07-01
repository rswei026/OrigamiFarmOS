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

No implementation exists yet (Phase 0 — see [product/ROADMAP.md](ROADMAP.md)), so the Implementation and Test columns are empty by design. This table should be updated as each phase delivers code, not filled in speculatively.

| Chapter | Document ID | Roadmap phase | Implementation | Test evidence | Status |
|---|---|---|---|---|---|
| 1. Vision | FM-HB-01 | Phase 0 | N/A (foundational) | N/A | Drafted |
| 2. Ontology | FM-HB-02 | Phase 1-2 | — | — | Drafted |
| 3. Behavioral Model | FM-HB-03 | Phase 1-3 | — | — | Drafted |
| 4.1 Purpose and Philosophy | FM-HB-04.1 | Phase 6 | — | — | Drafted |
| 4.2 Knowledge Lifecycle | FM-HB-04.2 | Phase 6 | — | — | Drafted |
| 4.3 Observation Model | FM-HB-04.3 | Phase 3 | — | — | Drafted |
| 4.4 Correlation Engine | FM-HB-04.4 | Phase 6 | — | — | Drafted |
| 4.5 Recommendation Engine | FM-HB-04.5 | Phase 6 | — | — | Drafted |
| 4.6 Decision Intelligence | FM-HB-04.6 | Phase 6 | — | — | Drafted |
| 4.7 Explainable AI | FM-HB-04.7 | Phase 6 | — | — | Drafted |
| 4.8 Knowledge Timeline | FM-HB-04.8 | Phase 2 | — | — | Drafted |
| 4.9 Knowledge Feedback Loop | FM-HB-04.9 | Phase 6 | — | — | Drafted |
| 4.10 AI Governance | FM-HB-04.10 | Ongoing (governance) | — | — | Drafted |
| 5. Animal Digital Twin | FM-HB-05 | Phase 2 | — | — | Drafted |
| 6. Feed Management | FM-HB-06 | Phase 3 | — | — | Drafted |
| 7. Dairy Management | FM-HB-07 | Phase 3 | — | — | Drafted |
| 8. Poultry Management | FM-HB-08 | Phase 3 | — | — | Drafted |
| 9. Veterinary Management | FM-HB-09 | Phase 4 | — | — | Drafted |
| 10. Inventory Management | FM-HB-10 | Phase 5 | — | — | Drafted |
| 11. Produce Management | FM-HB-11 | Phase 5 | — | — | Drafted |
| 12. Sales and Finance | FM-HB-12 | Phase 5 | — | — | Drafted |
| 13. UI/UX Design System | FM-HB-13 | Phase 1 (foundation), all phases (application) | — | — | Drafted |
| 14. Database Architecture | FM-HB-14 | Phase 1 | — | — | Drafted |
| 15. API Architecture | FM-HB-15 | Phase 1 | — | — | Drafted |
| 16. Offline Synchronization | FM-HB-16 | Phase 1 | — | — | Drafted |
| 17. Security | FM-HB-17 | Phase 1 | — | — | Drafted |
| 18. Testing | FM-HB-18 | Ongoing (all phases) | — | — | Drafted |
| 19. Deployment | FM-HB-19 | Phase 1 (pipeline), Phase 7 (pilot gate) | — | — | Drafted |

## Status Legend

- **Drafted** — handbook chapter written and reviewed as architecture (Constitution Principle 19 satisfied for this chapter).
- **In Progress** — implementation underway against this chapter.
- **Implemented** — implementation complete, acceptance criteria not yet fully test-verified.
- **Verified** — acceptance criteria demonstrated via passing tests per [Chapter 18](../handbook/18-Testing/18-Testing.md).

## Maintenance Rule

Update this table whenever a chapter's status changes, and whenever [product/ROADMAP.md](ROADMAP.md) phase checklists are updated. A phase item in the roadmap should not be marked complete unless the corresponding row(s) here reach **Verified**.
