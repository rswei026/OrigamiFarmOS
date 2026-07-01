import Dexie, { type Table } from 'dexie'

// Local-first storage - ADR-009 "Local/Offline Tier": Dexie/IndexedDB plays
// the same architectural role the handbook assigns to local SQLite
// (Ch.14 §14.2). Every critical workflow writes here first (Ch.16 §16.2);
// the sync queue reconciles to the backend when connectivity allows.
export interface QueuedWrite {
  id: string // client-generated UUID (Ch.14 RULE-DB-103) - also used as idempotency key
  method: 'POST'
  url: string
  body: unknown
  createdAt: string
  status: 'pending' | 'syncing' | 'synced' | 'error'
  errorMessage?: string
  label: string // human-readable summary for the offline status UI
}

class FarmOsDb extends Dexie {
  syncQueue!: Table<QueuedWrite, string>

  constructor() {
    super('farmos')
    this.version(1).stores({
      // Indexed by status so the flush loop can efficiently find pending items.
      syncQueue: 'id, status, createdAt',
    })
  }
}

export const db = new FarmOsDb()
