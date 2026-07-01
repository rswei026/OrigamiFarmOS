import { Badge } from '@/components/ui/badge'
import type { RecommendationPriority } from '@/api/types'

const VARIANT: Record<RecommendationPriority, 'destructive' | 'warning' | 'secondary' | 'muted'> = {
  urgent: 'destructive',
  high: 'warning',
  medium: 'secondary',
  low: 'muted',
}

export function PriorityBadge({ priority }: { priority: RecommendationPriority }) {
  return <Badge variant={VARIANT[priority]}>{priority}</Badge>
}
