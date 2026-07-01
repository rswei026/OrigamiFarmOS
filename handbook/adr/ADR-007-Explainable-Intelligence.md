---
title: ADR-007 Explainable Intelligence
adr: 007
status: Accepted
date: 2026-07-01
owner: Product Architecture
tags:
  - ai
  - explainability
  - trust
---

# ADR-007 — Explainable Intelligence

## Status

Accepted

## Context

FarmOS's central differentiator is turning observations into recommendations (concept note §7). If those recommendations cannot be explained, farm managers have no basis to trust them (Risk 4, concept note §21), and the system risks behaving as an unaccountable black box — directly contradicting Constitution Principle 8.

## Decision

Every recommendation FarmOS produces must satisfy the six-question explanation contract defined in [4.7 Explainable AI §4.7.2](../04-Knowledge-Model/04.7-Explainable-AI.md#472-the-explanation-contract): what was observed, which trends were detected, what historical context matters, what confidence is assigned and why, what action is suggested, and what information is missing. This applies equally to the MVP's rule-based recommendation engine ([4.5](../04-Knowledge-Model/04.5-Recommendation-Engine.md)) and to any future statistical/ML component, which must satisfy the same contract before it can be promoted to production ([4.10 AI Governance §4.10.3](../04-Knowledge-Model/04.10-AI-Governance.md#4103-governance-requirements-for-any-model-introduced-post-mvp)).

## Consequences

- Recommendation and Knowledge Object schemas structurally include evidence, confidence, and explanation fields — this is not optional metadata (§4.5.3).
- No recommendation may be displayed without its confidence band and supporting evidence (RULE-KM-702).
- A future ML model that cannot produce this explanation structure cannot be used for farm-facing recommendations, regardless of predictive accuracy (RULE-KM-703).
- Confidence is computed from observation quality and signal agreement (§4.4.5, §4.7.3), never a fixed or inflated placeholder.

## Alternatives Considered

### Show Only a Recommendation and a Confidence Percentage

Rejected: a bare percentage without underlying reasoning does not let a manager judge whether to trust it, and fails the six-question contract.

### Defer Explainability Until After a Model Is Built

Rejected: retrofitting explainability onto an opaque model is far harder than requiring it from the start, and risks shipping unexplainable recommendations during the pilot when trust matters most (Phase 7).

## Related Documents

- ../04-Knowledge-Model/04.5-Recommendation-Engine.md
- ../04-Knowledge-Model/04.7-Explainable-AI.md
- ../04-Knowledge-Model/04.10-AI-Governance.md
- ../../CONSTITUTION.md
