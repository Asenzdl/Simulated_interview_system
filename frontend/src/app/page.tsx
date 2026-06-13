import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { BookOpen, RotateCcw, MessageSquare, AlertCircle } from "lucide-react";

const stats = [
  { title: "题目总数", value: "—", icon: BookOpen, description: "加载中..." },
  { title: "待复习", value: "—", icon: RotateCcw, description: "加载中..." },
  { title: "面试次数", value: "—", icon: MessageSquare, description: "加载中..." },
  { title: "错题数", value: "—", icon: AlertCircle, description: "加载中..." },
];

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">仪表盘</h2>
        <p className="text-muted-foreground">欢迎使用智能模拟面试系统</p>
      </div>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <Card key={stat.title}>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">{stat.title}</CardTitle>
              <stat.icon className="size-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
              <p className="text-xs text-muted-foreground">{stat.description}</p>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
