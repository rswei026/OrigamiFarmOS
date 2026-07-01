import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { Link } from 'react-router-dom'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Plus, ChevronRight } from 'lucide-react'
import { animalsApi } from '@/api/endpoints'
import type { AnimalSpecies } from '@/api/types'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Badge } from '@/components/ui/badge'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'

const SPECIES_OPTIONS: AnimalSpecies[] = ['cow', 'sheep', 'goat', 'horse']

export function AnimalsListPage() {
  const { t } = useTranslation()
  const queryClient = useQueryClient()
  const [open, setOpen] = useState(false)
  const [tagNumber, setTagNumber] = useState('')
  const [name, setName] = useState('')
  const [species, setSpecies] = useState<AnimalSpecies>('cow')
  const [sex, setSex] = useState('female')

  const animals = useQuery({ queryKey: ['animals'], queryFn: () => animalsApi.list() })

  const register = useMutation({
    mutationFn: () => animalsApi.register({ tag_number: tagNumber, name: name || null, species, breed: null, sex, birth_date: null, current_location_id: null }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['animals'] })
      setOpen(false)
      setTagNumber('')
      setName('')
    },
  })

  return (
    <div className="flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">{t('nav.animals')}</h1>
        <Dialog open={open} onOpenChange={setOpen}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="h-4 w-4" /> {t('animal.register')}
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>{t('animal.register')}</DialogTitle>
            </DialogHeader>
            <form
              className="flex flex-col gap-4"
              onSubmit={(e) => {
                e.preventDefault()
                register.mutate()
              }}
            >
              <div className="flex flex-col gap-1.5">
                <Label htmlFor="tag">{t('animal.tagNumber')}</Label>
                <Input id="tag" required value={tagNumber} onChange={(e) => setTagNumber(e.target.value)} />
              </div>
              <div className="flex flex-col gap-1.5">
                <Label htmlFor="name">{t('animal.name')}</Label>
                <Input id="name" value={name} onChange={(e) => setName(e.target.value)} />
              </div>
              <div className="flex flex-col gap-1.5">
                <Label htmlFor="species">{t('animal.species')}</Label>
                <select
                  id="species"
                  className="h-12 rounded-xl border border-border bg-card px-4"
                  value={species}
                  onChange={(e) => setSpecies(e.target.value as AnimalSpecies)}
                >
                  {SPECIES_OPTIONS.map((s) => (
                    <option key={s} value={s}>
                      {s}
                    </option>
                  ))}
                </select>
              </div>
              <div className="flex flex-col gap-1.5">
                <Label htmlFor="sex">{t('animal.sex')}</Label>
                <select
                  id="sex"
                  className="h-12 rounded-xl border border-border bg-card px-4"
                  value={sex}
                  onChange={(e) => setSex(e.target.value)}
                >
                  <option value="female">{t('animal.female')}</option>
                  <option value="male">{t('animal.male')}</option>
                </select>
              </div>
              <Button type="submit" disabled={register.isPending}>
                {t('common.save')}
              </Button>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {animals.data?.map((animal) => (
          <Link key={animal.id} to={`/animals/${animal.id}`}>
            <Card className="transition hover:border-primary">
              <CardContent className="flex items-center justify-between p-4">
                <div>
                  <div className="font-semibold">
                    {animal.tag_number} {animal.name && `· ${animal.name}`}
                  </div>
                  <div className="text-sm capitalize text-muted-foreground">
                    {animal.species} · {animal.sex}
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Badge variant="outline" className="capitalize">
                    {animal.status.replace('_', ' ')}
                  </Badge>
                  <ChevronRight className="h-4 w-4 text-muted-foreground" />
                </div>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  )
}
