"use client"

import { useEffect, useState } from "react"
import { useParams, useRouter } from "next/navigation"
import { QuestionForm } from "@/components/questions/question-form"
import { questions as questionsApi, categories as categoriesApi } from "@/lib/api"
import type { Category, Question, QuestionUpdate } from "@/types"
import { toast } from "sonner"

export default function EditQuestionPage() {
  const params = useParams()
  const router = useRouter()
  const id = Number(params.id)
  const [question, setQuestion] = useState<Question | null>(null)
  const [categories, setCategories] = useState<Category[]>([])

  useEffect(() => {
    Promise.all([
      questionsApi.get(id).catch(() => null),
      categoriesApi.list().catch(() => ({ items: [] })),
    ]).then(([q, cats]) => {
      if (!q) {
        toast.error("题目不存在")
        router.push("/questions")
        return
      }
      setQuestion(q)
      setCategories(cats.items)
    })
  }, [id, router])

  async function handleSubmit(data: QuestionUpdate) {
    await questionsApi.update(id, data)
  }

  if (!question) return null

  return <QuestionForm question={question} categories={categories} onSubmit={handleSubmit} />
}
