# File: `handbook/adr/ADR-003-Knowledge-Lifecycle.md`

```markdown
---
title: ADR-003 Knowledge Lifecycle Architecture
adr: 003
status: Accepted
date: 2026-06-30
owner: Product Architecture
tags:
  - knowledge
  - ai
  - decision-intelligence
---

# ADR-003 — Knowledge Lifecycle Architecture

## Status

Accepted

## Context

FarmOS is intended to be more than a record keeping system. It must help Origami Farms convert daily observations into evidence-based decisions and long-term institutional knowledge.

Traditional systems often stop at storing records. This does not satisfy the FarmOS Constitution.

## Decision

FarmOS shall implement a full knowledge lifecycle:

Reality  
→ Observation  
→ Validation  
→ Information  
→ Knowledge  
→ Recommendation  
→ Human Decision  
→ Action  
→ Outcome  
→ Learning

## Consequences

- Recommendations must be first-class entities.
- Outcomes must be captured.
- Learning must be supported.
- AI outputs must be traceable.
- The system must store evidence chains.
- Future modules must comply with this lifecycle.

## Alternatives Considered

### Simple CRUD Records

Rejected because isolated records do not support explainable intelligence.

### Chatbot-First AI

Rejected because FarmOS must build knowledge from structured observations before generating recommendations.

### Dashboard-Only Analytics

Rejected because reporting what happened is insufficient. FarmOS must support decisions.

## Related Documents

- ../04-Knowledge-Model/04.1-Purpose-and-Philosophy.md
- ../04-Knowledge-Model/04.2-Knowledge-Lifecycle.md
```

---