import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { Check, X, Eye, ChevronDown, ChevronUp } from 'lucide-react'
import { Card, CardContent, CardHeader } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Label } from '@/components/ui/label'
import { ConfidenceBadge } from './ConfidenceBadge'
import { PriorityBadge } from './PriorityBadge'
import type { Recommendation, DecisionOption } from '@/api/types'

// Ch.4.5.9 / Ch.4.7.4: every recommendation card must show entity,
// priority + confidence, one-line explanation, accept/reject/monitor
// without scrolling, and a link to the full evidence chain. Built once,
// reused across the Morning Briefing and Recommendations Review pages
// (RULE-UX-102).
export function RecommendationCard({
  recommendation,
  entityLabel,
  onDecide,
}: {
  recommendation: Recommendation
  entityLabel: string
  onDecide: (decision: DecisionOption, reason?: string) => void
}) {
  const { t } = useTranslation()
  const [showEvidence, setShowEvidence] = useState(false)
  const [rejectOpen, setRejectOpen] = useState(false)
  const [reason, setReason] = useState('')

  const isDecided = recommendation.status !== 'open'

  return (
    <Card folded>
      <CardHeader className="flex-row items-start justify-between gap-3">
        <div>
          <div className="text-base font-semibold">{entityLabel}</div>
          <div className="mt-1 flex flex-wrap gap-2">
            <PriorityBadge priority={recommendation.priority} />
            <ConfidenceBadge band={recommendation.confidence_band} />
            {isDecided && <span className="text-xs text-muted-foreground capitalize">{t('recommendation.status')}: {recommendation.status}</span>}
          </div>
        </div>
      </CardHeader>
      <CardContent className="flex flex-col gap-3">
        <p className="text-sm text-foreground">{recommendation.explanation}</p>

        {recommendation.missing_information && (
          <p className="text-xs text-muted-foreground">
            {t('recommendation.missingInfo')}: {recommendation.missing_information}
          </p>
        )}

        <button
          type="button"
          onClick={() => setShowEvidence((v) => !v)}
          className="flex items-center gap-1 self-start text-xs font-medium text-primary"
        >
          {showEvidence ? <ChevronUp className="h-3.5 w-3.5" /> : <ChevronDown className="h-3.5 w-3.5" />}
          Evidence ({recommendation.evidence.observations?.length ?? 0})
        </button>
        {showEvidence && (
          <ul className="rounded-lg bg-muted p-3 text-xs text-muted-foreground">
            {recommendation.evidence.observations?.map((o) => (
              <li key={o.id}>
                {o.type}: {String(o.value)}
                {o.unit ?? ''} ({new Date(o.observed_at).toLocaleDateString()}, quality {o.quality})
              </li>
            ))}
          </ul>
        )}

        {!isDecided && (
          <div className="flex flex-wrap gap-2 pt-1">
            <Button size="sm" onClick={() => onDecide('accept')}>
              <Check className="h-4 w-4" /> {t('recommendation.accept')}
            </Button>
            <Button size="sm" variant="outline" onClick={() => onDecide('monitor')}>
              <Eye className="h-4 w-4" /> {t('recommendation.monitor')}
            </Button>
            <Button size="sm" variant="destructive" onClick={() => setRejectOpen(true)}>
              <X className="h-4 w-4" /> {t('recommendation.reject')}
            </Button>
          </div>
        )}
      </CardContent>

      <Dialog open={rejectOpen} onOpenChange={setRejectOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{t('recommendation.reject')}</DialogTitle>
          </DialogHeader>
          <Label htmlFor="reject-reason">{t('recommendation.reason')}</Label>
          <textarea
            id="reject-reason"
            className="mt-2 w-full rounded-xl border border-border p-3 text-sm"
            rows={3}
            value={reason}
            onChange={(e) => setReason(e.target.value)}
            placeholder={t('recommendation.reasonRequired')}
          />
          <div className="mt-4 flex justify-end gap-2">
            <Button variant="outline" onClick={() => setRejectOpen(false)}>
              {t('recommendation.cancel')}
            </Button>
            <Button
              variant="destructive"
              disabled={!reason.trim()}
              onClick={() => {
                onDecide('reject', reason)
                setRejectOpen(false)
                setReason('')
              }}
            >
              {t('recommendation.submit')}
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </Card>
  )
}
