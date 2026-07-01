import { useQuery } from '@tanstack/react-query'
import { animalsApi, flocksApi } from '@/api/endpoints'

// Resolves an entity_type/entity_id pair (as referenced by Observations,
// Recommendations, Timeline entries - Ch.2 Ontology) to a human-readable
// label, so recommendation cards never show a bare UUID.
export function useEntityLabels() {
  const animals = useQuery({ queryKey: ['animals'], queryFn: () => animalsApi.list() })
  const flocks = useQuery({ queryKey: ['flocks'], queryFn: () => flocksApi.list() })

  function getLabel(entityType: string, entityId: string): string {
    if (entityType === 'Animal') {
      const animal = animals.data?.find((a) => a.id === entityId)
      return animal ? `${animal.species} ${animal.tag_number}${animal.name ? ` (${animal.name})` : ''}` : 'Animal'
    }
    if (entityType === 'Flock') {
      const flock = flocks.data?.find((f) => f.id === entityId)
      return flock ? `${flock.species} flock '${flock.name}'` : 'Flock'
    }
    return entityType
  }

  return { getLabel, isLoading: animals.isLoading || flocks.isLoading }
}
