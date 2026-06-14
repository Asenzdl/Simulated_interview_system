"use client"

import { useState, useEffect } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetDescription,
} from "@/components/ui/sheet"
import { FileText } from "lucide-react"
import Markdown from "react-markdown"
import remarkGfm from "remark-gfm"
import { cn } from "@/lib/utils"

interface FlashCardProps {
  title: string
  content: string | null
  answer: string | null
  className?: string
}

export function FlashCard({ title, content, answer, className }: FlashCardProps) {
  const [flipped, setFlipped] = useState(false)
  const [sheetOpen, setSheetOpen] = useState(false)

  const showDetailButton = content && content !== answer

  useEffect(() => {
    setFlipped(false)
  }, [title])

  return (
    <>
      <div
        className={cn("cursor-pointer", className)}
        onClick={() => setFlipped((f) => !f)}
      >
        {!flipped ? (
          <Card className="h-[500px] border-2 border-neutral-700 bg-[#303030] hover:border-neutral-500 transition-colors">
            <CardContent className="flex flex-col items-center justify-center h-full p-8 text-center">
              <h2 className="text-xl font-semibold leading-relaxed text-white">{title}</h2>
            </CardContent>
          </Card>
        ) : (
          <Card className="h-[500px] border-2 border-neutral-200 bg-white flex flex-col">
            <CardContent className="flex-1 flex flex-col items-center p-8 overflow-hidden">
              <div className="prose prose-sm max-w-none text-left overflow-y-auto flex-1 w-full scrollbar-hide">
                <Markdown remarkPlugins={[remarkGfm]}>
                  {answer || "暂无答案"}
                </Markdown>
              </div>
              {showDetailButton && (
                <Button
                  variant="ghost"
                  size="sm"
                  className="text-muted-foreground shrink-0 mt-3"
                  onClick={(e) => {
                    e.stopPropagation()
                    setSheetOpen(true)
                  }}
                >
                  <FileText className="mr-1.5 size-3.5" />
                  查看详细内容
                </Button>
              )}
            </CardContent>
          </Card>
        )}
      </div>

      <Sheet open={sheetOpen} onOpenChange={setSheetOpen}>
        <SheetContent side="right">
          <SheetHeader>
            <SheetTitle>详细内容</SheetTitle>
            <SheetDescription>{title}</SheetDescription>
          </SheetHeader>
          <div className="px-4 pb-4 overflow-y-auto flex-1 prose prose-sm dark:prose-invert max-w-none">
            <Markdown remarkPlugins={[remarkGfm]}>
              {content || ""}
            </Markdown>
          </div>
        </SheetContent>
      </Sheet>
    </>
  )
}
