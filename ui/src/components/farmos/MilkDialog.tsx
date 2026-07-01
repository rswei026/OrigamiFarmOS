import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { dairyApi } from '@/api/endpoints'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

// Ch.7 §7.2 Milk Recording Workflow.
export function MilkDialog({ animalId, trigger }: { animalId: string; trigger: React.ReactNode }) {
  const { t } = useTranslation()
  const queryClient = useQueryClient()
  const [open, setOpen] = useState(false)
  const [session, setSession] = useState<'AM' | 'PM'>('AM')
  const [volume, setVolume] = useState('')

  const submit = useMutation({
    mutationFn: () => dairyApi.create({ animal_id: animalId, session, volume_liters: Number(volume) }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['animal-timeline', animalId] })
      queryClient.invalidateQueries({ queryKey: ['recommendations'] })
      queryClient.invalidateQueries({ queryKey: ['briefing'] })
      setOpen(false)
      setVolume('')
    },
  })

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>{trigger}</DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{t('quickActions.milk')}</DialogTitle>
        </DialogHeader>
        <form
          className="flex flex-col gap-4"
          onSubmit={(e) => {
            e.preventDefault()
            submit.mutate()
          }}
        >
          <div className="flex flex-col gap-1.5">
            <Label>Session</Label>
            <select className="h-12 rounded-xl border border-border bg-card px-4" value={session} onChange={(e) => setSession(e.target.value as 'AM' | 'PM')}>
              <option value="AM">AM</option>
              <option value="PM">PM</option>
            </select>
          </div>
          <div className="flex flex-col gap-1.5">
            <Label htmlFor="volume">Volume (L)</Label>
            <Input id="volume" type="number" step="0.1" required value={volume} onChange={(e) => setVolume(e.target.value)} />
          </div>
          <Button type="submit" disabled={submit.isPending}>
            {t('common.save')}
          </Button>
        </form>
      </DialogContent>
    </Dialog>
  )
}
