"use client"

import { useState, useRef, useCallback } from "react"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Upload, FileText, X } from "lucide-react"
import { questions as questionsApi, categories as categoriesApi } from "@/lib/api"
import type { Category } from "@/types"
import { toast } from "sonner"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Label } from "@/components/ui/label"

interface ImportDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSuccess: () => void
}

export function ImportDialog({ open, onOpenChange, onSuccess }: ImportDialogProps) {
  const [file, setFile] = useState<File | null>(null)
  const [content, setContent] = useState("")
  const [preview, setPreview] = useState<string[]>([])
  const [loading, setLoading] = useState(false)
  const [categories, setCategories] = useState<Category[]>([])
  const [categoryId, setCategoryId] = useState("__none__")
  const fileInputRef = useRef<HTMLInputElement>(null)

  // 加载分类列表
  useState(() => {
    categoriesApi.list().then((r) => setCategories(r.items)).catch(() => {})
  })

  const parsePreview = useCallback((text: string) => {
    const blocks = text.split(/\n---\n/).filter((b) => b.trim())
    const titles = blocks.map((b) => {
      const firstLine = b.trim().split("\n")[0]
      return firstLine.replace(/^##\s*/, "").trim()
    })
    setPreview(titles)
  }, [])

  function handleFile(f: File) {
    setFile(f)
    const reader = new FileReader()
    reader.onload = (e) => {
      const text = e.target?.result as string
      setContent(text)
      parsePreview(text)
    }
    reader.readAsText(f)
  }

  function handleDrop(e: React.DragEvent) {
    e.preventDefault()
    const f = e.dataTransfer.files[0]
    if (f) handleFile(f)
  }

  function handleFileInput(e: React.ChangeEvent<HTMLInputElement>) {
    const f = e.target.files?.[0]
    if (f) handleFile(f)
  }

  function reset() {
    setFile(null)
    setContent("")
    setPreview([])
    setCategoryId("__none__")
  }

  async function handleSubmit() {
    if (!content) return
    setLoading(true)
    try {
      const catId = categoryId !== "__none__" ? Number(categoryId) : undefined
      const result = await questionsApi.import(content, catId)
      if (result.skipped > 0) {
        toast.success(`导入完成：${result.imported} 道新题目，${result.skipped} 道重复跳过`)
      } else {
        toast.success(`成功导入 ${result.imported} 道题目`)
      }
      reset()
      onOpenChange(false)
      onSuccess()
    } catch {
      toast.error("导入失败")
    } finally {
      setLoading(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={(v) => { if (!v) reset(); onOpenChange(v) }}>
      <DialogContent className="sm:max-w-xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>批量导入题目</DialogTitle>
          <DialogDescription>
            上传 Markdown 文件，按 `---` 分隔每道题目
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4">
          {/* 上传区域 */}
          {!file ? (
            <div
              className="flex flex-col items-center justify-center gap-3 rounded-lg border-2 border-dashed p-8 transition-colors hover:border-primary/50 cursor-pointer"
              onDragOver={(e) => e.preventDefault()}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
            >
              <Upload className="size-8 text-muted-foreground" />
              <p className="text-sm text-muted-foreground">
                拖拽文件到此处，或点击选择文件
              </p>
              <p className="text-xs text-muted-foreground">支持 .md / .txt 文件</p>
              <input
                ref={fileInputRef}
                type="file"
                accept=".md,.txt"
                className="hidden"
                onChange={handleFileInput}
              />
            </div>
          ) : (
            <div className="flex items-center gap-3 rounded-lg border p-3">
              <FileText className="size-5 text-muted-foreground" />
              <div className="flex-1">
                <p className="text-sm font-medium">{file.name}</p>
                <p className="text-xs text-muted-foreground">
                  {preview.length} 道题目
                </p>
              </div>
              <Button variant="ghost" size="icon-sm" onClick={reset}>
                <X className="size-4" />
              </Button>
            </div>
          )}

          {/* 分类选择 */}
          {file && (
            <div className="grid gap-2">
              <Label>导入到分类（可选）</Label>
              <Select value={categoryId} onValueChange={setCategoryId}>
                <SelectTrigger>
                  <SelectValue placeholder="选择分类" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="__none__">不指定分类</SelectItem>
                  {categories.map((c) => (
                    <SelectItem key={c.id} value={c.id.toString()}>
                      {c.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          )}

          {/* 预览 */}
          {preview.length > 0 && (
            <div className="max-h-64 space-y-1 overflow-y-auto rounded-lg border p-3">
              <p className="mb-2 text-xs font-medium text-muted-foreground">预览题目标题</p>
              {preview.map((title, i) => (
                <p key={i} className="text-sm break-words whitespace-pre-wrap">
                  {i + 1}. {title}
                </p>
              ))}
            </div>
          )}
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            取消
          </Button>
          <Button onClick={handleSubmit} disabled={!content || loading}>
            {loading ? "导入中..." : "确认导入"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
