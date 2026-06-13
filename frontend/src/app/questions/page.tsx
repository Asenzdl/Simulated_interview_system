"use client"

import { useEffect, useState, useCallback } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { QuestionTable } from "@/components/questions/question-table"
import { QuestionDeleteDialog } from "@/components/questions/question-delete-dialog"
import { ImportDialog } from "@/components/questions/import-dialog"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog"
import { CategoryManager } from "@/components/categories/category-manager"
import { questions as questionsApi, categories as categoriesApi } from "@/lib/api"
import { Plus, Search, FolderCog, Upload, Trash2 } from "lucide-react"
import type { Question, Category } from "@/types"
import { toast } from "sonner"

export default function QuestionsPage() {
  const router = useRouter()
  const [items, setItems] = useState<Question[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [pages, setPages] = useState(0)
  const [search, setSearch] = useState("")
  const [categories, setCategories] = useState<Category[]>([])

  const [deleteOpen, setDeleteOpen] = useState(false)
  const [deleteQuestion, setDeleteQuestion] = useState<Question | null>(null)
  const [categoryOpen, setCategoryOpen] = useState(false)
  const [importOpen, setImportOpen] = useState(false)
  const [selectedIds, setSelectedIds] = useState<number[]>([])
  const [batchDeleteOpen, setBatchDeleteOpen] = useState(false)

  const fetchData = useCallback(async (p: number, q?: string) => {
    try {
      const res = await questionsApi.list({ page: p, page_size: 20, search: q || undefined })
      setItems(res.items)
      setTotal(res.total)
      setPage(res.page)
      setPages(res.pages)
    } catch {
      toast.error("加载题目列表失败")
    }
  }, [])

  useEffect(() => {
    fetchData(1)
    categoriesApi.list().then((r) => setCategories(r.items)).catch(() => {})
  }, [fetchData])

  function handleSearch(e: React.FormEvent) {
    e.preventDefault()
    fetchData(1, search)
  }

  async function handleDelete() {
    if (!deleteQuestion) return
    try {
      await questionsApi.delete(deleteQuestion.id)
      toast.success("题目已删除")
      setDeleteOpen(false)
      setDeleteQuestion(null)
      setSelectedIds([])
      fetchData(page, search)
    } catch {
      toast.error("删除失败")
    }
  }

  function handleToggleSelect(id: number) {
    setSelectedIds((prev) => prev.includes(id) ? prev.filter((i) => i !== id) : [...prev, id])
  }

  function handleToggleAll() {
    setSelectedIds((prev) => prev.length === items.length ? [] : items.map((q) => q.id))
  }

  async function handleBatchDelete() {
    try {
      await Promise.all(selectedIds.map((id) => questionsApi.delete(id)))
      toast.success(`已删除 ${selectedIds.length} 道题目`)
      setSelectedIds([])
      setBatchDeleteOpen(false)
      fetchData(page, search)
    } catch {
      toast.error("批量删除失败")
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">题库管理</h2>
          <p className="text-muted-foreground">共 {total} 道题目</p>
        </div>
        <div className="flex gap-2">
          {selectedIds.length > 0 && (
            <Button variant="destructive" onClick={() => setBatchDeleteOpen(true)}>
              <Trash2 className="mr-2 size-4" />
              删除 ({selectedIds.length})
            </Button>
          )}
          <Button variant="outline" onClick={() => setCategoryOpen(true)}>
            <FolderCog className="mr-2 size-4" />
            分类管理
          </Button>
          <Button variant="outline" onClick={() => setImportOpen(true)}>
            <Upload className="mr-2 size-4" />
            批量导入
          </Button>
          <Button onClick={() => router.push("/questions/new")}>
            <Plus className="mr-2 size-4" />
            新建题目
          </Button>
        </div>
      </div>

      <form onSubmit={handleSearch} className="flex gap-2">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="搜索题目..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-9"
          />
        </div>
        <Button type="submit" variant="secondary">搜索</Button>
      </form>

      <QuestionTable
        questions={items}
        selectedIds={selectedIds}
        onToggleSelect={handleToggleSelect}
        onToggleAll={handleToggleAll}
        onEdit={(q) => router.push(`/questions/${q.id}/edit`)}
      />
      {pages > 1 && (
        <div className="flex justify-center gap-2">
          <Button
            variant="outline"
            size="sm"
            disabled={page <= 1}
            onClick={() => fetchData(page - 1, search)}
          >
            上一页
          </Button>
          <span className="flex items-center px-3 text-sm text-muted-foreground">
            {page} / {pages}
          </span>
          <Button
            variant="outline"
            size="sm"
            disabled={page >= pages}
            onClick={() => fetchData(page + 1, search)}
          >
            下一页
          </Button>
        </div>
      )}

      <QuestionDeleteDialog
        open={deleteOpen}
        onOpenChange={setDeleteOpen}
        question={deleteQuestion}
        onConfirm={handleDelete}
      />

      <ImportDialog
        open={importOpen}
        onOpenChange={setImportOpen}
        onSuccess={() => fetchData(1, search)}
      />

      <CategoryManager
        open={categoryOpen}
        onOpenChange={setCategoryOpen}
        categories={categories}
        onChange={() => categoriesApi.list().then((r) => setCategories(r.items))}
      />

      <AlertDialog open={batchDeleteOpen} onOpenChange={setBatchDeleteOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>确认批量删除</AlertDialogTitle>
            <AlertDialogDescription>
              确定要删除选中的 {selectedIds.length} 道题目吗？此操作不可撤销。
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>取消</AlertDialogCancel>
            <AlertDialogAction
              onClick={handleBatchDelete}
              className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
            >
              删除
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  )
}
