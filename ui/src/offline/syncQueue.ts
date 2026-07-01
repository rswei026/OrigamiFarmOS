import { apiClient } from '@/api/client'
import { db, type QueuedWrite } from './db'

// RULE-SYNC-101 (Ch.16 §16.2): local save is never blocked by network.
// Every quick-action workflow calls `writeOrQueue` instead of the API
// client directly. It tries an immediate send; on any failure (offline,
// timeout, 5xx) it falls back to the durable local queue and returns
// success to the caller immediately - the worker never waits on a
// network round-trip to see their entry "saved".
export async function writeOrQueue(url: string, body: Record<string, unknown>, label: string): Promise<{ queued: boolean }> {
  const id = (body.id as string) || crypto.randomUUID()
  const payload = { ...body, id }

  if (navigator.onLine) {
    try {
      await apiClient.post(url, payload)
      return { queued: false }
    } catch {
      // fall through to queueing - could be a transient network failure
    }
  }

  const entry: QueuedWrite = {
    id,
    method: 'POST',
    url,
    body: payload,
    createdAt: new Date().toISOString(),
    status: 'pending',
    label,
  }
  await db.syncQueue.put(entry)
  return { queued: true }
}

let flushing = false

// RULE-SYNC-103: opportunistic, backoff-friendly flush - triggered on
// reconnect and on an interval, never a tight polling loop.
export async function flushQueue(): Promise<void> {
  if (flushing || !navigator.onLine) return
  flushing = true
  try {
    const pending = await db.syncQueue.where('status').equals('pending').sortBy('createdAt')
    for (const item of pending) {
      await db.syncQueue.update(item.id, { status: 'syncing' })
      try {
        // Idempotent replay (RULE-API-103): the same client-generated id
        // is safe to resend if a previous attempt partially succeeded.
        await apiClient.post(item.url, item.body)
        await db.syncQueue.update(item.id, { status: 'synced' })
      } catch (err) {
        await db.syncQueue.update(item.id, {
          status: 'pending',
          errorMessage: err instanceof Error ? err.message : 'Sync failed',
        })
        // Stop on first failure to preserve ordering and avoid hammering
        // an unreachable backend (RULE-SYNC-103).
        break
      }
    }
    // Housekeeping: drop synced entries older than a day to keep the
    // local queue table small.
    const cutoff = new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString()
    const stale = await db.syncQueue.where('status').equals('synced').toArray()
    await db.syncQueue.bulkDelete(stale.filter((s) => s.createdAt < cutoff).map((s) => s.id))
  } finally {
    flushing = false
  }
}

export function initSyncQueue() {
  window.addEventListener('online', () => void flushQueue())
  void flushQueue()
  // Fallback heartbeat in case the 'online' event is missed (RULE-SYNC-103).
  setInterval(() => void flushQueue(), 30_000)
}
