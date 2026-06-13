"use client"

import { useEffect, useState } from "react"
import { QuestionForm } from "@/components/questions/question-form"
import { questions as questionsApi, categories as categoriesApi } from "@/lib/api"
import type { Category, QuestionCreate, QuestionUpdate } from "@/types"
import { toast } from "sonner"

export default function NewQuestionPage() {
  const [categories, setCategories] = useState<Category[]>([])

  useEffect(() => {
    categoriesApi.list().then((r) => setCategories(r.items)).catch(() => toast.error("加载分类失败"))
  }, [])

  async function handleSubmit(data: QuestionCreate | QuestionUpdate) {
    await questionsApi.create(data as QuestionCreate)
  }

  return <QuestionForm categories={categories} onSubmit={handleSubmit} />
}
