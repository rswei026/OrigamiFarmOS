// Mirrors backend/app/schemas/* (handbook Chapter 15 §15.2: OpenAPI is
// authoritative; these types are a hand-written mirror for this pass).

export type AnimalSpecies = 'cow' | 'sheep' | 'goat' | 'horse'
export type AnimalStatus =
  | 'registered'
  | 'active'
  | 'under_observation'
  | 'in_treatment'
  | 'withdrawal_period'
  | 'pregnant'
  | 'sold'
  | 'deceased'
export type FlockSpecies = 'chicken' | 'duck' | 'turkey'

export interface Animal {
  id: string
  farm_id: string
  tag_number: string
  name: string | null
  species: AnimalSpecies
  breed: string | null
  sex: string
  birth_date: string | null
  current_location_id: string | null
  status: AnimalStatus
}

export interface Flock {
  id: string
  farm_id: string
  name: string
  species: FlockSpecies
  bird_count: number
  location_id: string | null
  active: boolean
}

export interface Location {
  id: string
  farm_id: string
  name: string
  location_type: string
  parent_id: string | null
  active: boolean
}

export type ObservationQuality = 'A' | 'B' | 'C' | 'D'

export interface TimelineEntry {
  type: string
  timestamp: string
  summary: string
  id: string
  [key: string]: unknown
}

export type RecommendationCategory = 'health' | 'production' | 'inventory' | 'financial' | 'breeding' | 'compliance'
export type RecommendationPriority = 'urgent' | 'high' | 'medium' | 'low'
export type ConfidenceBand = 'high' | 'medium' | 'low'
export type RecommendationStatus = 'open' | 'accepted' | 'rejected' | 'monitoring' | 'action_in_progress' | 'closed'

export interface Recommendation {
  id: string
  farm_id: string
  entity_type: string
  entity_id: string
  category: RecommendationCategory
  priority: RecommendationPriority
  confidence_score: number
  confidence_band: ConfidenceBand
  evidence: {
    signals?: { signal: string; detail: string; weight: number; confidence: number }[]
    observations?: { id: string; type: string; value: unknown; unit: string | null; observed_at: string; quality: string }[]
  }
  explanation: string
  explanation_provider: string
  suggested_action: string
  missing_information: string | null
  due_date: string | null
  status: RecommendationStatus
  created_at: string
}

export type DecisionOption = 'accept' | 'reject' | 'monitor' | 'delegate' | 'escalate' | 'postpone'

export interface FeedItem {
  id: string
  farm_id: string
  name: string
  unit: string
}

export interface FeedLot {
  id: string
  farm_id: string
  feed_item_id: string
  source: 'purchase' | 'production'
  quantity_received: number
  unit_cost: number
  received_at: string
  remaining: number | null
}

export interface MorningBriefing {
  date: string
  urgent_recommendations: {
    id: string
    entity_type: string
    entity_id: string
    category: RecommendationCategory
    priority: RecommendationPriority
    confidence_band: ConfidenceBand
    explanation: string
    suggested_action: string
  }[]
  open_recommendations_by_category: Record<string, number>
  feed_stock_warnings: { feed_item_id: string; feed_item_name: string; days_remaining: number }[]
  todays_activity: {
    milk_recorded: boolean
    eggs_recorded: boolean
    observations_recorded_today: number
  }
}
