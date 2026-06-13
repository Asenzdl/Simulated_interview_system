const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message)
    this.name = "ApiError"
  }
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json", ...options?.headers },
    ...options,
  })

  if (!res.ok) {
    const body = await res.json().catch(() => ({ detail: res.statusText }))
    throw new ApiError(res.status, body.detail || "请求失败")
  }

  if (res.status === 204) return undefined as T
  return res.json()
}

// ── Questions ─────────────────────────────────────────

import type {
  PageResult,
  Question,
  QuestionCreate,
  QuestionUpdate,
  Category,
  CategoryCreate,
  CategoryUpdate,
} from "@/types"

export const questions = {
  list: (params?: Record<string, string | number | boolean | undefined>) => {
    const qs = new URLSearchParams()
    if (params) {
      Object.entries(params).forEach(([k, v]) => {
        if (v !== undefined && v !== "") qs.set(k, String(v))
      })
    }
    const query = qs.toString()
    return request<PageResult<Question>>(`/api/questions/${query ? `?${query}` : ""}`)
  },
  get: (id: number) => request<Question>(`/api/questions/${id}`),
  create: (data: QuestionCreate) =>
    request<Question>("/api/questions/", { method: "POST", body: JSON.stringify(data) }),
  update: (id: number, data: QuestionUpdate) =>
    request<Question>(`/api/questions/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  delete: (id: number) =>
    request<void>(`/api/questions/${id}`, { method: "DELETE" }),
  import: (fileContent: string, categoryId?: number, difficulty?: number) => {
    const params = new URLSearchParams()
    if (categoryId) params.set("category_id", String(categoryId))
    if (difficulty) params.set("difficulty", String(difficulty))
    const query = params.toString()
    return request<{ imported: number; skipped: number }>(`/api/questions/import${query ? `?${query}` : ""}`, {
      method: "POST",
      headers: { "Content-Type": "text/plain" },
      body: fileContent,
    })
  },
}

// ── Categories ────────────────────────────────────────

export const categories = {
  list: () => request<PageResult<Category>>("/api/categories/"),
  create: (data: CategoryCreate) =>
    request<Category>("/api/categories/", { method: "POST", body: JSON.stringify(data) }),
  update: (id: number, data: CategoryUpdate) =>
    request<Category>(`/api/categories/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  delete: (id: number) =>
    request<void>(`/api/categories/${id}`, { method: "DELETE" }),
}
