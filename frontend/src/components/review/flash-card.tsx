"use client"

import { useState } from "react"
import { motion, AnimatePresence } from "framer-motion"
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

  return (
    <>
      <div
        className={cn("cursor-pointer [perspective:1200px]", className)}
        onClick={() => setFlipped((f) => !f)}
      >
        <AnimatePresence mode="wait">
          {!flipped ? (
            <motion.div
              key="front"
              initial={{ rotateY: -90, opacity: 0 }}
              animate={{ rotateY: 0, opacity: 1 }}
              exit={{ rotateY: 90, opacity: 0 }}
              transition={{ duration: 0.35, ease: "easeInOut" }}
            >
              <Card className="min-h-[320px] border-2 hover:border-primary/40 transition-colors">
                <CardContent className="flex flex-col items-center justify-center h-full p-8 text-center gap-4">
                  <span className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
                    题目
                  </span>
                  <h2 className="text-xl font-semibold leading-relaxed">{title}</h2>
                  <span className="text-xs text-muted-foreground mt-4 opacity-60">
                    点击查看答案
                  </span>
                </CardContent>
              </Card>
            </motion.div>
          ) : (
            <motion.div
              key="back"
              initial={{ rotateY: -90, opacity: 0 }}
              animate={{ rotateY: 0, opacity: 1 }}
              exit={{ rotateY: 90, opacity: 0 }}
              transition={{ duration: 0.35, ease: "easeInOut" }}
            >
              <Card className="min-h-[320px] border-2 border-primary/30 bg-primary/[0.03]">
                <CardContent className="flex flex-col items-center justify-center h-full p-8 text-center gap-4">
                  <span className="text-xs font-medium text-primary uppercase tracking-wider">
                    答案
                  </span>
                  <div className="prose prose-sm dark:prose-invert max-w-none text-left">
                    <Markdown remarkPlugins={[remarkGfm]}>
                      {answer || "暂无答案"}
                    </Markdown>
                  </div>
                  {showDetailButton && (
                    <Button
                      variant="ghost"
                      size="sm"
                      className="text-muted-foreground"
                      onClick={(e) => {
                        e.stopPropagation()
                        setSheetOpen(true)
                      }}
                    >
                      <FileText className="mr-1.5 size-3.5" />
                      查看详细内容
                    </Button>
                  )}
                  <span className="text-xs text-muted-foreground mt-2 opacity-60">
                    点击返回题目
                  </span>
                </CardContent>
              </Card>
            </motion.div>
          )}
        </AnimatePresence>
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
