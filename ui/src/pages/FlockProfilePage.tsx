import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { Wheat, Egg, Eye } from 'lucide-react'
import { flocksApi } from '@/api/endpoints'
import { Timeline } from '@/components/farmos/Timeline'
import { FeedDialog } from '@/components/farmos/FeedDialog'
import { EggDialog } from '@/components/farmos/EggDialog'
import { ObservationDialog } from '@/components/farmos/ObservationDialog'
import { Button } from '@/components/ui/button'

// Ch.8 Poultry Management: Flock is the digital twin (RULE-ONT-104),
// same profile pattern as Animal (Ch.5) for UI consistency.
export function FlockProfilePage() {
  const { id } = useParams<{ id: string }>()
  const flock = useQuery({ queryKey: ['flock', id], queryFn: () => flocksApi.get(id!), enabled: !!id })
  const timeline = useQuery({ queryKey: ['flock-timeline', id], queryFn: () => flocksApi.timeline(id!), enabled: !!id })

  if (!flock.data) return <p className="text-muted-foreground">Loading...</p>

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-bold">{flock.data.name}</h1>
        <p className="capitalize text-muted-foreground">
          {flock.data.species} · {flock.data.bird_count} birds
        </p>
      </div>

      <div className="flex flex-wrap gap-3">
        <FeedDialog
          entityType="Flock"
          entityId={flock.data.id}
          trigger={
            <Button variant="secondary" size="lg" className="h-auto flex-col gap-1.5 px-6 py-4">
              <Wheat className="h-6 w-6" /> Feed
            </Button>
          }
        />
        <EggDialog
          flockId={flock.data.id}
          trigger={
            <Button variant="secondary" size="lg" className="h-auto flex-col gap-1.5 px-6 py-4">
              <Egg className="h-6 w-6" /> Collect Eggs
            </Button>
          }
        />
        <ObservationDialog
          entityType="Flock"
          entityId={flock.data.id}
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
