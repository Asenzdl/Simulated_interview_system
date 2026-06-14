"use client"

import { cn } from "@/lib/utils"

interface ReviewProgressProps {
  current: number
  total: number
  className?: string
}

export function ReviewProgress({ current, total, className }: ReviewProgressProps) {
  const pct = total > 0 ? (current / total) * 100 : 0

  return (
    <div className={cn("flex items-center gap-3", className)}>
      <div className="flex-1 h-2 bg-muted rounded-full overflow-hidden">
        <div
          className="h-full bg-primary transition-all duration-500 ease-out rounded-full"
          style={{ width: `${pct}%` }}
        />
      </div>
      <span className="text-sm text-muted-foreground tabular-nums whitespace-nowrap">
        {current} / {total}
      </span>
    </div>
  )
}
