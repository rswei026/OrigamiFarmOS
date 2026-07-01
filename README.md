# OrigamiFarmOS

Origami FarmOS is an offline-first, tablet-first digital operating system for managing the daily operations, production, health, inventory, finance, and decision-making needs of Origami Farms. It is being built first, and specifically, for Origami Farms, and will only be considered for commercialization to other farms after it proves its value in real daily use.

FarmOS helps farmers make better decisions with less effort by turning worker observations into evidence-based, explainable recommendations — never silent diagnoses or unaccountable AI.

## Start Here

- [CONCEPT_NOTE.md](CONCEPT_NOTE.md) — the product concept and rationale
- [CONSTITUTION.md](CONSTITUTION.md) — the non-negotiable engineering and product principles
- [handbook/SUMMARY.md](handbook/SUMMARY.md) — the full Engineering Handbook (architecture and specification)
- [product/MVP_SCOPE.md](product/MVP_SCOPE.md) — what is, and is not, in the first release
- [product/ROADMAP.md](product/ROADMAP.md) — the phased delivery plan
- [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md) — current status by area

## Running It

- [backend/README.md](backend/README.md) — FastAPI + PostgreSQL API (setup, migrations, seed data)
- [ui/README.md](ui/README.md) — React + TypeScript PWA (offline-first, bilingual English/Arabic)

## Current Status

Phase 0 (Engineering Repository Setup) is complete: the Constitution, Concept Note, and full Engineering Handbook are drafted, per Constitution Principle 19 (architecture before implementation).

A first vertical slice of Phases 1-3 is implemented: farm/user/role foundation, the Animal and Flock digital twins, Feed/Milk/Egg-collection/Observation workflows, a rule-based Knowledge Engine producing explainable, evidence-based recommendations, Decision recording, and the Morning Briefing — backed by a FastAPI/PostgreSQL backend and a React PWA frontend. See [backend/README.md](backend/README.md) and [ui/README.md](ui/README.md) for what's implemented versus deferred, and [product/TRACEABILITY.md](product/TRACEABILITY.md) / [product/ROADMAP.md](product/ROADMAP.md) for what's next.
