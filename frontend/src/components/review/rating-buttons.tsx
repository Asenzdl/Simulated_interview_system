"use client"

import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

interface RatingButtonsProps {
  onRate: (rating: number) => void
  disabled?: boolean
}

const ratings = [
  { value: 1, label: "忘了", color: "bg-red-500 hover:bg-red-600 text-white" },
  { value: 2, label: "模糊", color: "bg-orange-500 hover:bg-orange-600 text-white" },
  { value: 3, label: "记得", color: "bg-green-500 hover:bg-green-600 text-white" },
  { value: 4, label: "秒答", color: "bg-blue-500 hover:bg-blue-600 text-white" },
]

export function RatingButtons({ onRate, disabled }: RatingButtonsProps) {
  return (
    <div className="flex gap-3 justify-center">
      {ratings.map((r) => (
        <Button
          key={r.value}
          onClick={() => onRate(r.value)}
          disabled={disabled}
          className={cn("flex-1 max-w-24 h-12 text-sm font-medium", r.color)}
        >
          {r.label}
        </Button>
      ))}
    </div>
  )
}
