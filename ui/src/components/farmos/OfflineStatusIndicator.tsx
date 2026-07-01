import { useTranslation } from 'react-i18next'
import { Wifi, WifiOff, RefreshCw } from 'lucide-react'
import { useSyncStatus } from '@/hooks/useSyncStatus'
import { Badge } from '@/components/ui/badge'

// Ch.13 §13.6 RULE-UX-105: connectivity/sync state visible from any
// screen - workers must never wonder whether their entry was saved.
export function OfflineStatusIndicator() {
  const { t } = useTranslation()
  const { online, pendingCount } = useSyncStatus()

  if (online && pendingCount === 0) {
    return (
      <Badge variant="success" className="gap-1">
        <Wifi className="h-3.5 w-3.5" /> {t('offline.online')}
      </Badge>
    )
  }
  if (!online) {
    return (
      <Badge variant="warning" className="gap-1">
        <WifiOff className="h-3.5 w-3.5" /> {t('offline.offline')}
        {pendingCount > 0 && ` · ${t('offline.pending', { count: pendingCount })}`}
      </Badge>
    )
  }
  return (
    <Badge variant="secondary" className="gap-1">
      <RefreshCw className="h-3.5 w-3.5 animate-spin" /> {t('offline.pending', { count: pendingCount })}
    </Badge>
  )
}
