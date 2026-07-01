import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useQuery } from '@tanstack/react-query'
import { recommendationsApi } from '@/api/endpoints'
import { RecommendationCard } from '@/components/farmos/RecommendationCard'
import { useEntityLabels } from '@/hooks/useEntityLabel'
import { useDecideRecommendation } from '@/hooks/useDecideRecommendation'
import { cn } from '@/lib/utils'

// Ch.4.6.4 Decision Intelligence reviews: filtered views over the same
// Recommendation store as the Morning Briefing (RULE-KM-602).
const STATUS_FILTERS = ['open', 'monitoring', 'accepted', 'rejected'] as const

export function RecommendationsPage() {
  const { t } = useTranslation()
  const [status, setStatus] = useState<(typeof STATUS_FILTERS)[number]>('open')
  const { getLabel } = useEntityLabels()
  const decide = useDecideRecommendation()

  const recommendations = useQuery({
    queryKey: ['recommendations', status],
    queryFn: () => recommendationsApi.list({ status_filter: status }),
  })

  return (
    <div className="flex flex-col gap-4">
      <h1 className="text-2xl font-bold">{t('nav.recommendations')}</h1>

      <div className="flex gap-2">
        {STATUS_FILTERS.map((s) => (
          <button
            key={s}
            onClick={() => setStatus(s)}
            className={cn(
              'rounded-full border px-4 py-2 text-sm font-medium capitalize',
              status === s ? 'border-primary bg-primary text-primary-foreground' : 'border-border bg-card',
            )}
          >
            {s}
          </button>
        ))}
      </div>

      {recommendations.isLoading ? (
        <p className="text-muted-foreground">{t('common.loading')}</p>
      ) : recommendations.data && recommendations.data.length > 0 ? (
        <div className="grid gap-3 sm:grid-cols-2">
          {recommendations.data.map((rec) => (
            <RecommendationCard
              key={rec.id}
              recommendation={rec}
              entityLabel={getLabel(rec.entity_type, rec.entity_id)}
              onDecide={(decision, reason) => decide.mutate({ id: rec.id, decision, reason })}
            />
          ))}
        </div>
      ) : (
        <p className="text-sm text-muted-foreground">{t('recommendation.noRecommendations')}</p>
      )}
    </div>
  )
}
