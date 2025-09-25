import { useParams } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { KanbanColumn } from '@/components/KanbanColumn'
import { TaskCard } from '@/components/TaskCard'
import { CreateTaskDialog } from '@/components/CreateTaskDialog'
import { Button } from '@/components/ui/button'
import { useToast } from '@/hooks/use-toast'
import { apiService, Task } from '@/lib/api'
import { useState } from 'react'
import { Plus, ArrowLeft } from 'lucide-react'
import { Link } from 'react-router-dom'

const columns = [
  { id: 'todo', title: 'К выполнению', color: 'bg-gray-100' },
  { id: 'in_progress', title: 'В работе', color: 'bg-blue-100' },
  { id: 'in_review', title: 'На проверке', color: 'bg-yellow-100' },
  { id: 'done', title: 'Готово', color: 'bg-green-100' },
]

export function Kanban() {
  const { projectId } = useParams<{ projectId: string }>()
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false)
  const [activeTask, setActiveTask] = useState<Task | null>(null)
  const { toast } = useToast()
  const queryClient = useQueryClient()

  const { data: project, isLoading: projectLoading } = useQuery({
    queryKey: ['project', projectId],
    queryFn: () => apiService.getProject(Number(projectId)).then(res => res.data),
    enabled: !!projectId,
  })

  const { data: tasks = [], isLoading: tasksLoading } = useQuery({
    queryKey: ['tasks', projectId],
    queryFn: () => apiService.getTasks().then(res => res.data),
    enabled: !!projectId,
  })

  const updateTaskMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<Task> }) => 
      apiService.updateTask(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks', projectId] })
      toast({
        title: "Задача обновлена",
        description: "Статус задачи изменен",
      })
    },
    onError: (error: any) => {
      toast({
        title: "Ошибка",
        description: error.response?.data?.detail || "Не удалось обновить задачу",
        variant: "destructive",
      })
    },
  })

  const createTaskMutation = useMutation({
    mutationFn: (data: Partial<Task>) => apiService.createTask(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks', projectId] })
      setIsCreateDialogOpen(false)
      toast({
        title: "Задача создана",
        description: "Задача успешно создана",
      })
    },
    onError: (error: any) => {
      toast({
        title: "Ошибка",
        description: error.response?.data?.detail || "Не удалось создать задачу",
        variant: "destructive",
      })
    },
  })

  const handleDragStart = (event: DragStartEvent) => {
    const task = tasks.find(t => t.id === event.active.id)
    setActiveTask(task || null)
  }

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event
    
    if (!over || active.id === over.id) {
      setActiveTask(null)
      return
    }

    const taskId = active.id as number
    const newStatus = over.id as string

    // Проверяем, что это валидный статус
    if (!columns.some(col => col.id === newStatus)) {
      setActiveTask(null)
      return
    }

    updateTaskMutation.mutate({
      id: taskId,
      data: { status: newStatus as any }
    })
    
    setActiveTask(null)
  }

  const handleCreateTask = (data: { title: string; description?: string; priority: string }) => {
    createTaskMutation.mutate({
      ...data,
      project_id: Number(projectId),
      status: 'todo',
      priority: data.priority as any
    })
  }

  // Группируем задачи по статусам
  const tasksByStatus = columns.reduce((acc, column) => {
    acc[column.id] = tasks.filter(task => task.status === column.id)
    return acc
  }, {} as Record<string, Task[]>)

  if (projectLoading || tasksLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    )
  }

  if (!project) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Проект не найден</h2>
        <Button asChild className="bg-blue-600 hover:bg-blue-700 transition-all duration-200 hover:scale-105 hover:shadow-lg hover:-translate-y-0.5">
          <Link to="/projects">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Вернуться к проектам
          </Link>
        </Button>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <Button variant="ghost" size="sm" asChild className="hover:bg-blue-50 hover:text-blue-700 transition-all duration-200 hover:scale-105 hover:shadow-lg hover:-translate-y-0.5">
              <Link to="/projects">
                <ArrowLeft className="h-4 w-4" />
              </Link>
            </Button>
            <div 
              className="w-4 h-4 rounded-full" 
              style={{ backgroundColor: project.color }}
            />
            <h1 className="text-3xl font-bold text-gray-900">{project.name}</h1>
          </div>
          {project.description && (
            <p className="text-gray-600">{project.description}</p>
          )}
        </div>
        <Button onClick={() => setIsCreateDialogOpen(true)} className="bg-blue-600 hover:bg-blue-700 transition-all duration-200 hover:scale-105 hover:shadow-lg hover:-translate-y-0.5">
          <Plus className="h-4 w-4 mr-2" />
          Новая задача
        </Button>
      </div>

      {/* Kanban Board */}
      <DndContext onDragStart={handleDragStart} onDragEnd={handleDragEnd}>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
          {columns.map((column) => (
            <KanbanColumn
              key={column.id}
              id={column.id}
              title={column.title}
              color={column.color}
              tasks={tasksByStatus[column.id] || []}
              onStatusChange={(taskId, newStatus) => {
                updateTaskMutation.mutate({
                  id: taskId,
                  data: { status: newStatus as any }
                })
              }}
            />
          ))}
        </div>

        <DragOverlay>
          {activeTask ? <TaskCard task={activeTask} isDragging /> : null}
        </DragOverlay>
      </DndContext>

      {/* Create Task Dialog */}
      <CreateTaskDialog
        open={isCreateDialogOpen}
        onOpenChange={setIsCreateDialogOpen}
        onSubmit={handleCreateTask}
        isLoading={createTaskMutation.isPending}
      />
    </div>
  )
}
