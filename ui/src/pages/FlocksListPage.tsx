import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { Link } from 'react-router-dom'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Plus, ChevronRight } from 'lucide-react'
import { flocksApi } from '@/api/endpoints'
import type { FlockSpecies } from '@/api/types'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'

const SPECIES_OPTIONS: FlockSpecies[] = ['chicken', 'duck', 'turkey']

export function FlocksListPage() {
  const { t } = useTranslation()
  const queryClient = useQueryClient()
  const [open, setOpen] = useState(false)
  const [name, setName] = useState('')
  const [species, setSpecies] = useState<FlockSpecies>('chicken')
  const [birdCount, setBirdCount] = useState('')

  const flocks = useQuery({ queryKey: ['flocks'], queryFn: () => flocksApi.list() })

  const register = useMutation({
    mutationFn: () => flocksApi.register({ name, species, bird_count: Number(birdCount) || 0, location_id: null }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['flocks'] })
      setOpen(false)
      setName('')
      setBirdCount('')
    },
  })

  return (
    <div className="flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">{t('nav.flocks')}</h1>
        <Dialog open={open} onOpenChange={setOpen}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="h-4 w-4" /> {t('flock.register')}
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>{t('flock.register')}</DialogTitle>
            </DialogHeader>
            <form
              className="flex flex-col gap-4"
              onSubmit={(e) => {
                e.preventDefault()
                register.mutate()
              }}
            >
              <div className="flex flex-col gap-1.5">
                <Label htmlFor="name">{t('flock.name')}</Label>
                <Input id="name" required value={name} onChange={(e) => setName(e.target.value)} />
              </div>
              <div className="flex flex-col gap-1.5">
                <Label htmlFor="species">{t('flock.species')}</Label>
                <select id="species" className="h-12 rounded-xl border border-border bg-card px-4" value={species} onChange={(e) => setSpecies(e.target.value as FlockSpecies)}>
                  {SPECIES_OPTIONS.map((s) => (
                    <option key={s} value={s}>
                      {s}
                    </option>
                  ))}
                </select>
              </div>
              <div className="flex flex-col gap-1.5">
                <Label htmlFor="count">{t('flock.birdCount')}</Label>
                <Input id="count" type="number" value={birdCount} onChange={(e) => setBirdCount(e.target.value)} />
              </div>
              <Button type="submit" disabled={register.isPending}>
                {t('common.save')}
              </Button>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {flocks.data?.map((flock) => (
          <Link key={flock.id} to={`/flocks/${flock.id}`}>
            <Card className="transition hover:border-primary">
              <CardContent className="flex items-center justify-between p-4">
                <div>
                  <div className="font-semibold">{flock.name}</div>
                  <div className="text-sm capitalize text-muted-foreground">
                    {flock.species} · {flock.bird_count} birds
                  </div>
                </div>
                <ChevronRight className="h-4 w-4 text-muted-foreground" />
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  )
}
