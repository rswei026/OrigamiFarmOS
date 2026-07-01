import type { LucideIcon } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'

export interface QuickAction {
  key: string
  label: string
  icon: LucideIcon
  onClick: () => void
}

// Ch.13 §13.3 / concept note §17: consistent icon + label quick-action
// bar, reused wherever quick actions appear (Morning Briefing, Animal and
// Flock profiles) - Constitution Principle 12 (Simplicity Over Complexity).
export function QuickActionBar({ actions, className }: { actions: QuickAction[]; className?: string }) {
  return (
    <div className={cn('flex flex-wrap gap-3', className)}>
      {actions.map((action) => (
        <Button key={action.key} variant="secondary" size="lg" onClick={action.onClick} className="flex-col h-auto py-4 px-6 gap-1.5">
          <action.icon className="h-6 w-6" />
          <span className="text-sm">{action.label}</span>
        </Button>
      ))}
    </div>
  )
}
