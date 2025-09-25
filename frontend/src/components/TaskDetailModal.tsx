import { useState, useEffect } from 'react'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent } from '@/components/ui/card'
import { Calendar, User, Flag, Clock, Camera, X } from 'lucide-react'
import { apiService } from '@/lib/api'

interface TaskDetail {
  id: number
  title: string
  description?: string
  status: string
  priority: string
  deadline?: string
  project_id?: number
  project_name?: string
  created_by?: number
  created_at?: string
  assigned_to?: number
}

interface TaskDetailModalProps {
  taskId: number | null
  isOpen: boolean
  onClose: () => void
  onStatusChange?: (taskId: number, newStatus: string) => void
}

export function TaskDetailModal({ taskId, isOpen, onClose, onStatusChange }: TaskDetailModalProps) {
  const [task, setTask] = useState<TaskDetail | null>(null)
  const [loading, setLoading] = useState(false)
  const [photoExists, setPhotoExists] = useState(false)
  const [showPhoto, setShowPhoto] = useState(false)

  useEffect(() => {
    if (isOpen && taskId) {
      fetchTaskDetails()
      checkPhoto()
    }
  }, [isOpen, taskId])

  const fetchTaskDetails = async () => {
    if (!taskId) return
    
    setLoading(true)
    try {
      // Получаем детали задачи
      const response = await apiService.getTask(taskId)
      setTask(response.data)
    } catch (error) {
      console.error('Ошибка загрузки задачи:', error)
    } finally {
      setLoading(false)
    }
  }

  const checkPhoto = async () => {
    if (!taskId) return
    
    try {
      // Проверяем наличие фото
      await apiService.getTaskPhoto(taskId)
      setPhotoExists(true)
    } catch (error) {
      setPhotoExists(false)
    }
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'urgent': return 'bg-red-500 text-white'
      case 'high': return 'bg-orange-500 text-white'
      case 'medium': return 'bg-yellow-500 text-white'
      case 'low': return 'bg-green-500 text-white'
      default: return 'bg-gray-500 text-white'
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'todo': return 'bg-blue-100 text-blue-800'
      case 'in_progress': return 'bg-yellow-100 text-yellow-800'
      case 'done': return 'bg-green-100 text-green-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const formatDate = (dateString?: string) => {
    if (!dateString) return null
    try {
      const date = new Date(dateString)
      return date.toLocaleDateString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    } catch {
      return dateString
    }
  }

  const handleStatusChange = async (newStatus: string) => {
    if (!task || !onStatusChange) return
    
    try {
      await apiService.updateTaskStatus(task.id, newStatus)
      onStatusChange(task.id, newStatus)
      setTask({ ...task, status: newStatus })
    } catch (error) {
      console.error('Ошибка обновления статуса:', error)
    }
  }

  if (loading) {
    return (
      <Dialog open={isOpen} onOpenChange={onClose}>
        <DialogContent className="max-w-md mx-auto">
          <div className="flex items-center justify-center p-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
        </DialogContent>
      </Dialog>
    )
  }

  if (!task) {
    return (
      <Dialog open={isOpen} onOpenChange={onClose}>
        <DialogContent className="max-w-md mx-auto">
          <div className="text-center p-8">
            <p className="text-gray-500">Задача не найдена</p>
          </div>
        </DialogContent>
      </Dialog>
    )
  }

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-md mx-auto max-h-[90vh] overflow-y-auto">
        <DialogHeader className="pb-4">
          <DialogTitle className="text-lg font-semibold leading-tight">
            {task.title}
          </DialogTitle>
        </DialogHeader>

        <div className="space-y-4">
          {/* Статус и приоритет */}
          <div className="flex flex-wrap gap-2">
            <Badge className={getStatusColor(task.status)}>
              {task.status === 'todo' ? 'Новая' : 
               task.status === 'in_progress' ? 'В работе' : 
               task.status === 'done' ? 'Выполнена' : task.status}
            </Badge>
            
            <Badge className={getPriorityColor(task.priority)}>
              <Flag className="h-3 w-3 mr-1" />
              {task.priority === 'urgent' ? 'Срочно' :
               task.priority === 'high' ? 'Высокий' :
               task.priority === 'medium' ? 'Средний' :
               task.priority === 'low' ? 'Низкий' : task.priority}
            </Badge>
          </div>

          {/* Описание */}
          <Card>
            <CardContent className="p-4">
              <h4 className="font-medium mb-2">Описание</h4>
              <p className="text-sm text-gray-700 whitespace-pre-wrap">
                {task.description}
              </p>
            </CardContent>
          </Card>

          {/* Детали задачи */}
          <div className="space-y-2">
            {task.project_name && (
              <div className="flex items-center gap-2 text-sm">
                <span className="font-medium">Проект:</span>
                <Badge variant="outline">📂 {task.project_name}</Badge>
              </div>
            )}

            {task.deadline && (
              <div className="flex items-center gap-2 text-sm">
                <Calendar className="h-4 w-4 text-gray-500" />
                <span className="font-medium">Дедлайн:</span>
                <span>{formatDate(task.deadline)}</span>
              </div>
            )}

            <div className="flex items-center gap-2 text-sm">
              <User className="h-4 w-4 text-gray-500" />
              <span className="font-medium">ID задачи:</span>
              <span>{task.id}</span>
            </div>

            {task.created_at && (
              <div className="flex items-center gap-2 text-sm">
                <Clock className="h-4 w-4 text-gray-500" />
                <span className="font-medium">Создана:</span>
                <span>{formatDate(task.created_at)}</span>
              </div>
            )}
          </div>

          {/* Фото */}
          {photoExists && (
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center justify-between mb-3">
                  <h4 className="font-medium flex items-center gap-2">
                    <Camera className="h-4 w-4" />
                    Прикрепленное фото
                  </h4>
                  <Button 
                    variant="outline" 
                    size="sm"
                    onClick={() => setShowPhoto(!showPhoto)}
                  >
                    {showPhoto ? 'Скрыть' : 'Показать'}
                  </Button>
                </div>
                
                {showPhoto && (
                  <div className="relative">
                    <img 
                      src={`https://projectmanager.chickenkiller.com/api/v1/photos/tasks/${task.id}/photo/`}
                      alt={`Фото для задачи ${task.title}`}
                      className="w-full rounded-lg border"
                      onError={(e) => {
                        e.currentTarget.src = '/placeholder-image.png'
                        e.currentTarget.alt = 'Фото недоступно'
                      }}
                    />
                  </div>
                )}
              </CardContent>
            </Card>
          )}

          {/* Кнопки управления статусом */}
          <div className="flex flex-wrap gap-2 pt-4">
            {task.status !== 'todo' && (
              <Button 
                variant="outline" 
                size="sm"
                onClick={() => handleStatusChange('todo')}
              >
                В новые
              </Button>
            )}
            {task.status !== 'in_progress' && (
              <Button 
                variant="outline" 
                size="sm"
                onClick={() => handleStatusChange('in_progress')}
              >
                В работу
              </Button>
            )}
            {task.status !== 'done' && (
              <Button 
                variant="outline" 
                size="sm"
                onClick={() => handleStatusChange('done')}
              >
                Выполнено
              </Button>
            )}
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}
