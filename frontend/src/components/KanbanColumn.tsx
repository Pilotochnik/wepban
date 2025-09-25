import { TaskCard } from './TaskCard'
import { Task } from '@/lib/api'
import { cn } from '@/lib/utils'

interface KanbanColumnProps {
  id: string
  title: string
  color: string
  tasks: Task[]
  onStatusChange?: (taskId: number, newStatus: string) => void
}

export function KanbanColumn({ id, title, color, tasks, onStatusChange }: KanbanColumnProps) {
  return (
    <div className="flex flex-col group">
      <div className="flex items-center gap-2 mb-4">
        <div className={cn("w-3 h-3 rounded-full group-hover:scale-110 transition-transform duration-300", color)} />
        <h3 className="font-semibold text-gray-900 group-hover:text-blue-600 transition-colors duration-300">{title}</h3>
        <span className="ml-auto text-sm text-gray-500 bg-gray-100 px-2 py-1 rounded-full group-hover:bg-blue-100 group-hover:text-blue-600 transition-all duration-300">
          {tasks.length}
        </span>
      </div>
      
      <div
        className={cn(
          "min-h-[300px] sm:min-h-[400px] p-3 sm:p-4 rounded-lg border-2 border-dashed transition-all duration-300 hover:border-blue-300 hover:bg-blue-50/50",
          "border-gray-200 bg-gray-50"
        )}
      >
        <div className="space-y-3">
          {tasks.map((task) => (
            <TaskCard key={task.id} task={task} onStatusChange={onStatusChange} />
          ))}
          {tasks.length === 0 && (
            <div className="text-center text-gray-500 py-8">
              <p>Нет задач</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
