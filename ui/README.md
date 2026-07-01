# FarmOS UI

React + TypeScript PWA implementing [Chapter 13 - UI/UX Design System](../handbook/13-UI-UX-Design-System/13-UI-UX-Design-System.md) and the offline-first behavior of [Chapter 16](../handbook/16-Offline-Synchronization/16-Offline-Synchronization.md), per [ADR-009](../handbook/adr/ADR-009-Technology-Stack-Selection.md).

## Requirements

- Node.js 20+
- The backend running at `http://localhost:8000` (see [../backend/README.md](../backend/README.md))

## Setup

```bash
npm install
echo "VITE_API_BASE_URL=http://localhost:8000/api/v1" > .env
```

## Run

```bash
npm run dev
```

Open `http://localhost:5173`, log in with a seeded account (see backend README), and the app opens to the Morning Briefing (RULE-UX-101).

## Build

```bash
npm run build   # production build + service worker (installable PWA)
```

## Structure

- `src/components/ui/` - base primitives (Button, Card, Badge, Dialog, Input, Label) in the shadcn/ui style.
- `src/components/farmos/` - FarmOS-specific shared components (Ch.13 §13.4): `RecommendationCard`, `Timeline`, `ConfidenceBadge`, `PriorityBadge`, `OfflineStatusIndicator`, `QuickActionBar`, and the Feed/Milk/Egg/Observation quick-action dialogs.
- `src/offline/` - Dexie (IndexedDB) local store and sync queue (Ch.16), playing the role the handbook assigns to local SQLite (see ADR-009's "Local/Offline Tier").
- `src/api/` - typed API client and endpoint functions (Ch.15).
- `src/i18n/` - English/Arabic locales with RTL layout mirroring (RULE-UX-106).
- `src/pages/` - Login, Morning Briefing, Animals, Flocks, Recommendations.

## What's implemented in this pass

Login, Morning Briefing, Animal/Flock registration and profile with Timeline, Feed/Milk/Egg-collection/Observation quick actions, and the Recommendation review flow (accept/reject-with-reason/monitor). Offline writes for the quick-action workflows queue in IndexedDB and sync automatically on reconnect.

Deferred: Treatment/withdrawal UI, Sales & Finance, Produce, and a dedicated conflict-resolution UI (the sync queue itself handles the common additive-event case per Ch.16 §16.4).
