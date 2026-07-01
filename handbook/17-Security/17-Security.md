---
title: Security
chapter: 17
document_id: FM-HB-17
status: Draft
version: 0.1.0
owner: Product Architecture
last_updated: 2026-07-01
depends_on:
  - ../03-Behavioral-Model.md
  - ../15-API-Architecture/15-API-Architecture.md
tags:
  - security
  - roles
  - permissions
---

# Chapter 17 — Security

## 17.1 Purpose

This chapter formalizes the role-based permission model referenced throughout the handbook (concept note §13, [Behavioral Model §3.6](../03-Behavioral-Model.md#36-role-driven-behavior)) and the security requirements around device loss, data protection, and audit.

## 17.2 Roles

| Role | Scope (concept note §13) |
|---|---|
| Farm Owner | Full access: configure farm, review reports, approve recommendations, review financials, manage users, export data |
| Farm Manager | Daily operations: review briefing, assign tasks, validate observations, review alerts, approve actions, monitor performance |
| Worker | Complete assigned work, record observations, cannot diagnose unless separately authorized |
| Veterinarian | Health records: review history, record diagnosis, prescribe treatment, confirm recovery, define withdrawal period |
| Accountant / Finance User | Sales, expenses, customers, suppliers, financial reports |
| Read-Only User | View selected records/reports without editing |

## 17.3 Permission Matrix (Summary)

| Action | Owner | Manager | Worker | Vet | Finance | Read-Only |
|---|---|---|---|---|---|---|
| Record observation | Yes | Yes | Yes | Yes | No | No |
| Enter diagnosis (RULE-VET-102) | No | No* | No | Yes | No | No |
| Accept/reject recommendation | Yes | Yes | No | Yes (health) | No | No |
| Record sale/expense | Yes | Yes | No | No | Yes | No |
| Configure farm/users | Yes | Limited | No | No | No | No |
| View reports | Yes | Yes | Limited | Health only | Financial only | Yes |

\* Unless explicitly authorized per farm configuration (§9.3 RULE-VET-102).

### RULE-SEC-101 — Least Privilege by Default

New roles or permission grants default to the most restrictive applicable set; broader access is an explicit configuration decision by the Farm Owner, not a default.

## 17.4 Enforcement Layers

### RULE-SEC-102 — Defense in Depth

Permissions SHALL be enforced at both the UI layer (hiding unavailable actions, §13) and the API layer (rejecting unauthorized requests, §15.4 RULE-API-102). UI-only enforcement is never sufficient, since the API is reachable independent of the mobile client.

## 17.5 Authentication

FarmOS uses per-user authentication (not shared/generic device logins), so that every event (§3.2) records a real, individually accountable `observer_id`/`recorded_by`/`decided_by` field, satisfying the traceability requirements throughout Chapters 4-12.

### RULE-SEC-103 — No Anonymous or Shared Accounts

Every write action SHALL be attributable to a specific authenticated user. Shared tablet logins that obscure who performed an action are prohibited, since they break observer-reliability learning (§4.9.3) and audit traceability (Constitution Principle 15).

## 17.6 Device and Data Protection

- Tablets are shared, farm-owned devices used by multiple workers across a shift; session handling should support quick user-switching without requiring a full logout/login cycle that discourages proper attribution (§17.5).
- Local SQLite data on a lost/stolen tablet is a real risk given offline-first design; device-level protections (PIN/passcode lock, optionally at-rest encryption) are a Phase 1-2 hardening item, tracked in [product/ROADMAP.md](../../product/ROADMAP.md).
- Central PostgreSQL backups follow standard practice: scheduled backups, tested restore procedure, before any pilot deployment (Phase 7).

## 17.7 Audit Trail

Per Constitution Principle 15 (Traceability), every event, decision, and correction (§3.2 RULE-BM-101) already carries its acting user and timestamp as a structural requirement, not an add-on logging feature. Chapter 17 does not introduce a separate audit-log system — it requires that the event-sourced model itself (Chapter 14) *is* the audit trail.

## 17.8 Functional Requirements

### REQ-SEC-101
FarmOS shall authenticate every user individually, even on a shared tablet.
### REQ-SEC-102
FarmOS shall enforce the permission matrix (§17.3) at the API layer independent of client UI state.
### REQ-SEC-103
FarmOS shall support quick user-switching on a shared tablet without compromising per-action attribution.

## 17.9 Codex Implementation Notes

- Implement authorization as centralized policy checks (e.g., a permissions dependency in FastAPI) referenced by every endpoint, not ad hoc `if role == X` checks scattered per route.
- Design the login/session UX for a shared tablet from the start (fast PIN-based user switching), rather than assuming one user per device as a desktop app would.
- Do not build a separate audit-log table; rely on the event-sourced schema (Chapter 14) as the audit trail, and ensure every event table actually has its `recorded_by`/`observer_id` field populated and non-nullable.

## 17.10 Acceptance Criteria

This chapter is satisfied when:

- Every write in the system carries an individually attributable user, even when multiple users share one tablet in a day.
- A Worker-role API call attempting a Veterinarian-only or Manager-only action is rejected server-side.
- A tested backup/restore procedure exists for the central database before the Origami Farms pilot (Phase 7).
