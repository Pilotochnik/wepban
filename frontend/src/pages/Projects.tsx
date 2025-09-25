import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { useToast } from '@/hooks/use-toast'
import { apiService, Project } from '@/lib/api'
import { 
  Plus, 
  FolderKanban, 
  Edit, 
  Trash2,
  MoreVertical,
  Wrench
} from 'lucide-react'
import { Link } from 'react-router-dom'
import { CreateProjectDialog } from '@/components/CreateProjectDialog'
import { EquipmentTab } from '@/components/EquipmentTab'

export function Projects() {
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false)
  const { toast } = useToast()
  const queryClient = useQueryClient()

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
            Управляйте своими проектами и задачами
          </p>
        </div>
        <Button onClick={() => setIsCreateDialogOpen(true)} className="bg-blue-600 hover:bg-blue-700 transition-all duration-200 hover:scale-105 hover:shadow-lg hover:-translate-y-0.5">
          <Plus className="h-4 w-4 mr-2" />
          Новый проект
        </Button>
      </div>

      {/* Tabs */}
      <Tabs defaultValue="projects" className="space-y-6">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="projects" className="flex items-center gap-2">
            <FolderKanban className="h-4 w-4" />
            Проекты
          </TabsTrigger>
          <TabsTrigger value="equipment" className="flex items-center gap-2">
            <Wrench className="h-4 w-4" />
            Техника
          </TabsTrigger>
        </TabsList>

        <TabsContent value="projects" className="space-y-6">

      {/* Projects Grid */}
      {projects.length === 0 ? (
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-12">
            <FolderKanban className="h-16 w-16 text-gray-400 mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">Нет проектов</h3>
            <p className="text-gray-500 text-center mb-6">
              Создайте свой первый проект, чтобы начать управлять задачами
            </p>
            <Button onClick={() => setIsCreateDialogOpen(true)} className="bg-blue-600 hover:bg-blue-700 transition-all duration-200 hover:scale-105 hover:shadow-lg hover:-translate-y-0.5">
              <Plus className="h-4 w-4 mr-2" />
              Создать проект
            </Button>
          </CardContent>
        </Card>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
          {projects.map((project) => (
            <Card key={project.id} className="group hover:shadow-lg hover:shadow-blue-500/10 transition-all duration-300 hover:-translate-y-1 hover:scale-[1.02] border-0 bg-gradient-to-br from-white to-slate-50/50 backdrop-blur-sm rounded-xl">
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
                  <Button size="sm" asChild className="flex-1 bg-blue-50 hover:bg-blue-100 text-blue-700 border-blue-200 transition-all duration-200 hover:scale-105 hover:shadow-lg hover:-translate-y-0.5">
                    <Link to={`/kanban/${project.id}`}>
                      <FolderKanban className="h-4 w-4 mr-2" />
                      Открыть
                    </Link>
                  </Button>
                </div>
                <div className="flex gap-2">
                  <Button variant="outline" size="sm" className="flex-1 hover:bg-slate-50 hover:border-slate-300 transition-all duration-200 hover:scale-105 hover:shadow-lg hover:-translate-y-0.5">
                    <Edit className="h-4 w-4 sm:mr-2" />
                    <span className="hidden sm:inline">Изменить</span>
                  </Button>
                  <Button 
                    variant="outline" 
                    size="sm" 
                    className="flex-1 text-red-600 hover:text-red-700 hover:bg-red-50 hover:border-red-300 transition-all duration-200 hover:scale-105 hover:shadow-lg hover:-translate-y-0.5"
                    onClick={() => handleDeleteProject(project.id)}
                  >
                    <Trash2 className="h-4 w-4 sm:mr-2" />
                    <span className="hidden sm:inline">Удалить</span>
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

        </TabsContent>

        <TabsContent value="equipment" className="space-y-6">
          <EquipmentTab projectId={projects[0]?.id || 0} />
        </TabsContent>
      </Tabs>

      {/* Create Project Dialog */}
      <CreateProjectDialog
        open={isCreateDialogOpen}
        onOpenChange={setIsCreateDialogOpen}
        onSubmit={handleCreateProject}
        isLoading={createProjectMutation.isPending}
      />
    </div>
  )
}
