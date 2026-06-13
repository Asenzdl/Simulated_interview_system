"use client"

import { useState } from "react"
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Pencil, Trash2, Plus, Check, X } from "lucide-react"
import { categories as categoriesApi } from "@/lib/api"
import type { Category, CategoryCreate, CategoryUpdate } from "@/types"
import { toast } from "sonner"

interface CategoryManagerProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  categories: Category[]
  onChange: () => void
}

const presetColors = [
  "#f7df1e", "#3178c6", "#61dafb", "#ff6b6b",
  "#51cf66", "#ffd43b", "#845ef7", "#ff922b",
]

export function CategoryManager({
  open,
  onOpenChange,
  categories,
  onChange,
}: CategoryManagerProps) {
  const [editing, setEditing] = useState<number | null>(null)
  const [creating, setCreating] = useState(false)
  const [form, setForm] = useState({ name: "", color: presetColors[0] })

  function resetForm() {
    setForm({ name: "", color: presetColors[0] })
    setEditing(null)
    setCreating(false)
  }

  async function handleCreate() {
    if (!form.name.trim()) return
    try {
      await categoriesApi.create({ name: form.name.trim(), color: form.color })
      toast.success("分类创建成功")
      resetForm()
      onChange()
    } catch {
      toast.error("创建失败，名称可能重复")
    }
  }

  async function handleUpdate(id: number) {
    if (!form.name.trim()) return
    try {
      await categoriesApi.update(id, { name: form.name.trim(), color: form.color })
      toast.success("分类更新成功")
      resetForm()
      onChange()
    } catch {
      toast.error("更新失败")
    }
  }

  async function handleDelete(id: number, name: string) {
    if (!confirm(`确定删除分类「${name}」？`)) return
    try {
      await categoriesApi.delete(id)
      toast.success("分类已删除")
      onChange()
    } catch {
      toast.error("删除失败")
    }
  }

  function startEdit(cat: Category) {
    setEditing(cat.id)
    setCreating(false)
    setForm({ name: cat.name, color: cat.color || presetColors[0] })
  }

  return (
    <Sheet open={open} onOpenChange={(v) => { if (!v) resetForm(); onOpenChange(v) }}>
      <SheetContent>
        <SheetHeader>
          <SheetTitle>分类管理</SheetTitle>
          <SheetDescription>添加、编辑或删除题目分类</SheetDescription>
        </SheetHeader>

        <div className="mt-6 space-y-4 px-4">
          {/* 新建 */}
          {creating ? (
            <div className="space-y-3 rounded-lg border p-3">
              <Input
                placeholder="分类名称"
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
              />
              <div className="flex flex-wrap gap-2">
                {presetColors.map((c) => (
                  <button
                    key={c}
                    className={`size-6 rounded-full border-2 ${form.color === c ? "border-foreground" : "border-transparent"}`}
                    style={{ backgroundColor: c }}
                    onClick={() => setForm({ ...form, color: c })}
                  />
                ))}
              </div>
              <div className="flex gap-2">
                <Button size="sm" onClick={handleCreate} disabled={!form.name.trim()}>
                  <Check className="mr-1 size-3" /> 创建
                </Button>
                <Button size="sm" variant="outline" onClick={resetForm}>
                  <X className="mr-1 size-3" /> 取消
                </Button>
              </div>
            </div>
          ) : (
            <Button variant="outline" className="w-full" onClick={() => { setCreating(true); setEditing(null) }}>
              <Plus className="mr-2 size-4" /> 新建分类
            </Button>
          )}

          {/* 列表 */}
          <div className="space-y-2">
            {categories.map((cat) => (
              <div key={cat.id} className="flex items-center gap-3 rounded-lg border p-3">
                {editing === cat.id ? (
                  <div className="flex flex-1 items-center gap-2">
                    <Input
                      value={form.name}
                      onChange={(e) => setForm({ ...form, name: e.target.value })}
                      className="h-8"
                    />
                    <div className="flex gap-1">
                      {presetColors.slice(0, 4).map((c) => (
                        <button
                          key={c}
                          className={`size-5 rounded-full border-2 ${form.color === c ? "border-foreground" : "border-transparent"}`}
                          style={{ backgroundColor: c }}
                          onClick={() => setForm({ ...form, color: c })}
                        />
                      ))}
                    </div>
                    <Button size="icon-xs" onClick={() => handleUpdate(cat.id)}>
                      <Check className="size-3" />
                    </Button>
                    <Button size="icon-xs" variant="outline" onClick={resetForm}>
                      <X className="size-3" />
                    </Button>
                  </div>
                ) : (
                  <>
                    <div
                      className="size-4 rounded-full shrink-0"
                      style={{ backgroundColor: cat.color || "#94a3b8" }}
                    />
                    <span className="flex-1 text-sm font-medium">{cat.name}</span>
                    <Button size="icon-xs" variant="ghost" onClick={() => startEdit(cat)}>
                      <Pencil className="size-3" />
                    </Button>
                    <Button
                      size="icon-xs"
                      variant="ghost"
                      className="text-destructive"
                      onClick={() => handleDelete(cat.id, cat.name)}
                    >
                      <Trash2 className="size-3" />
                    </Button>
                  </>
                )}
              </div>
            ))}
            {categories.length === 0 && (
              <p className="py-8 text-center text-sm text-muted-foreground">暂无分类</p>
            )}
          </div>
        </div>
      </SheetContent>
    </Sheet>
  )
}
