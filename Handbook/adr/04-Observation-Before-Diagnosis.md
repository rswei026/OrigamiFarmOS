# File: `handbook/adr/ADR-004-Observation-Before-Diagnosis.md`

```markdown
---
title: ADR-004 Observation Before Diagnosis
adr: 004
status: Accepted
date: 2026-06-30
owner: Product Architecture
tags:
  - observations
  - veterinary
  - ai-governance
---

# ADR-004 — Observation Before Diagnosis

## Status

Accepted

## Context

Farm workers may observe signs of illness, production changes, or abnormal behavior, but diagnosis should remain the responsibility of veterinarians or qualified professionals.

FarmOS must avoid encouraging subjective or incorrect diagnosis by workers.

## Decision

FarmOS shall require workers to record objective observations rather than diagnoses.

Workers record:

- milk dropped
- animal refused feed
- temperature elevated
- swelling observed
- limping observed

Workers do not record:

- mastitis
- ketosis
- infection
- pneumonia

FarmOS may generate an evidence-based recommendation suggesting veterinary review, but it must not present itself as a diagnostic authority.

## Consequences

- Observation templates must focus on signs and facts.
- Diagnosis fields are restricted to veterinarian or manager-approved workflows.
- AI recommendations must be framed as decision support.
- Every health recommendation must include evidence and confidence.
- User interface must avoid disease labels in worker input screens unless part of a confirmed diagnosis workflow.

## Alternatives Considered

### Allow Workers to Select Disease

Rejected because it increases subjectivity and risk.

### Allow AI to Diagnose Automatically

Rejected because FarmOS is a decision-support platform, not a replacement for veterinary judgement.

## Related Documents

- ../04-Knowledge-Model/04.3-Observation-Model.md
- ../../CONSTITUTION.md
```

---