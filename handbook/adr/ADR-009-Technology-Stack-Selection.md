---
title: ADR-009 Technology Stack Selection
adr: 009
status: Accepted
date: 2026-07-01
owner: Product Architecture
tags:
  - architecture
  - technology
  - implementation
---

# ADR-009 — Technology Stack Selection

## Status

Accepted

## Context

[CONCEPT_NOTE.md §14](../../CONCEPT_NOTE.md#14-technical-concept) left the technical direction deliberately flexible ("Flutter or another cross-platform framework... the exact technical stack can be refined"). Phase 1 implementation ([product/ROADMAP.md](../../product/ROADMAP.md)) requires concrete, pinned choices. Two additional constraints now apply: the system must leave a clean integration path for a future on-premises-capable AI backend ([ADR-010](ADR-010-AI-Integration-Architecture.md)), and the UI must reach a modern, polished standard quickly rather than accreting one screen at a time.

## Decision

### Backend

- **Language/framework**: Python 3.11 + FastAPI, per the concept note's own recommendation. FastAPI's native OpenAPI generation satisfies [Chapter 15 §15.2](../15-API-Architecture/15-API-Architecture.md#152-technology) (RULE-API-101) with no extra tooling, and its async support suits both the sync-queue workload (Chapter 16) and any future streaming AI responses (ADR-010).
- **ORM/migrations**: SQLAlchemy 2.0 + Alembic, one migration source of truth applied to both environments, per [Chapter 14 §14.8](../14-Database-Architecture/14-Database-Architecture.md#148-codex-implementation-notes).
- **Database**: PostgreSQL as the central database (concept note §14). For this phase, the "local SQLite" tier described in the concept note is superseded by the frontend decision below — see §"Local/Offline Tier" — rather than a second Python-side SQLite deployment.
- **Auth**: JWT bearer tokens, individually issued per user (never shared device logins, per [Chapter 17 §17.5](../17-Security/17-Security.md#175-authentication) RULE-SEC-103), with a centralized FastAPI dependency enforcing the permission matrix (§17.3) server-side (RULE-SEC-102).

### Frontend — Web PWA, Not Flutter, for This Phase

- **Framework**: React 18 + TypeScript + Vite.
- **UI system**: Tailwind CSS + shadcn/ui (Radix primitives) — chosen specifically to satisfy the "latest UI/UX" requirement with production-quality, accessible components available immediately, rather than custom-building a polished widget set from scratch.
- **State/data**: TanStack Query for server state; component-local/Context state for UI state.
- **Local/Offline Tier**: Dexie.js over IndexedDB as the browser-side "local database," playing the same architectural role the concept note assigns to local SQLite ([Chapter 14 §14.2](../14-Database-Architecture/14-Database-Architecture.md#142-two-tier-database-model)) — a durable local store that every critical workflow writes to first, with a sync queue table (§16.3) reconciling to the FastAPI/PostgreSQL backend when connectivity allows.
- **Installability/offline runtime**: a Workbox-generated service worker makes the app installable and usable with no connectivity, satisfying Constitution Principle 10 at the browser level.
- **i18n**: react-i18next with English and Arabic locales and RTL layout mirroring from the first screen built (Chapter 13 §13.7, RULE-UX-104).

This deliberately departs from the concept note's Flutter-first suggestion for the current phase. The reasoning: Flutter remains the better fit for a deep, native, truly offline-first Android tablet experience, but building a polished custom widget set in Flutter is slower than adopting a mature component library, and the project's own philosophy — prove value at Origami Farms before deeper investment (Constitution Principle 2) — favors reaching a working, demoable, good-looking product quickly. A native Flutter build remains a valid later phase once workflows are validated ([product/ROADMAP.md](../../product/ROADMAP.md)); this ADR does not close that door, and the backend/API layer is UI-framework-agnostic by design (Chapter 15), so a future Flutter client consumes the same API without backend changes.

### Deployment (local/dev, this phase)

Docker is unavailable in this development sandbox; the backend runs directly against a locally installed PostgreSQL 16 instance during this phase. [Chapter 19](../19-Deployment/19-Deployment.md) containerization requirements are unaffected and apply once a container runtime is available — the application is built container-ready (standard `pip`/`npm` dependency management, environment-variable configuration) even though it is not containerized in this pass.

## Consequences

- The "local SQLite" language used throughout Chapters 6, 9, 10, 14, and 16 is implemented as "local IndexedDB via Dexie" for the web client. The architectural pattern (event-sourced, client-generated IDs, sync queue, no silent overwrites) is unchanged; only the storage engine differs from the concept note's literal suggestion.
- A future native mobile client (Flutter or otherwise) integrates against the same FastAPI/PostgreSQL backend and OpenAPI contract with zero backend changes required.
- UI development can draw on shadcn/ui's existing component set (cards, dialogs, badges, forms) as the base for the Chapter 13 shared components (recommendation card, timeline, confidence/withdrawal badges), rather than building each from a blank canvas.

## Alternatives Considered

### Flutter Native, This Phase

Rejected for this phase only (not permanently): would take materially longer to reach a "latest UI/UX" bar and a working demo, and the sandboxed dev environment has no Android/iOS toolchain readily available. Revisit once the web PWA has validated the core workflows (see [product/ROADMAP.md](../../product/ROADMAP.md)).

### Node.js/Express or Django Instead of FastAPI

Rejected: FastAPI's automatic OpenAPI generation directly satisfies RULE-API-101 with no extra tooling, and matches the concept note's own recommendation.

### SQLite (via a Python service) as the Actual Local Tier, with a Thin Web View

Rejected: would require running a second local process/server on the tablet purely to expose SQLite to a browser-based UI, adding operational complexity with no benefit over IndexedDB, which is natively available to any browser-based client.

## Related Documents

- ../14-Database-Architecture/14-Database-Architecture.md
- ../15-API-Architecture/15-API-Architecture.md
- ../16-Offline-Synchronization/16-Offline-Synchronization.md
- ../13-UI-UX-Design-System/13-UI-UX-Design-System.md
- ADR-002-Offline-First-Tablet-First.md
- ADR-010-AI-Integration-Architecture.md
- ../../CONCEPT_NOTE.md
