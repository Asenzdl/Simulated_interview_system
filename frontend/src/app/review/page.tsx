"use client"

import { useEffect, useState, useCallback } from "react"
import { review, questions as questionsApi } from "@/lib/api"
import { FlashCard } from "@/components/review/flash-card"
import { RatingButtons } from "@/components/review/rating-buttons"
import { ReviewProgress } from "@/components/review/review-progress"
import { ReviewComplete } from "@/components/review/review-complete"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Skeleton } from "@/components/ui/skeleton"
import { RotateCcw } from "lucide-react"
import type { Question, CardState, ReviewStats } from "@/types"
import { toast } from "sonner"

export default function ReviewPage() {
  const [loading, setLoading] = useState(true)
  const [card, setCard] = useState<CardState | null>(null)
  const [question, setQuestion] = useState<Question | null>(null)
  const [queueTotal, setQueueTotal] = useState(0)
  const [reviewed, setReviewed] = useState(0)
  const [rating, setRating] = useState(false)
  const [completeOpen, setCompleteOpen] = useState(false)
  const [stats, setStats] = useState<ReviewStats | null>(null)

  const loadNext = useCallback(async () => {
    try {
      const [nextCard, queueRes] = await Promise.all([
        review.next(),
        review.queueCount(),
      ])
      setQueueTotal(queueRes.count)

      if (!nextCard) {
        // No more cards
        const s = await review.stats()
        setStats(s)
        setCompleteOpen(true)
        setCard(null)
        setQuestion(null)
        return
      }

      setCard(nextCard)
      // Fetch question details
      const q = await questionsApi.get(nextCard.question_id)
      setQuestion(q)
    } catch {
      toast.error("加载卡片失败")
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    loadNext()
  }, [loadNext])

  async function handleRate(ratingValue: number) {
    if (!card || rating) return
    setRating(true)
    try {
      await review.rate(card.question_id, ratingValue)
      setReviewed((n) => n + 1)
      await loadNext()
    } catch {
      toast.error("评分失败")
    } finally {
      setRating(false)
    }
  }

  async function handleRestart() {
    setCompleteOpen(false)
    setReviewed(0)
    setLoading(true)
    await loadNext()
  }

  if (loading) {
    return (
      <div className="max-w-2xl mx-auto space-y-6">
        <Skeleton className="h-8 w-48" />
        <Skeleton className="h-2 w-full" />
        <Skeleton className="h-80 w-full" />
        <Skeleton className="h-12 w-full" />
      </div>
    )
  }

  if (!card || !question) {
    return (
      <div className="max-w-2xl mx-auto space-y-6">
        <div className="text-center py-20 space-y-4">
          <RotateCcw className="mx-auto size-12 text-muted-foreground" />
          <h2 className="text-2xl font-bold">暂无待复习卡片</h2>
          <p className="text-muted-foreground">所有题目都已复习完毕，稍后再来</p>
          <Button onClick={handleRestart}>刷新</Button>
        </div>

        {stats && (
          <ReviewComplete
            open={completeOpen}
            onOpenChange={setCompleteOpen}
            stats={stats}
            reviewed={reviewed}
          />
        )}
      </div>
    )
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold tracking-tight">闪卡复习</h2>
        <span className="text-sm text-muted-foreground">
          队列 {queueTotal} 题
        </span>
      </div>

      <ReviewProgress current={reviewed} total={queueTotal + reviewed} />

      <FlashCard
        title={question.title}
        content={question.content}
        answer={question.answer}
      />

      <Card>
        <CardContent className="p-4">
          <RatingButtons onRate={handleRate} disabled={rating} />
        </CardContent>
      </Card>

      {stats && (
        <ReviewComplete
          open={completeOpen}
          onOpenChange={(open) => {
            setCompleteOpen(open)
            if (!open) handleRestart()
          }}
          stats={stats}
          reviewed={reviewed}
        />
      )}
    </div>
  )
}
