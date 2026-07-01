import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { Wheat, Droplets, Eye } from 'lucide-react'
import { animalsApi } from '@/api/endpoints'
import { Timeline } from '@/components/farmos/Timeline'
import { FeedDialog } from '@/components/farmos/FeedDialog'
import { MilkDialog } from '@/components/farmos/MilkDialog'
import { ObservationDialog } from '@/components/farmos/ObservationDialog'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'

// Ch.5 Animal Digital Twin: identity + status + quick actions + timeline,
// satisfying the Five-Minute Test (Ontology §2.6).
export function AnimalProfilePage() {
  const { id } = useParams<{ id: string }>()
  const animal = useQuery({ queryKey: ['animal', id], queryFn: () => animalsApi.get(id!), enabled: !!id })
  const timeline = useQuery({ queryKey: ['animal-timeline', id], queryFn: () => animalsApi.timeline(id!), enabled: !!id })

  if (!animal.data) return <p className="text-muted-foreground">Loading...</p>

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl font-bold">
            {animal.data.tag_number} {animal.data.name && `· ${animal.data.name}`}
          </h1>
          <p className="capitalize text-muted-foreground">
            {animal.data.species} · {animal.data.breed ?? 'unknown breed'} · {animal.data.sex}
          </p>
        </div>
        <Badge variant="outline" className="capitalize">
          {animal.data.status.replace('_', ' ')}
        </Badge>
      </div>

      <div className="flex flex-wrap gap-3">
        <FeedDialog
          entityType="Animal"
          entityId={animal.data.id}
          trigger={
            <Button variant="secondary" size="lg" className="h-auto flex-col gap-1.5 px-6 py-4">
              <Wheat className="h-6 w-6" /> Feed
            </Button>
          }
        />
        <MilkDialog
          animalId={animal.data.id}
          trigger={
            <Button variant="secondary" size="lg" className="h-auto flex-col gap-1.5 px-6 py-4">
              <Droplets className="h-6 w-6" /> Milk
            </Button>
          }
        />
        <ObservationDialog
          entityType="Animal"
          entityId={animal.data.id}
          trigger={
            <Button variant="secondary" size="lg" className="h-auto flex-col gap-1.5 px-6 py-4">
              <Eye className="h-6 w-6" /> Observe
            </Button>
          }
        />
      </div>

      <section>
        <h2 className="mb-3 text-lg font-semibold">Timeline</h2>
        {timeline.isLoading ? <p className="text-muted-foreground">Loading...</p> : <Timeline entries={timeline.data ?? []} />}
      </section>
    </div>
  )
}
