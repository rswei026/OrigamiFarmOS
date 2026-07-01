import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import type { TimelineEntry } from '@/api/types'

// Ch.4.8 Knowledge Timeline: one component reused across Animal and Flock
// profiles (§4.8.7 Codex notes) rather than per-entity-type timeline UIs.
const ICON: Record<string, string> = {
  observation: '\u{1F441}\u{FE0F}', // eye
  milk_record: '\u{1F95B}', // milk glass
  egg_collection: '\u{1F95A}', // egg
  feed_distribution: '\u{1F33E}', // sheaf
  recommendation: '\u{1F4A1}', // bulb
}

export function Timeline({ entries }: { entries: TimelineEntry[] }) {
  if (entries.length === 0) {
    return <p className="text-sm text-muted-foreground">No history yet.</p>
  }
  return (
    <ol className="flex flex-col gap-3">
      {entries.map((entry) => (
        <li key={`${entry.type}-${entry.id}`}>
          <Card>
            <CardContent className="flex items-start gap-3 p-4">
              <span className="text-xl leading-none">{ICON[entry.type] ?? '•'}</span>
              <div className="flex-1">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="text-sm font-medium">{entry.summary}</span>
                  {entry.type === 'recommendation' && entry.priority ? (
                    <Badge variant="outline">{String(entry.priority)}</Badge>
                  ) : null}
                </div>
                <div className="text-xs text-muted-foreground">{new Date(entry.timestamp).toLocaleString()}</div>
              </div>
            </CardContent>
          </Card>
        </li>
      ))}
    </ol>
  )
}
