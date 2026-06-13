// ── Common ─────────────────────────────────────────────

export interface PageResult<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  pages: number
}

// ── Category ──────────────────────────────────────────

export interface Category {
  id: number
  name: string
  color: string | null
  icon: string | null
  sort_order: number
  created_at: string
}

export interface CategoryCreate {
  name: string
  color?: string | null
  icon?: string | null
  sort_order?: number
}

export interface CategoryUpdate {
  name?: string
  color?: string | null
  icon?: string | null
  sort_order?: number
}

// ── Tag ───────────────────────────────────────────────

export interface Tag {
  id: number
  name: string
  created_at: string
}

// ── Question ──────────────────────────────────────────

export type QuestionType = "theory" | "coding" | "scenario" | "behavioral"

export interface Question {
  id: number
  title: string
  content: string | null
  answer: string | null
  category_id: number | null
  difficulty: number
  question_type: QuestionType
  is_active: boolean
  chroma_id: string | null
  created_at: string
  updated_at: string
  category: Category | null
  tags: Tag[]
}

export interface QuestionCreate {
  title: string
  content?: string | null
  answer?: string | null
  category_id?: number | null
  difficulty?: number
  question_type?: QuestionType
  is_active?: boolean
  tags?: string[]
}

export interface QuestionUpdate {
  title?: string
  content?: string | null
  answer?: string | null
  category_id?: number | null
  difficulty?: number
  question_type?: QuestionType
  is_active?: boolean
  tags?: string[] | null
}

// ── Review ────────────────────────────────────────────

export interface CardState {
  question_id: number
  due: string
  stability: number
  difficulty: number
  elapsed_days: number
  scheduled_days: number
  reps: number
  lapses: number
  state: number
  last_review: string | null
}

export interface ReviewStats {
  total_reviewed: number
  again_count: number
  hard_count: number
  good_count: number
  easy_count: number
  due_count: number
}

// ── Interview ─────────────────────────────────────────

export interface InterviewMessage {
  id: number
  role: "user" | "assistant" | "system"
  content: string
  created_at: string
}

export interface InterviewSession {
  id: number
  question_id: number | null
  status: "active" | "completed" | "abandoned"
  overall_score: number | null
  dimension_scores: Record<string, number> | null
  ai_feedback: string | null
  model_used: string | null
  started_at: string
  ended_at: string | null
  created_at: string
  messages: InterviewMessage[]
}

// ── Error Record ──────────────────────────────────────

export interface ErrorRecord {
  id: number
  question_id: number
  source: "review" | "interview"
  error_type: string | null
  user_answer: string | null
  notes: string | null
  is_mastered: boolean
  mastered_at: string | null
  created_at: string
}

// ── Analytics ─────────────────────────────────────────

export interface Overview {
  total_questions: number
  total_reviews: number
  total_interviews: number
  mastered_count: number
  error_count: number
  due_today: number
}

export interface TrendPoint {
  date: string
  count: number
  avg_rating?: number
}

export interface CategoryStat {
  category_id: number | null
  category_name: string
  count: number
  mastered: number
}

export interface HeatmapPoint {
  date: string
  count: number
}
