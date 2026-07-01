---
title: Deployment
chapter: 19
document_id: FM-HB-19
status: Draft
version: 0.1.0
owner: Product Architecture
last_updated: 2026-07-01
depends_on:
  - ../14-Database-Architecture/14-Database-Architecture.md
  - ../18-Testing/18-Testing.md
tags:
  - deployment
  - operations
---

# Chapter 19 — Deployment

## 19.1 Purpose

This chapter defines how FarmOS is built, released, and operated, culminating in the Origami Farms Pilot (Phase 7, [product/ROADMAP.md](../../product/ROADMAP.md)) — the point at which "deployment" stops meaning "runs in a test environment" and starts meaning "runs the real farm."

## 19.2 Environments

| Environment | Purpose |
|---|---|
| Development | Local developer environment, seeded with the mixed-species test dataset (§18.4) |
| Staging | Mirrors production configuration, used to validate a release before it reaches the farm |
| Pilot (Origami Farms) | The real, single-farm production environment (Phase 7) |

### RULE-DEPLOY-101 — Staging Mirrors Pilot Before Any Release

No release SHALL go to the Pilot environment without first passing the full test suite (§18) in Staging, configured identically (same schema version, same rule/pattern configuration versions per §4.10.5).

## 19.3 Backend Deployment

Per concept note §14: FastAPI backend, containerized, backed by PostgreSQL. The backend is deployed independently of mobile releases, versioned via the API contract (§15.2 RULE-API-101), so a mobile app on an older version continues to function against a compatible backend during a rollout window.

## 19.4 Mobile Deployment

Per concept note §14: Flutter (or equivalent cross-platform framework) targeting Android tablets primarily, with desktop/web access as a secondary channel (Windows app, web/PWA, or BlueStacks). During the pilot phase, the Android build is distributed directly (sideloaded APK or private distribution channel) rather than through a public app store, since the audience is exactly one farm.

## 19.5 Release Versioning

Releases are tracked in [product/RELEASES.md](../../product/RELEASES.md), each tied to the roadmap phase it completes (Phase 1-8, concept note §22 / [product/ROADMAP.md](../../product/ROADMAP.md)) and the handbook chapter versions it implements (each chapter's frontmatter `version` field).

## 19.6 Backup and Recovery

### RULE-DEPLOY-102 — Backups Precede Pilot

A tested, scheduled backup of the central PostgreSQL database, with a documented and rehearsed restore procedure, SHALL exist before the Origami Farms Pilot (Phase 7) begins. This is a hard gate, not a nice-to-have, since the pilot is the farm's real operational data from day one (§17.6).

## 19.7 Monitoring During Pilot

During Phase 7, monitoring is deliberately lightweight and farm-relevant rather than enterprise-grade: sync failure rate, API error rate, and — most importantly per the Feedback Loop (§4.9) — recommendation acceptance/rejection rates, since pilot feedback is the primary input to MVP stabilization (Phase 7 outputs: worker feedback, bug fixing, workflow refinement, feature removal where unused).

## 19.8 Functional Requirements

### REQ-DEPLOY-101
The backend shall be deployable as a versioned, containerized service independent of mobile app release cycles.
### REQ-DEPLOY-102
A tested backup/restore procedure shall exist for the central database prior to Phase 7.
### REQ-DEPLOY-103
Every release shall be traceable to the roadmap phase and handbook chapter versions it implements.

## 19.9 Codex Implementation Notes

- Containerize the backend from the first working version, even in development, so environment parity (§19.2 RULE-DEPLOY-101) is real rather than assumed.
- Keep mobile API compatibility versioned explicitly (§15.2) so a pilot farm is never forced into a hard simultaneous upgrade of app and backend.
- Do not defer backup/restore tooling to "later" — implement and test it before Phase 7 begins, per RULE-DEPLOY-102; farm data loss during a real pilot is not recoverable goodwill.

## 19.10 Acceptance Criteria

This chapter is satisfied when:

- A release can be deployed to Staging and validated against the full test suite before reaching Pilot.
- A backup has been taken and successfully restored in a rehearsal before Phase 7 begins.
- Mobile and backend versions can be independently released without breaking compatibility.
