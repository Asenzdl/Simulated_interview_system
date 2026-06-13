"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ArrowLeft, Save } from "lucide-react"
import type { Question, QuestionCreate, QuestionUpdate, Category } from "@/types"
import { toast } from "sonner"

const difficultyOptions = [
  { value: 1, label: "入门" },
  { value: 2, label: "初级" },
  { value: 3, label: "中级" },
  { value: 4, label: "高级" },
  { value: 5, label: "专家" },
]

interface QuestionFormProps {
  question?: Question | null
  categories: Category[]
  onSubmit: (data: QuestionCreate | QuestionUpdate) => Promise<void>
}

export function QuestionForm({ question, categories, onSubmit }: QuestionFormProps) {
  const router = useRouter()
  const isEdit = !!question
  const [loading, setLoading] = useState(false)
  const [form, setForm] = useState({
    title: question?.title || "",
    content: question?.content || "",
    answer: question?.answer || "",
    category_id: question?.category_id?.toString() || "__none__",
    difficulty: question?.difficulty?.toString() || "1",
    tags: question?.tags.map((t) => t.name).join(", ") || "",
  })

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!form.title.trim()) return

    setLoading(true)
    try {
      const data = {
        title: form.title.trim(),
        content: form.content.trim() || null,
        answer: form.answer.trim() || null,
        category_id:
          form.category_id && form.category_id !== "__none__"
            ? Number(form.category_id)
            : null,
        difficulty: Number(form.difficulty),
        tags: form.tags
          .split(",")
          .map((t) => t.trim())
          .filter(Boolean),
      }
      await onSubmit(data)
      toast.success(isEdit ? "题目更新成功" : "题目创建成功")
      router.replace("/questions")
    } catch (err) {
      const message = err instanceof Error ? err.message : "保存失败"
      toast.error(message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" onClick={() => router.back()}>
          <ArrowLeft className="size-4" />
        </Button>
        <div>
          <h2 className="text-2xl font-bold tracking-tight">
            {isEdit ? "编辑题目" : "新建题目"}
          </h2>
          <p className="text-muted-foreground">
            {isEdit ? "修改题目信息" : "填写题目信息创建新题目"}
          </p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle className="text-base">基本信息</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid gap-2">
              <Label htmlFor="title">题目标题 *</Label>
              <Input
                id="title"
                value={form.title}
                onChange={(e) => setForm({ ...form, title: e.target.value })}
                placeholder="输入题目标题"
                required
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="grid gap-2">
                <Label>分类</Label>
                <Select
                  value={form.category_id}
                  onValueChange={(v) => setForm({ ...form, category_id: v })}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="选择分类" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="__none__">无分类</SelectItem>
                    {categories.map((c) => (
                      <SelectItem key={c.id} value={c.id.toString()}>
                        {c.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="grid gap-2">
                <Label>难度</Label>
                <Select
                  value={form.difficulty}
                  onValueChange={(v) => setForm({ ...form, difficulty: v })}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {difficultyOptions.map((d) => (
                      <SelectItem key={d.value} value={d.value.toString()}>
                        {d.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="grid gap-2">
              <Label htmlFor="tags">标签</Label>
              <Input
                id="tags"
                value={form.tags}
                onChange={(e) => setForm({ ...form, tags: e.target.value })}
                placeholder="用逗号分隔，如：闭包, JavaScript, 基础"
              />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-base">题目内容</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid gap-2">
              <Label htmlFor="content">详细描述（Markdown）</Label>
              <Textarea
                id="content"
                value={form.content}
                onChange={(e) => setForm({ ...form, content: e.target.value })}
                placeholder="题目的详细描述、场景、约束条件等..."
                rows={8}
              />
            </div>

            <div className="grid gap-2">
              <Label htmlFor="answer">参考答案（Markdown）</Label>
              <Textarea
                id="answer"
                value={form.answer}
                onChange={(e) => setForm({ ...form, answer: e.target.value })}
                placeholder="标准答案..."
                rows={8}
              />
            </div>
          </CardContent>
        </Card>

        <div className="flex justify-end gap-3">
          <Button type="button" variant="outline" onClick={() => router.back()}>
            取消
          </Button>
          <Button type="submit" disabled={loading || !form.title.trim()}>
            <Save className="mr-2 size-4" />
            {loading ? "保存中..." : isEdit ? "保存修改" : "创建题目"}
          </Button>
        </div>
      </form>
    </div>
  )
}
