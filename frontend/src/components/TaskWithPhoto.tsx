import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Eye, Calendar, User, Flag } from 'lucide-react'

interface TaskWithPhoto {
  id: number
  title: string
  description: string
  status: string
  priority: string
  deadline?: string
  project_name?: string
  created_by?: number
  has_photo?: boolean
}

interface TaskWithPhotoProps {
  task: TaskWithPhoto
  onStatusChange?: (taskId: number, newStatus: string) => void
}

export function TaskWithPhoto({ task, onStatusChange }: TaskWithPhotoProps) {
  const [showPhoto, setShowPhoto] = useState(false)

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'urgent': return 'bg-red-500'
      case 'high': return 'bg-orange-500'
      case 'medium': return 'bg-yellow-500'
      case 'low': return 'bg-green-500'
      default: return 'bg-gray-500'
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

  const formatDeadline = (deadline?: string) => {
    if (!deadline) return null
    try {
      const date = new Date(deadline)
      return date.toLocaleDateString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    } catch {
      return deadline
    }
  }

  return (
    <Card className="w-full">
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <CardTitle className="text-lg font-semibold">{task.title}</CardTitle>
            <p className="text-sm text-gray-600 mt-1">{task.description}</p>
          </div>
          {task.has_photo && (
            <Dialog>
              <DialogTrigger asChild>
                <Button variant="outline" size="sm">
                  <Eye className="h-4 w-4 mr-2" />
                  Фото
                </Button>
              </DialogTrigger>
              <DialogContent className="max-w-2xl">
                <DialogHeader>
                  <DialogTitle>Фото задачи: {task.title}</DialogTitle>
                </DialogHeader>
                <div className="flex justify-center">
                  <img 
                    src={`https://projectmanager.chickenkiller.com/api/v1/photos/tasks/${task.id}/photo/`}
                    alt={`Фото для задачи ${task.title}`}
                    className="max-w-full max-h-96 object-contain rounded-lg"
                    onError={(e) => {
                      e.currentTarget.src = '/placeholder-image.png'
                      e.currentTarget.alt = 'Фото недоступно'
                    }}
                  />
                </div>
              </DialogContent>
            </Dialog>
          )}
        </div>
      </CardHeader>
      
      <CardContent className="pt-0">
        <div className="flex flex-wrap gap-2 mb-3">
          <Badge className={getStatusColor(task.status)}>
            {task.status === 'todo' ? 'Новая' : 
             task.status === 'in_progress' ? 'В работе' : 
             task.status === 'done' ? 'Выполнена' : task.status}
          </Badge>
          
          <Badge className={`${getPriorityColor(task.priority)} text-white`}>
            <Flag className="h-3 w-3 mr-1" />
            {task.priority === 'urgent' ? 'Срочно' :
             task.priority === 'high' ? 'Высокий' :
             task.priority === 'medium' ? 'Средний' :
             task.priority === 'low' ? 'Низкий' : task.priority}
          </Badge>
          
          {task.project_name && (
            <Badge variant="outline">
              📂 {task.project_name}
            </Badge>
          )}
        </div>

        <div className="flex items-center gap-4 text-sm text-gray-600">
          {task.deadline && (
            <div className="flex items-center gap-1">
              <Calendar className="h-4 w-4" />
              <span>До: {formatDeadline(task.deadline)}</span>
            </div>
          )}
          
          <div className="flex items-center gap-1">
            <User className="h-4 w-4" />
            <span>ID: {task.id}</span>
          </div>
        </div>

        {task.has_photo && (
          <div className="mt-3 p-2 bg-blue-50 rounded-lg">
            <p className="text-sm text-blue-700">
              📸 Эта задача содержит прикрепленное фото
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
