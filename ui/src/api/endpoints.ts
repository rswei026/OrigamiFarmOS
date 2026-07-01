import { apiClient } from './client'
import { writeOrQueue } from '@/offline/syncQueue'
import type {
  Animal,
  Flock,
  Location,
  MorningBriefing,
  Recommendation,
  DecisionOption,
  FeedItem,
  FeedLot,
  TimelineEntry,
} from './types'

// Read paths always go straight through the API client (TanStack Query
// handles caching); write paths for offline-critical workflows go through
// `writeOrQueue` (Ch.16). This mirrors the read/write asymmetry in the
// handbook: reads are recomputed views, writes are events (§3.2, §4.8.3).

export const briefingApi = {
  morning: () => apiClient.get<MorningBriefing>('/briefing/morning').then((r) => r.data),
}

export const locationsApi = {
  list: () => apiClient.get<Location[]>('/locations').then((r) => r.data),
}

export const animalsApi = {
  list: (params?: { species?: string; location_id?: string }) =>
    apiClient.get<Animal[]>('/animals', { params }).then((r) => r.data),
  get: (id: string) => apiClient.get<Animal>(`/animals/${id}`).then((r) => r.data),
  timeline: (id: string) => apiClient.get<TimelineEntry[]>(`/animals/${id}/timeline`).then((r) => r.data),
  register: (payload: Omit<Animal, 'id' | 'farm_id' | 'status'> & { id?: string }) =>
    writeOrQueue('/animals', { id: payload.id ?? crypto.randomUUID(), ...payload }, `Register animal ${payload.tag_number}`),
}

export const flocksApi = {
  list: (params?: { species?: string }) => apiClient.get<Flock[]>('/flocks', { params }).then((r) => r.data),
  get: (id: string) => apiClient.get<Flock>(`/flocks/${id}`).then((r) => r.data),
  timeline: (id: string) => apiClient.get<TimelineEntry[]>(`/flocks/${id}/timeline`).then((r) => r.data),
  register: (payload: Omit<Flock, 'id' | 'farm_id' | 'active'> & { id?: string }) =>
    writeOrQueue('/flocks', { id: payload.id ?? crypto.randomUUID(), ...payload }, `Register flock ${payload.name}`),
}

export const observationsApi = {
  create: (payload: {
    entity_type: string
    entity_id: string
    observation_type: string
    value_numeric?: number
    value_text?: string
    unit?: string
    quality: string
    notes?: string
  }) => writeOrQueue('/observations', { id: crypto.randomUUID(), source: 'worker', ...payload }, `Observation: ${payload.observation_type}`),
}

export const feedApi = {
  items: () => apiClient.get<FeedItem[]>('/feed/items').then((r) => r.data),
  lots: (feed_item_id?: string) => apiClient.get<FeedLot[]>('/feed/lots', { params: { feed_item_id } }).then((r) => r.data),
  distribute: (payload: { feed_lot_id: string; entity_type: string; entity_id: string; quantity: number }) =>
    writeOrQueue('/feed/distributions', { id: crypto.randomUUID(), ...payload }, 'Feed distribution'),
}

export const dairyApi = {
  create: (payload: { animal_id: string; session: 'AM' | 'PM'; volume_liters: number; destination?: string }) =>
    writeOrQueue('/dairy/milk-sessions', { id: crypto.randomUUID(), ...payload }, 'Milk record'),
}

export const poultryApi = {
  create: (payload: {
    flock_id: string
    total_eggs: number
    broken_eggs?: number
    consumed?: number
    sold?: number
    hatching?: number
  }) => writeOrQueue('/poultry/egg-collections', { id: crypto.randomUUID(), ...payload }, 'Egg collection'),
}

export const recommendationsApi = {
  list: (params?: { status_filter?: string; category?: string; priority?: string }) =>
    apiClient.get<Recommendation[]>('/recommendations', { params }).then((r) => r.data),
  decide: (recommendationId: string, decision: DecisionOption, reason?: string) =>
    apiClient
      .post(`/recommendations/${recommendationId}/decisions`, {
        id: crypto.randomUUID(),
        decision,
        reason,
      })
      .then((r) => r.data),
}
