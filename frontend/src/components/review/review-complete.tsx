"use client"

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import type { ReviewStats } from "@/types"

interface ReviewCompleteProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  stats: ReviewStats
  reviewed: number
}

export function ReviewComplete({ open, onOpenChange, stats, reviewed }: ReviewCompleteProps) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>复习完成</DialogTitle>
          <DialogDescription>本次复习总结</DialogDescription>
        </DialogHeader>

        <div className="space-y-4 py-4">
          <div className="text-center">
            <span className="text-5xl font-bold text-primary">{reviewed}</span>
            <p className="text-sm text-muted-foreground mt-1">本次复习题数</p>
          </div>

          <div className="grid grid-cols-4 gap-2 text-center">
            <div className="rounded-lg bg-red-500/10 p-2">
              <p className="text-lg font-semibold text-red-500">{stats.again_count}</p>
              <p className="text-xs text-muted-foreground">忘了</p>
            </div>
            <div className="rounded-lg bg-orange-500/10 p-2">
              <p className="text-lg font-semibold text-orange-500">{stats.hard_count}</p>
              <p className="text-xs text-muted-foreground">模糊</p>
            </div>
            <div className="rounded-lg bg-green-500/10 p-2">
              <p className="text-lg font-semibold text-green-500">{stats.good_count}</p>
              <p className="text-xs text-muted-foreground">记得</p>
            </div>
            <div className="rounded-lg bg-blue-500/10 p-2">
              <p className="text-lg font-semibold text-blue-500">{stats.easy_count}</p>
              <p className="text-xs text-muted-foreground">秒答</p>
            </div>
          </div>
        </div>

        <DialogFooter>
          <Button onClick={() => onOpenChange(false)} className="w-full">
            完成
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
