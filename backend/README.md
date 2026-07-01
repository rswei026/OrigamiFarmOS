# FarmOS Backend

FastAPI implementation of the handbook's Phase 1-3 slice (see [product/ROADMAP.md](../product/ROADMAP.md)): [Chapter 14 - Database Architecture](../handbook/14-Database-Architecture/14-Database-Architecture.md), [Chapter 15 - API Architecture](../handbook/15-API-Architecture/15-API-Architecture.md), [Chapter 17 - Security](../handbook/17-Security/17-Security.md), and the domain chapters (5-9) it implements. See [ADR-009](../handbook/adr/ADR-009-Technology-Stack-Selection.md) and [ADR-010](../handbook/adr/ADR-010-AI-Integration-Architecture.md) for the technology decisions behind this implementation.

## Requirements

- Python 3.11+
- PostgreSQL 16 (local instance; `DATABASE_URL` is configurable via `FARMOS_DATABASE_URL`)

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Create databases (adjust connection details for your Postgres install)
psql -U postgres -c "CREATE DATABASE farmos;"

# Apply migrations
alembic upgrade head

# Seed realistic mixed-species Origami Farms data (Ch.18 §18.4),
# including one animal engineered to trigger a health-decline recommendation
python -m app.seed
```

## Run

```bash
uvicorn app.main:app --reload --port 8000
```

API docs: `http://localhost:8000/docs` (FastAPI's auto-generated OpenAPI UI - Ch.15 RULE-API-101).

Seeded logins (password `password123`): `owner@origamifarms.io`, `manager@origamifarms.io`, `worker@origamifarms.io`, `vet@origamifarms.io`.

## What's implemented in this pass

- Farm, Location, User/roles, Animal, Flock, Herd (Ch.2, Ch.5, Ch.8)
- Generic Observation model (Ch.4.3)
- Feed Item/Lot/Distribution with derived stock and a simple forecast (Ch.6)
- Milk recording and Egg collection, each also emitting a companion Observation for correlation (Ch.7, Ch.8)
- Knowledge Engine: rule-based Correlation Engine + Recommendation Engine + pluggable `AIProvider` (Ch.4.4-4.5, 4.7, 4.10, ADR-010)
- Decision recording (accept/reject/monitor/delegate/escalate/postpone) (Ch.4.6)
- Morning Briefing aggregation endpoint (Ch.3 §3.4, Ch.4.6.4.1)
- JWT auth + role-based endpoint enforcement (Ch.17)

## Deferred to a later pass

Treatment/Medicine/withdrawal periods (Ch.9), Sales & Finance (Ch.12), Produce (Ch.11), the generalized Inventory model for medicine/product (Ch.10), and offline sync conflict UI (Ch.16) beyond the client-side queue already implemented in `ui/`. See [product/TRACEABILITY.md](../product/TRACEABILITY.md).

## Configuration

All settings are environment variables prefixed `FARMOS_` (see `app/core/config.py`), loadable from a `.env` file. Notably `FARMOS_AI_PROVIDER`, `FARMOS_OPENAI_BASE_URL`, `FARMOS_OPENAI_API_KEY` control the AI explanation provider per [ADR-010](../handbook/adr/ADR-010-AI-Integration-Architecture.md) - point `FARMOS_OPENAI_BASE_URL` at a self-hosted, on-premises OpenAI-compatible endpoint to use it instead of the hosted OpenAI API, with no code changes.
