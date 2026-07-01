import { useTranslation } from 'react-i18next'
import { useQuery } from '@tanstack/react-query'
import { AlertTriangle, PackageX } from 'lucide-react'
import { briefingApi, recommendationsApi } from '@/api/endpoints'
import { RecommendationCard } from '@/components/farmos/RecommendationCard'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { useAuth } from '@/context/AuthContext'
import { useEntityLabels } from '@/hooks/useEntityLabel'
import { useDecideRecommendation } from '@/hooks/useDecideRecommendation'

// Ch.3 §3.4 / Ch.4.6.4.1: FarmOS opens with a Morning Briefing, not a
// static dashboard - the Daily Review answering "what needs attention
// today?".
export function BriefingPage() {
  const { t } = useTranslation()
  const { user } = useAuth()
  const { getLabel } = useEntityLabels()
  const decide = useDecideRecommendation()

  const briefing = useQuery({ queryKey: ['briefing'], queryFn: briefingApi.morning })
  const urgentFull = useQuery({
    queryKey: ['recommendations', 'open'],
    queryFn: () => recommendationsApi.list({ status_filter: 'open' }),
  })

  if (briefing.isLoading) return <p className="text-muted-foreground">{t('common.loading')}</p>

  const urgentIds = new Set((briefing.data?.urgent_recommendations ?? []).map((r) => r.id))
  const urgentRecommendations = (urgentFull.data ?? []).filter((r) => urgentIds.has(r.id))

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-bold">{t('briefing.title', { name: user?.full_name })}</h1>
        <p className="text-muted-foreground">{t('briefing.subtitle')}</p>
      </div>

      <section className="flex flex-col gap-3">
        <h2 className="flex items-center gap-2 text-lg font-semibold">
          <AlertTriangle className="h-5 w-5 text-priority-urgent" /> {t('briefing.urgent')}
        </h2>
        {urgentRecommendations.length === 0 ? (
          <p className="text-sm text-muted-foreground">{t('briefing.noUrgent')}</p>
        ) : (
          <div className="grid gap-3 sm:grid-cols-2">
            {urgentRecommendations.map((rec) => (
              <RecommendationCard
                key={rec.id}
                recommendation={rec}
                entityLabel={getLabel(rec.entity_type, rec.entity_id)}
                onDecide={(decision, reason) => decide.mutate({ id: rec.id, decision, reason })}
              />
            ))}
          </div>
        )}
      </section>

      {briefing.data && briefing.data.feed_stock_warnings.length > 0 && (
        <section className="flex flex-col gap-3">
          <h2 className="flex items-center gap-2 text-lg font-semibold">
            <PackageX className="h-5 w-5 text-warning" /> {t('briefing.feedWarnings')}
          </h2>
          <div className="grid gap-3 sm:grid-cols-2">
            {briefing.data.feed_stock_warnings.map((w) => (
              <Card key={w.feed_item_id}>
                <CardContent className="flex items-center justify-between p-4">
                  <span className="font-medium">{w.feed_item_name}</span>
                  <Badge variant="warning">{t('briefing.daysRemaining', { days: w.days_remaining })}</Badge>
                </CardContent>
              </Card>
            ))}
          </div>
        </section>
      )}

      <section>
        <Card>
          <CardHeader>
            <CardTitle className="text-base">{t('briefing.todaysActivity')}</CardTitle>
          </CardHeader>
          <CardContent className="flex flex-wrap gap-4 text-sm">
            <span>
              {t('briefing.milkRecorded')}:{' '}
              <Badge variant={briefing.data?.todays_activity.milk_recorded ? 'success' : 'muted'}>
                {briefing.data?.todays_activity.milk_recorded ? t('briefing.done') : t('briefing.notYet')}
              </Badge>
            </span>
            <span>
              {t('briefing.eggsRecorded')}:{' '}
              <Badge variant={briefing.data?.todays_activity.eggs_recorded ? 'success' : 'muted'}>
                {briefing.data?.todays_activity.eggs_recorded ? t('briefing.done') : t('briefing.notYet')}
              </Badge>
            </span>
            <span>
              {t('briefing.observationsRecorded', { count: briefing.data?.todays_activity.observations_recorded_today ?? 0 })}
            </span>
          </CardContent>
        </Card>
      </section>
    </div>
  )
}
