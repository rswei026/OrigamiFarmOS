import { useEffect, useState } from 'react'
import { useLiveQuery } from 'dexie-react-hooks'
import { db } from '@/offline/db'

// Backs the OfflineStatusIndicator (Ch.13 §13.4, RULE-UX-105): connectivity
// and pending-sync state must be visible from any screen.
export function useSyncStatus() {
  const [online, setOnline] = useState(navigator.onLine)

  useEffect(() => {
    const goOnline = () => setOnline(true)
    const goOffline = () => setOnline(false)
    window.addEventListener('online', goOnline)
    window.addEventListener('offline', goOffline)
    return () => {
      window.removeEventListener('online', goOnline)
      window.removeEventListener('offline', goOffline)
    }
  }, [])

  const pendingCount = useLiveQuery(() => db.syncQueue.where('status').anyOf(['pending', 'syncing']).count(), [], 0)

  return { online, pendingCount: pendingCount ?? 0 }
}
