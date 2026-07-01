import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { observationsApi } from '@/api/endpoints'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import type { ObservationQuality } from '@/api/types'

// Ch.9 §9.2 Health Observation Workflow: structured, objective fields
// only - RULE-VET-101, no diagnosis field is presented here by design.
const OBSERVATION_TYPES = [
  { value: 'temperature', label: 'Temperature (°C)', numeric: true, quality: 'A' as ObservationQuality },
  { value: 'weight', label: 'Weight (kg)', numeric: true, quality: 'B' as ObservationQuality },
  { value: 'appetite', label: 'Appetite (reduced / normal / refused)', numeric: false, quality: 'C' as ObservationQuality },
  { value: 'limping', label: 'Limping (yes / no)', numeric: false, quality: 'C' as ObservationQuality },
  { value: 'general_note', label: 'General note', numeric: false, quality: 'D' as ObservationQuality },
]

export function ObservationDialog({
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
  const [type, setType] = useState(OBSERVATION_TYPES[0])
  const [value, setValue] = useState('')
  const [notes, setNotes] = useState('')

  const submit = useMutation({
    mutationFn: () =>
      observationsApi.create({
        entity_type: entityType,
        entity_id: entityId,
        observation_type: type.value,
        ...(type.numeric ? { value_numeric: Number(value) } : { value_text: value }),
        quality: type.quality,
        notes: notes || undefined,
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [entityType === 'Animal' ? 'animal-timeline' : 'flock-timeline', entityId] })
      queryClient.invalidateQueries({ queryKey: ['recommendations'] })
      queryClient.invalidateQueries({ queryKey: ['briefing'] })
      setOpen(false)
      setValue('')
      setNotes('')
    },
  })

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>{trigger}</DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{t('animal.recordObservation')}</DialogTitle>
        </DialogHeader>
        <form
          className="flex flex-col gap-4"
          onSubmit={(e) => {
            e.preventDefault()
            submit.mutate()
          }}
        >
          <div className="flex flex-col gap-1.5">
            <Label>Observation type</Label>
            <select
              className="h-12 rounded-xl border border-border bg-card px-4"
              value={type.value}
              onChange={(e) => setType(OBSERVATION_TYPES.find((o) => o.value === e.target.value)!)}
            >
              {OBSERVATION_TYPES.map((o) => (
                <option key={o.value} value={o.value}>
                  {o.label}
                </option>
              ))}
            </select>
          </div>
          <div className="flex flex-col gap-1.5">
            <Label htmlFor="value">Value</Label>
            <Input id="value" type={type.numeric ? 'number' : 'text'} step="0.1" required value={value} onChange={(e) => setValue(e.target.value)} />
          </div>
          <div className="flex flex-col gap-1.5">
            <Label htmlFor="notes">Notes</Label>
            <Input id="notes" value={notes} onChange={(e) => setNotes(e.target.value)} />
          </div>
          <Button type="submit" disabled={submit.isPending}>
            {t('common.save')}
          </Button>
        </form>
      </DialogContent>
    </Dialog>
  )
}
