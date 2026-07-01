import { useTranslation } from 'react-i18next'
import { Badge } from '@/components/ui/badge'
import type { ConfidenceBand } from '@/api/types'

// Ch.13 §13.4 / RULE-UX-102: one confidence-band component, reused
// everywhere a recommendation appears (Ch.4.7 §4.7.7 - consistent color
// coding app-wide).
const VARIANT: Record<ConfidenceBand, 'success' | 'warning' | 'muted'> = {
  high: 'success',
  medium: 'warning',
  low: 'muted',
}

export function ConfidenceBadge({ band }: { band: ConfidenceBand }) {
  const { t } = useTranslation()
  return (
    <Badge variant={VARIANT[band]}>
      {t('recommendation.confidence')}: {band}
    </Badge>
  )
}
