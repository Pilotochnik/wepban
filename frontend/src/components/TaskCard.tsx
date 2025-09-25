import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Task } from '@/lib/api'
import { cn } from '@/lib/utils'
import { format } from 'date-fns'
import { ru } from 'date-fns/locale'
import { Eye, ChevronRight, ChevronLeft, Clock, User, Flag } from 'lucide-react'
import { useState } from 'react'
import { TaskDetailModal } from './TaskDetailModal'

interface TaskCardProps {
  task: Task
  onStatusChange?: (taskId: number, newStatus: string) => void
}

const priorityColors = {
  low: 'bg-emerald-50 text-emerald-700 border-emerald-200',
  medium: 'bg-blue-50 text-blue-700 border-blue-200',
  high: 'bg-amber-50 text-amber-700 border-amber-200',
  urgent: 'bg-red-50 text-red-700 border-red-200',
}

const priorityLabels = {
  low: 'Низкий',
  medium: 'Средний',
  high: 'Высокий',
  urgent: 'Срочный',
}

const statusColors = {
  todo: 'bg-slate-50 text-slate-700',
  in_progress: 'bg-blue-50 text-blue-700',
  done: 'bg-emerald-50 text-emerald-700',
}

export function TaskCard({ task, onStatusChange }: TaskCardProps) {
  const [showDetailModal, setShowDetailModal] = useState(false)
  const [isChangingStatus, setIsChangingStatus] = useState(false)

  const handleStatusChange = async (newStatus: string) => {
    setIsChangingStatus(true)
    try {
      await onStatusChange?.(task.id, newStatus)
    } finally {
      setIsChangingStatus(false)
    }
  }

  return (
    <Card className="group hover:shadow-lg hover:shadow-blue-500/10 transition-all duration-300 border-0 bg-gradient-to-br from-white to-slate-50/50 backdrop-blur-sm rounded-xl hover:-translate-y-1 hover:scale-[1.02]">
      <CardContent className="p-5">
        <div className="space-y-4">
          {/* Заголовок и описание */}
          <div className="space-y-2">
            <div className="flex items-start justify-between">
              <h4 className="font-semibold text-sm text-gray-900 line-clamp-2 leading-tight group-hover:text-blue-600 transition-colors duration-300">
                {task.title}
              </h4>
              <div className={cn(
                "px-2 py-1 text-xs rounded-full font-medium border group-hover:scale-105 transition-transform duration-300",
                priorityColors[task.priority]
              )}>
                <Flag className="h-3 w-3 inline mr-1" />
                {priorityLabels[task.priority]}
              </div>
            </div>
            {task.description && (
              <p className="text-xs text-gray-600 line-clamp-3 leading-relaxed">
                {task.description}
              </p>
            )}
          </div>

          {/* Метаданные задачи */}
          <div className="flex flex-col gap-2">
            {task.deadline && (
              <div className="flex items-center gap-2 text-xs">
                <Clock className="h-3 w-3 text-gray-400" />
                <span className={cn(
                  "px-2 py-1 rounded-full font-medium group-hover:scale-105 transition-transform duration-300",
                  new Date(task.deadline) < new Date() 
                    ? "bg-red-50 text-red-700 border border-red-200" 
                    : "bg-slate-50 text-slate-600 border border-slate-200"
                )}>
                  {format(new Date(task.deadline), 'dd.MM.yyyy', { locale: ru })}
                </span>
              </div>
            )}
            
            <div className="flex items-center justify-between text-xs text-gray-500">
              <span className="flex items-center gap-1">
                <Clock className="h-3 w-3" />
                Создано {format(new Date(task.created_at), 'dd.MM', { locale: ru })}
              </span>
              {task.assigned_to && (
                <span className="flex items-center gap-1 bg-blue-50 text-blue-700 px-2 py-1 rounded-full border border-blue-200 group-hover:scale-105 transition-transform duration-300">
                  <User className="h-3 w-3" />
                  Назначено
                </span>
              )}
            </div>
          </div>

          {/* Кнопки действий */}
          <div className="space-y-3">
            {/* Кнопки смены статуса */}
            <div className="flex gap-2">
              {task.status === 'todo' && (
                <Button
                  variant="outline"
                  size="sm"
                  className="flex-1 text-xs bg-blue-50 hover:bg-blue-100 border-blue-200 text-blue-700 transition-all duration-200 hover:scale-105 hover:shadow-lg hover:-translate-y-0.5"
                  onClick={(e) => {
                    e.stopPropagation()
                    handleStatusChange('in_progress')
                  }}
                  disabled={isChangingStatus}
                >
                  <ChevronRight className="h-3 w-3 mr-1" />
                  В работу
                </Button>
              )}
              {task.status === 'in_progress' && (
                <>
                  <Button
                    variant="outline"
                    size="sm"
                    className="flex-1 text-xs bg-slate-50 hover:bg-slate-100 border-slate-200 text-slate-700 transition-all duration-200 hover:scale-105 hover:shadow-lg hover:-translate-y-0.5"
                    onClick={(e) => {
                      e.stopPropagation()
                      handleStatusChange('todo')
                    }}
                    disabled={isChangingStatus}
                  >
                    <ChevronLeft className="h-3 w-3 mr-1" />
                    Назад
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    className="flex-1 text-xs bg-emerald-50 hover:bg-emerald-100 border-emerald-200 text-emerald-700 transition-all duration-200 hover:scale-105 hover:shadow-lg hover:-translate-y-0.5"
                    onClick={(e) => {
                      e.stopPropagation()
                      handleStatusChange('done')
                    }}
                    disabled={isChangingStatus}
                  >
                    <ChevronRight className="h-3 w-3 mr-1" />
                    Готово
                  </Button>
                </>
              )}
              {task.status === 'done' && (
                <Button
                  variant="outline"
                  size="sm"
                  className="flex-1 text-xs bg-blue-50 hover:bg-blue-100 border-blue-200 text-blue-700 transition-all duration-200 hover:scale-105 hover:shadow-lg hover:-translate-y-0.5"
                  onClick={(e) => {
                    e.stopPropagation()
                    handleStatusChange('in_progress')
                  }}
                  disabled={isChangingStatus}
                >
                  <ChevronLeft className="h-3 w-3 mr-1" />
                  В работу
                </Button>
              )}
            </div>
            
            {/* Кнопка подробнее */}
            <Button 
              variant="outline" 
              size="sm" 
              className="w-full bg-white hover:bg-slate-50 border-slate-200 text-slate-700 transition-all duration-200 hover:shadow-sm hover:scale-105 hover:-translate-y-0.5"
              onClick={(e) => {
                e.stopPropagation()
                setShowDetailModal(true)
              }}
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
