import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { feedApi } from '@/api/endpoints'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

// Ch.6 §6.3 Feeding Workflow: select lot, confirm quantity, save offline.
export function FeedDialog({
  entityType,
  entityId,
  trigger,
}: {
  entityType: 'Animal' | 'Flock'
  entityId: string
  trigger: React.ReactNode
}) {
  const { t } = useTranslation()
  const queryClient = useQueryClient()
  const [open, setOpen] = useState(false)
  const [feedLotId, setFeedLotId] = useState('')
  const [quantity, setQuantity] = useState('')

  const lots = useQuery({ queryKey: ['feed-lots'], queryFn: () => feedApi.lots(), enabled: open })

  const submit = useMutation({
    mutationFn: () => feedApi.distribute({ feed_lot_id: feedLotId, entity_type: entityType, entity_id: entityId, quantity: Number(quantity) }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [entityType === 'Animal' ? 'animal-timeline' : 'flock-timeline', entityId] })
      queryClient.invalidateQueries({ queryKey: ['briefing'] })
      setOpen(false)
      setQuantity('')
    },
  })

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>{trigger}</DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{t('quickActions.feed')}</DialogTitle>
        </DialogHeader>
        <form
          className="flex flex-col gap-4"
          onSubmit={(e) => {
            e.preventDefault()
            submit.mutate()
          }}
        >
          <div className="flex flex-col gap-1.5">
            <Label>Feed Lot</Label>
            <select className="h-12 rounded-xl border border-border bg-card px-4" required value={feedLotId} onChange={(e) => setFeedLotId(e.target.value)}>
              <option value="" disabled>
                Select feed lot
              </option>
              {lots.data?.map((lot) => (
                <option key={lot.id} value={lot.id}>
                  {lot.feed_item_id.slice(0, 8)}... ({lot.remaining?.toFixed(1)} remaining)
                </option>
              ))}
            </select>
          </div>
          <div className="flex flex-col gap-1.5">
            <Label htmlFor="qty">Quantity (kg)</Label>
            <Input id="qty" type="number" step="0.1" required value={quantity} onChange={(e) => setQuantity(e.target.value)} />
          </div>
          <Button type="submit" disabled={submit.isPending}>
            {t('common.save')}
          </Button>
        </form>
      </DialogContent>
    </Dialog>
  )
}
