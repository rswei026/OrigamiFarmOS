import { useMutation, useQueryClient } from '@tanstack/react-query'
import { recommendationsApi } from '@/api/endpoints'
import type { DecisionOption } from '@/api/types'

// Ch.4.6 Decision Intelligence: every Decision recorded against a
// Recommendation, shared by the Morning Briefing and Recommendations
// Review pages (RULE-KM-602: reviews are views over the same data).
export function useDecideRecommendation() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, decision, reason }: { id: string; decision: DecisionOption; reason?: string }) =>
      recommendationsApi.decide(id, decision, reason),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['recommendations'] })
      queryClient.invalidateQueries({ queryKey: ['briefing'] })
    },
  })
}
