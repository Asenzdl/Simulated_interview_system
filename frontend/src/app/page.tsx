"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Skeleton } from "@/components/ui/skeleton"
import { BookOpen, RotateCcw, CheckCircle2, CalendarCheck } from "lucide-react"
import { analytics } from "@/lib/api"
import { toast } from "sonner"

interface Overview {
  total_questions: number
  due_count: number
  mastered_count: number
  today_reviewed: number
}

export default function DashboardPage() {
  const router = useRouter()
  const [data, setData] = useState<Overview | null>(null)

  useEffect(() => {
    analytics.overview().then(setData).catch(() => toast.error("加载数据失败"))
  }, [])

  const cards = [
    { title: "总题数", value: data?.total_questions ?? 0, icon: BookOpen, color: "text-blue-500" },
    { title: "待复习", value: data?.due_count ?? 0, icon: RotateCcw, color: "text-orange-500" },
    { title: "已掌握", value: data?.mastered_count ?? 0, icon: CheckCircle2, color: "text-green-500" },
    { title: "今日已复习", value: data?.today_reviewed ?? 0, icon: CalendarCheck, color: "text-purple-500" },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">仪表盘</h2>
        <p className="text-muted-foreground">欢迎使用智能模拟面试系统</p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {cards.map((card) => (
          <Card key={card.title}>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">{card.title}</CardTitle>
              <card.icon className={`size-4 ${card.color}`} />
            </CardHeader>
            <CardContent>
              {data === null ? (
                <Skeleton className="h-8 w-16" />
              ) : (
                <div className="text-2xl font-bold">{card.value}</div>
              )}
            </CardContent>
          </Card>
        ))}
      </div>

      {data && data.due_count > 0 && (
        <Card className="border-primary/30">
          <CardContent className="flex items-center justify-between p-6">
            <div>
              <p className="text-lg font-semibold">今天还有 {data.due_count} 题待复习</p>
              <p className="text-sm text-muted-foreground">坚持每天复习，记忆更牢固</p>
            </div>
            <Button onClick={() => router.push("/review")}>
              开始复习
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
