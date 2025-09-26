import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { useToast } from '@/hooks/use-toast'
import { apiService, Project } from '@/lib/api'
import { useAuth } from '@/contexts/AuthContext'
import { 
  Plus, 
  FolderKanban, 
  Edit, 
  Trash2,
  MoreVertical
} from 'lucide-react'
import { Link } from 'react-router-dom'
import { CreateProjectDialog } from '@/components/CreateProjectDialog'
import { EditProjectDialog } from '@/components/EditProjectDialog'

export function Projects() {
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false)
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false)
  const [editingProject, setEditingProject] = useState<Project | null>(null)
  const { toast } = useToast()
  const queryClient = useQueryClient()
  const { user } = useAuth()

  const { data: projects = [], isLoading } = useQuery({
    queryKey: ['projects'],
    queryFn: () => apiService.getProjects().then(res => res.data),
  })

  const createProjectMutation = useMutation({
    mutationFn: (data: Partial<Project>) => apiService.createProject(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] })
      setIsCreateDialogOpen(false)
      toast({
        title: "Проект создан",
        description: "Проект успешно создан",
      })
    },
    onError: (error: any) => {
      toast({
        title: "Ошибка",
        description: error.response?.data?.detail || "Не удалось создать проект",
        variant: "destructive",
      })
    },
  })

  const updateProjectMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<Project> }) => apiService.updateProject(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] })
      setIsEditDialogOpen(false)
      setEditingProject(null)
      toast({
        title: "Проект обновлен",
        description: "Проект успешно обновлен",
      })
    },
    onError: (error: any) => {
      toast({
        title: "Ошибка",
        description: error.response?.data?.detail || "Не удалось обновить проект",
        variant: "destructive",
      })
    },
  })

  const deleteProjectMutation = useMutation({
    mutationFn: (id: number) => apiService.deleteProject(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] })
      toast({
        title: "Проект удален",
        description: "Проект успешно удален",
      })
    },
    onError: (error: any) => {
      toast({
        title: "Ошибка",
        description: error.response?.data?.detail || "Не удалось удалить проект",
        variant: "destructive",
      })
    },
  })

  const handleCreateProject = (data: { name: string; description?: string; color: string }) => {
    createProjectMutation.mutate(data)
  }

  const handleDeleteProject = (id: number) => {
    if (window.confirm('Вы уверены, что хотите удалить этот проект?')) {
      deleteProjectMutation.mutate(id)
    }
  }

  const handleEditProject = (project: Project) => {
    setEditingProject(project)
    setIsEditDialogOpen(true)
  }

  const handleUpdateProject = (data: { name: string; description?: string; color: string }) => {
    if (editingProject) {
      updateProjectMutation.mutate({ id: editingProject.id, data })
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Проекты</h1>
          <p className="text-gray-600 mt-2">
            {user?.role === 'creator' 
              ? "Управляйте своими проектами и задачами"
              : "Ваши назначенные проекты"
            }
          </p>
        </div>
        {user?.role === 'creator' && (
          <Button onClick={() => setIsCreateDialogOpen(true)} className="bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white shadow-lg transition-all duration-200 hover:scale-105 hover:shadow-xl hover:-translate-y-0.5">
            <Plus className="h-4 w-4 mr-2" />
            Новый проект
          </Button>
        )}
      </div>

      {projects.length === 0 ? (
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-12">
            <FolderKanban className="h-16 w-16 text-gray-400 mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">Нет проектов</h3>
            {user?.role === 'creator' ? (
              <>
                <p className="text-gray-500 text-center mb-6">
                  Создайте свой первый проект, чтобы начать управлять задачами
                </p>
                <Button onClick={() => setIsCreateDialogOpen(true)} className="bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white shadow-lg transition-all duration-200 hover:scale-105 hover:shadow-xl hover:-translate-y-0.5">
                  <Plus className="h-4 w-4 mr-2" />
                  Создать проект
                </Button>
              </>
            ) : (
              <p className="text-gray-500 text-center mb-6">
                Вам не назначены проекты. Обратитесь к администратору для получения доступа.
              </p>
            )}
          </CardContent>
        </Card>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
          {projects.map((project) => (
            <Card key={project.id} className="group hover:shadow-lg hover:shadow-blue-500/20 transition-all duration-300 hover:-translate-y-1 hover:scale-[1.02] border-0 bg-gradient-to-br from-white via-blue-50/30 to-indigo-50/50 backdrop-blur-sm rounded-xl">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div className="flex items-center min-w-0 flex-1">
                    <div 
                      className="w-4 h-4 rounded-full mr-3 flex-shrink-0 group-hover:scale-110 transition-transform duration-300" 
                      style={{ backgroundColor: project.color }}
                    />
                    <CardTitle className="text-lg truncate group-hover:text-blue-600 transition-colors duration-300">{project.name}</CardTitle>
                  </div>
                  <Button variant="ghost" size="sm" className="flex-shrink-0 group-hover:bg-blue-50 group-hover:text-blue-600 transition-all duration-300">
                    <MoreVertical className="h-4 w-4" />
                  </Button>
                </div>
                {project.description && (
                  <CardDescription className="mt-2">
                    {project.description}
                  </CardDescription>
                )}
              </CardHeader>
              <CardContent>
                <div className="flex gap-2 mb-4">
                  <Button size="sm" asChild className="flex-1 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white border-0 shadow-md transition-all duration-200 hover:scale-105 hover:shadow-lg hover:-translate-y-0.5">
                    <Link to={`/kanban/${project.id}`}>
                      <FolderKanban className="h-4 w-4 mr-2" />
                      Открыть
                    </Link>
                  </Button>
                </div>
                {user?.role === 'creator' && (
                  <div className="flex gap-2">
                    <Button 
                      variant="outline" 
                      size="sm" 
                      className="flex-1 bg-gradient-to-r from-emerald-50 to-emerald-100 hover:from-emerald-100 hover:to-emerald-200 text-emerald-700 border-emerald-300 transition-all duration-200 hover:scale-105 hover:shadow-lg hover:-translate-y-0.5"
                      onClick={() => handleEditProject(project)}
                    >
                      <Edit className="h-4 w-4 sm:mr-2" />
                      <span className="hidden sm:inline">Изменить</span>
                    </Button>
                    <Button 
                      variant="outline" 
                      size="sm" 
                      className="flex-1 bg-gradient-to-r from-red-50 to-red-100 hover:from-red-100 hover:to-red-200 text-red-700 border-red-300 transition-all duration-200 hover:scale-105 hover:shadow-lg hover:-translate-y-0.5"
                      onClick={() => handleDeleteProject(project.id)}
                    >
                      <Trash2 className="h-4 w-4 sm:mr-2" />
                      <span className="hidden sm:inline">Удалить</span>
                    </Button>
                  </div>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Create Project Dialog */}
      <CreateProjectDialog
        open={isCreateDialogOpen}
        onOpenChange={setIsCreateDialogOpen}
        onSubmit={handleCreateProject}
        isLoading={createProjectMutation.isPending}
      />

      {/* Edit Project Dialog */}
      <EditProjectDialog
        open={isEditDialogOpen}
        onOpenChange={setIsEditDialogOpen}
        onSubmit={handleUpdateProject}
        project={editingProject}
        isLoading={updateProjectMutation.isPending}
      />
    </div>
  )
}
