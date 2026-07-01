---
title: ADR-008 Repository as Single Source of Truth
adr: 008
status: Accepted
date: 2026-07-01
owner: Product Architecture
tags:
  - governance
  - process
---

# ADR-008 — Repository as Single Source of Truth

## Status

Accepted

## Context

FarmOS's product definition, architecture, and implementation are being developed with AI-assisted tooling (concept note §14-15) across multiple contributors and sessions. Without a single authoritative source, product intent, architecture decisions, and implementation could drift apart — decisions made in a chat, a meeting, or a comment could silently override or contradict the handbook.

## Decision

The GitHub repository (`origami-farmos`) is the single source of truth for product, architecture, documentation, and code, per Constitution Principle 18 and concept note §15. The Engineering Handbook is the authoritative specification; any implementation must trace back to a handbook chapter, and any architecture change requires a handbook update (and, for significant decisions, an ADR) before implementation — Constitution Principle 19 (Architecture Before Implementation).

## Consequences

- No feature is implemented without a corresponding handbook chapter/section describing it (see [product/TRACEABILITY.md](../../product/TRACEABILITY.md)).
- Significant architecture decisions are captured as ADRs in this folder, not left as implicit tribal knowledge or buried in pull request discussions.
- Documentation, implementation, and testing are expected to remain synchronized; a chapter's "Acceptance Criteria" section is not satisfied until implementation and tests both exist ([Chapter 18 — Testing](../18-Testing/18-Testing.md)).
- Product scope changes go through [product/MVP_SCOPE.md](../../product/MVP_SCOPE.md), not ad hoc feature requests.

## Alternatives Considered

### Keep Architecture Knowledge Primarily in Chat/Meeting Notes

Rejected: does not survive contributor turnover or AI-session boundaries, directly undermining Constitution Principle 9 (Institutional Memory) — the same principle FarmOS applies to the farm's own operational knowledge.

### Separate Wiki or External Documentation Tool

Rejected: separating documentation from the code it governs increases the risk of drift and removes the ability to review architecture and implementation changes together in one pull request.

## Related Documents

- ../../CONSTITUTION.md
- ../README.md
- ../../product/TRACEABILITY.md
- ../../product/MVP_SCOPE.md
