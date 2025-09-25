import { useQuery } from '@tanstack/react-query'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Link } from 'react-router-dom'
import { apiService } from '@/lib/api'
import { useAuth } from '@/contexts/AuthContext'
import { 
  FolderKanban, 
  CheckSquare, 
  Clock, 
  Plus,
  TrendingUp,
  Target,
  Activity,
  CheckCircle
} from 'lucide-react'

export function Dashboard() {
  const { user } = useAuth()
  
  const { data: projects = [], isLoading: projectsLoading } = useQuery({
    queryKey: ['projects'],
    queryFn: () => apiService.getProjects().then(res => res.data),
  })

  const { data: tasks = [], isLoading: tasksLoading } = useQuery({
    queryKey: ['tasks'],
    queryFn: async () => {
      const allTasks = []
      for (const project of projects) {
        try {
          const response = await apiService.getTasks()
          allTasks.push(...response.data)
        } catch (error) {
          console.error(`Ошибка загрузки задач для проекта ${project.id}:`, error)
        }
      }
      return allTasks
    },
    enabled: projects.length > 0,
  })

  const stats = {
    totalProjects: projects.length,
    totalTasks: tasks.length,
    completedTasks: tasks.filter(task => task.status === 'done').length,
    inProgressTasks: tasks.filter(task => task.status === 'in_progress').length,
  }

  const recentTasks = tasks
    .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
    .slice(0, 5)

  if (projectsLoading || tasksLoading) {
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
          <h1 className="text-3xl font-bold text-gray-900">
            Добро пожаловать, {user?.first_name}!
          </h1>
          <p className="text-gray-600 mt-2">
            Управляйте своими проектами и задачами с помощью AI-ассистента
          </p>
        </div>
        <div className="flex gap-3">
          <Button asChild className="bg-blue-600 hover:bg-blue-700 transition-all duration-200 hover:scale-105 hover:shadow-lg hover:-translate-y-0.5">
            <Link to="/projects">
              <Plus className="h-4 w-4 mr-2" />
              Новый проект
            </Link>
          </Button>
        </div>
      </div>

             {/* Stats */}
             <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-6">
               <Card className="bg-gradient-to-br from-blue-50 to-blue-100/50 border-blue-200/50 hover:shadow-blue-500/10 transition-all duration-300 hover:scale-105">
                 <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                   <CardTitle className="text-sm font-medium text-blue-700">Проекты</CardTitle>
                   <FolderKanban className="h-4 w-4 text-blue-500" />
                 </CardHeader>
                 <CardContent>
                   <div className="text-2xl font-bold text-blue-900">{stats.totalProjects}</div>
                   <p className="text-xs text-blue-600">
                     Всего проектов
                   </p>
                 </CardContent>
               </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Задачи</CardTitle>
            <CheckSquare className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.totalTasks}</div>
            <p className="text-xs text-muted-foreground">
              Всего задач
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">В работе</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.inProgressTasks}</div>
            <p className="text-xs text-muted-foreground">
              Активных задач
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Завершено</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.completedTasks}</div>
            <p className="text-xs text-muted-foreground">
              Выполненных задач
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Projects */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Мои проекты</CardTitle>
            <CardDescription>
              Управляйте своими проектами
            </CardDescription>
          </CardHeader>
          <CardContent>
            {projects.length === 0 ? (
              <div className="text-center py-6">
                <FolderKanban className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-500 mb-4">У вас пока нет проектов</p>
                <Button asChild className="bg-blue-600 hover:bg-blue-700 transition-all duration-200 hover:scale-105 hover:shadow-lg hover:-translate-y-0.5">
                  <Link to="/projects">Создать первый проект</Link>
                </Button>
              </div>
            ) : (
              <div className="space-y-3">
                {projects.slice(0, 5).map((project) => (
                  <div key={project.id} className="flex items-center justify-between p-3 border rounded-lg">
                    <div className="flex items-center min-w-0 flex-1">
                      <div 
                        className="w-3 h-3 rounded-full mr-3 flex-shrink-0" 
                        style={{ backgroundColor: project.color }}
                      />
                      <div className="min-w-0 flex-1">
                        <p className="font-medium truncate">{project.name}</p>
                        {project.description && (
                          <p className="text-sm text-gray-500 truncate">{project.description}</p>
                        )}
                      </div>
                    </div>
                    <Button variant="outline" size="sm" className="ml-2 flex-shrink-0 hover:bg-blue-50 hover:border-blue-300 transition-all duration-200 hover:scale-105 hover:shadow-lg hover:-translate-y-0.5" asChild>
                      <Link to={`/kanban/${project.id}`}>
                        Открыть
                      </Link>
                    </Button>
                  </div>
                ))}
                {projects.length > 5 && (
                  <Button variant="ghost" className="w-full hover:bg-blue-50 hover:text-blue-700 transition-all duration-200 hover:scale-105 hover:shadow-lg hover:-translate-y-0.5" asChild>
                    <Link to="/projects">Показать все проекты</Link>
                  </Button>
                )}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Recent Tasks */}
        <Card>
          <CardHeader>
            <CardTitle>Недавние задачи</CardTitle>
            <CardDescription>
              Последние созданные задачи
            </CardDescription>
          </CardHeader>
          <CardContent>
            {recentTasks.length === 0 ? (
              <div className="text-center py-6">
                <CheckSquare className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-500">Пока нет задач</p>
              </div>
            ) : (
              <div className="space-y-3">
                {recentTasks.map((task) => (
                  <div key={task.id} className="p-3 border rounded-lg">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <p className="font-medium text-sm">{task.title}</p>
                        <p className="text-xs text-gray-500 mt-1">
                          {task.project?.name || 'Без проекта'}
                        </p>
                      </div>
                      <span className={`
                        px-2 py-1 text-xs rounded-full
                        ${task.status === 'todo' ? 'bg-gray-100 text-gray-800' : ''}
                        ${task.status === 'in_progress' ? 'bg-blue-100 text-blue-800' : ''}
                        ${task.status === 'in_review' ? 'bg-yellow-100 text-yellow-800' : ''}
                        ${task.status === 'done' ? 'bg-green-100 text-green-800' : ''}
                      `}>
                        {task.status === 'todo' && 'К выполнению'}
                        {task.status === 'in_progress' && 'В работе'}
                        {task.status === 'in_review' && 'На проверке'}
                        {task.status === 'done' && 'Готово'}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
