import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { poultryApi } from '@/api/endpoints'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

// Ch.8 §8.2 Egg Collection Workflow.
export function EggDialog({ flockId, trigger }: { flockId: string; trigger: React.ReactNode }) {
  const { t } = useTranslation()
  const queryClient = useQueryClient()
  const [open, setOpen] = useState(false)
  const [total, setTotal] = useState('')
  const [broken, setBroken] = useState('0')

  const submit = useMutation({
    mutationFn: () => poultryApi.create({ flock_id: flockId, total_eggs: Number(total), broken_eggs: Number(broken) }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['flock-timeline', flockId] })
      queryClient.invalidateQueries({ queryKey: ['recommendations'] })
      queryClient.invalidateQueries({ queryKey: ['briefing'] })
      setOpen(false)
      setTotal('')
      setBroken('0')
    },
  })

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>{trigger}</DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{t('quickActions.eggs')}</DialogTitle>
        </DialogHeader>
        <form
          className="flex flex-col gap-4"
          onSubmit={(e) => {
            e.preventDefault()
            submit.mutate()
          }}
        >
          <div className="flex flex-col gap-1.5">
            <Label htmlFor="total">Total eggs</Label>
            <Input id="total" type="number" required value={total} onChange={(e) => setTotal(e.target.value)} />
          </div>
          <div className="flex flex-col gap-1.5">
            <Label htmlFor="broken">Broken eggs</Label>
            <Input id="broken" type="number" value={broken} onChange={(e) => setBroken(e.target.value)} />
          </div>
          <Button type="submit" disabled={submit.isPending}>
            {t('common.save')}
          </Button>
        </form>
      </DialogContent>
    </Dialog>
  )
}
