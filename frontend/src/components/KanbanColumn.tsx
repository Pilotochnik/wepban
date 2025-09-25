import { SortableContext, verticalListSortingStrategy } from '@dnd-kit/sortable'
import { useDroppable } from '@dnd-kit/core'
import { TaskCard } from './TaskCard'
import { Task } from '@/lib/api'
import { cn } from '@/lib/utils'

interface KanbanColumnProps {
  id: string
  title: string
  color: string
  tasks: Task[]
}

export function KanbanColumn({ id, title, color, tasks }: KanbanColumnProps) {
  const { setNodeRef, isOver } = useDroppable({
    id,
  })

  return (
    <div className="flex flex-col">
      <div className="flex items-center gap-2 mb-4">
        <div className={cn("w-3 h-3 rounded-full", color)} />
        <h3 className="font-semibold text-gray-900">{title}</h3>
        <span className="ml-auto text-sm text-gray-500 bg-gray-100 px-2 py-1 rounded-full">
          {tasks.length}
        </span>
      </div>
      
      <div
        ref={setNodeRef}
        className={cn(
          "min-h-[400px] p-4 rounded-lg border-2 border-dashed transition-colors",
          isOver ? "border-primary bg-primary/5" : "border-gray-200 bg-gray-50"
        )}
      >
        <SortableContext items={tasks.map(task => task.id)} strategy={verticalListSortingStrategy}>
          <div className="space-y-3">
            {tasks.map((task) => (
              <TaskCard key={task.id} task={task} />
            ))}
            {tasks.length === 0 && (
              <div className="text-center text-gray-500 py-8">
                <p>Нет задач</p>
              </div>
            )}
          </div>
        </SortableContext>
      </div>
    </div>
  )
}
