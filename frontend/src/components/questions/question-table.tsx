"use client"

import { Checkbox } from "@/components/ui/checkbox"
import { Badge } from "@/components/ui/badge"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { MoreHorizontal, Trash2, ExternalLink } from "lucide-react"
import type { Question } from "@/types"

const difficultyLabels: Record<number, string> = {
  1: "入门",
  2: "初级",
  3: "中级",
  4: "高级",
  5: "专家",
}

const difficultyColors: Record<number, string> = {
  1: "bg-green-100 text-green-800",
  2: "bg-blue-100 text-blue-800",
  3: "bg-yellow-100 text-yellow-800",
  4: "bg-orange-100 text-orange-800",
  5: "bg-red-100 text-red-800",
}

interface QuestionTableProps {
  questions: Question[]
  selectedIds: number[]
  onToggleSelect: (id: number) => void
  onToggleAll: () => void
  onEdit: (q: Question) => void
  onDelete: (q: Question) => void
}

export function QuestionTable({ questions, selectedIds, onToggleSelect, onToggleAll, onEdit, onDelete }: QuestionTableProps) {
  const allSelected = questions.length > 0 && selectedIds.length === questions.length

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead className="w-[40px]">
            <Checkbox checked={allSelected} onCheckedChange={onToggleAll} />
          </TableHead>
          <TableHead className="w-[40%]">题目</TableHead>
          <TableHead>分类</TableHead>
          <TableHead>难度</TableHead>
          <TableHead>标签</TableHead>
          <TableHead className="w-[50px]"></TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {questions.length === 0 ? (
          <TableRow>
            <TableCell colSpan={6} className="h-24 text-center text-muted-foreground">
              暂无题目，点击上方按钮添加
            </TableCell>
          </TableRow>
        ) : (
          questions.map((q) => (
            <TableRow key={q.id} data-selected={selectedIds.includes(q.id) ? "" : undefined} className="data-[selected]:bg-muted/50">
              <TableCell>
                <Checkbox checked={selectedIds.includes(q.id)} onCheckedChange={() => onToggleSelect(q.id)} />
              </TableCell>
              <TableCell className="font-medium group">
                <div className="flex items-center gap-2">
                  <span className="truncate max-w-md">{q.title}</span>
                  <button
                    onClick={() => onEdit(q)}
                    className="hidden group-hover:inline-flex items-center gap-1 text-xs text-muted-foreground hover:text-foreground transition-colors shrink-0"
                  >
                    <ExternalLink className="size-3" />
                    打开
                  </button>
                </div>
              </TableCell>
              <TableCell>
                {q.category ? (
                  <Badge variant="outline" style={{ borderColor: q.category.color || undefined }}>
                    {q.category.name}
                  </Badge>
                ) : (
                  <span className="text-muted-foreground text-sm">—</span>
                )}
              </TableCell>
              <TableCell>
                <span
                  className={`inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium ${difficultyColors[q.difficulty]}`}
                >
                  {difficultyLabels[q.difficulty]}
                </span>
              </TableCell>
              <TableCell>
                <div className="flex flex-wrap gap-1">
                  {q.tags.slice(0, 3).map((tag) => (
                    <Badge key={tag.id} variant="secondary" className="text-xs">
                      {tag.name}
                    </Badge>
                  ))}
                  {q.tags.length > 3 && (
                    <Badge variant="secondary" className="text-xs">+{q.tags.length - 3}</Badge>
                  )}
                </div>
              </TableCell>
              <TableCell>
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="icon-sm">
                      <MoreHorizontal className="size-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem onClick={() => onDelete(q)} className="text-destructive">
                      <Trash2 className="mr-2 size-4" />
                      删除
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </TableCell>
            </TableRow>
          ))
        )}
      </TableBody>
    </Table>
  )
}
