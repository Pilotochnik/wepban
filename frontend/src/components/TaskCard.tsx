import { useSortable } from '@dnd-kit/sortable'
import { CSS } from '@dnd-kit/utilities'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Task } from '@/lib/api'
import { cn } from '@/lib/utils'
import { format } from 'date-fns'
import { ru } from 'date-fns/locale'
import { Eye } from 'lucide-react'
import { useState } from 'react'
import { TaskDetailModal } from './TaskDetailModal'

interface TaskCardProps {
  task: Task
  isDragging?: boolean
  onStatusChange?: (taskId: number, newStatus: string) => void
}

const priorityColors = {
  low: 'bg-gray-100 text-gray-800',
  medium: 'bg-blue-100 text-blue-800',
  high: 'bg-orange-100 text-orange-800',
  urgent: 'bg-red-100 text-red-800',
}

const priorityLabels = {
  low: 'Низкий',
  medium: 'Средний',
  high: 'Высокий',
  urgent: 'Срочный',
}

export function TaskCard({ task, isDragging, onStatusChange }: TaskCardProps) {
  const [showDetailModal, setShowDetailModal] = useState(false)
  
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging: isSortableDragging,
  } = useSortable({
    id: task.id,
  })

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  }

  return (
    <Card
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      className={cn(
        "cursor-grab active:cursor-grabbing hover:shadow-md transition-shadow",
        (isDragging || isSortableDragging) && "opacity-50 rotate-3 scale-105"
      )}
    >
      <CardContent className="p-4">
        <div className="space-y-3">
          <div>
            <h4 className="font-medium text-sm text-gray-900 line-clamp-2">
              {task.title}
            </h4>
            {task.description && (
              <p className="text-xs text-gray-600 mt-1 line-clamp-3">
                {task.description}
              </p>
            )}
          </div>

          <div className="flex items-center justify-between">
            <span
              className={cn(
                "px-2 py-1 text-xs rounded-full font-medium",
                priorityColors[task.priority]
              )}
            >
              {priorityLabels[task.priority]}
            </span>

            {task.deadline && (
              <span className={cn(
                "text-xs px-2 py-1 rounded-full",
                new Date(task.deadline) < new Date() 
                  ? "bg-red-100 text-red-800" 
                  : "bg-gray-100 text-gray-600"
              )}>
                {format(new Date(task.deadline), 'dd.MM', { locale: ru })}
              </span>
            )}
          </div>

          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>
              {format(new Date(task.created_at), 'dd.MM.yyyy', { locale: ru })}
            </span>
            {task.assigned_to && (
              <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                Назначено
              </span>
            )}
          </div>

          {/* Кнопка для детального просмотра */}
          <div className="mt-3 pt-2 border-t border-gray-100">
            <Button 
              variant="outline" 
              size="sm" 
              className="w-full"
              onClick={() => setShowDetailModal(true)}
            >
              <Eye className="h-4 w-4 mr-2" />
              Подробнее
            </Button>
          </div>
        </div>
      </CardContent>

      {/* Модальное окно с деталями */}
      <TaskDetailModal
        taskId={task.id}
        isOpen={showDetailModal}
        onClose={() => setShowDetailModal(false)}
        onStatusChange={onStatusChange}
      />
    </Card>
  )
}
