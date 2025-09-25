import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Textarea } from '@/components/ui/textarea'
import { useToast } from '@/hooks/use-toast'
import { apiService, Project } from '@/lib/api'
import { useAuth } from '@/contexts/AuthContext'
import { 
  Users, 
  UserPlus, 
  CheckCircle, 
  XCircle, 
  Clock, 
  AlertCircle,
  Shield,
  Eye,
  UserCheck,
} from 'lucide-react'

interface User {
  id: number
  telegram_id: number
  username?: string
  first_name?: string
  last_name?: string
  role: 'creator' | 'foreman' | 'worker' | 'viewer'
  is_active: boolean
  created_at: string
}

interface ApprovalRequest {
  id: number
  requester: User
  approver: User
  action_type: string
  entity_type: string
  entity_id: number
  action_data: string
  status: 'pending' | 'approved' | 'rejected'
  created_at: string
  reviewed_at?: string
  review_comment?: string
}

export function AdminPanel() {
  const { user } = useAuth()
  const { toast } = useToast()
  const [users, setUsers] = useState<User[]>([])
  const [projects, setProjects] = useState<Project[]>([])
  const [pendingApprovals, setPendingApprovals] = useState<ApprovalRequest[]>([])
  const [showAddUserDialog, setShowAddUserDialog] = useState(false)
  const [selectedApproval, setSelectedApproval] = useState<ApprovalRequest | null>(null)
  const [loading, setLoading] = useState(false)

  // Проверяем права доступа
  if (user?.role !== 'creator') {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Card className="w-full max-w-md">
          <CardContent className="pt-6">
            <div className="text-center">
              <Shield className="h-12 w-12 mx-auto text-red-500 mb-4" />
              <h2 className="text-xl font-semibold mb-2">Доступ запрещен</h2>
              <p className="text-gray-600">
                Только создатель проекта может получить доступ к админ панели
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    setLoading(true)
    try {
      await Promise.all([
        loadUsers(),
        loadProjects(),
        loadPendingApprovals()
      ])
    } catch (error) {
      toast({
        title: "Ошибка загрузки данных",
        description: "Не удалось загрузить данные админ панели",
        variant: "destructive"
      })
    } finally {
      setLoading(false)
    }
  }

  const loadUsers = async () => {
    try {
      const response = await apiService.getAdminUsers()
      setUsers(response.data)
    } catch (error) {
      console.error('Ошибка загрузки пользователей:', error)
    }
  }

  const loadProjects = async () => {
    try {
      const response = await apiService.getProjects()
      setProjects(response.data)
    } catch (error) {
      console.error('Ошибка загрузки проектов:', error)
    }
  }

  const loadPendingApprovals = async () => {
    try {
      const response = await apiService.getPendingApprovals()
      setPendingApprovals(response.data)
    } catch (error) {
      console.error('Ошибка загрузки одобрений:', error)
    }
  }

  const handleApproval = async (approvalId: number, status: 'approved' | 'rejected', comment?: string) => {
    try {
      await apiService.reviewApproval(approvalId, status, comment)
      toast({
        title: status === 'approved' ? 'Одобрено' : 'Отклонено',
        description: `Действие ${status === 'approved' ? 'одобрено' : 'отклонено'}`,
      })
      loadPendingApprovals()
      setSelectedApproval(null)
    } catch (error) {
      toast({
        title: "Ошибка",
        description: "Не удалось обработать запрос",
        variant: "destructive"
      })
    }
  }

  const getRoleColor = (role: string) => {
    switch (role) {
      case 'creator': return 'bg-purple-100 text-purple-800'
      case 'foreman': return 'bg-blue-100 text-blue-800'
      case 'worker': return 'bg-green-100 text-green-800'
      case 'viewer': return 'bg-gray-100 text-gray-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getRoleLabel = (role: string) => {
    switch (role) {
      case 'creator': return 'Создатель'
      case 'foreman': return 'Прораб'
      case 'worker': return 'Рабочий'
      case 'viewer': return 'Наблюдатель'
      default: return role
    }
  }

  const getActionTypeLabel = (actionType: string) => {
    switch (actionType) {
      case 'create_task': return 'Создание задачи'
      case 'update_task': return 'Изменение задачи'
      case 'delete_task': return 'Удаление задачи'
      case 'create_project': return 'Создание проекта'
      case 'update_project': return 'Изменение проекта'
      case 'delete_project': return 'Удаление проекта'
      case 'add_user_to_project': return 'Добавление пользователя'
      case 'remove_user_from_project': return 'Удаление пользователя'
      default: return actionType
    }
  }

  return (
    <div className="space-y-4 sm:space-y-6 p-4 sm:p-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">Админ панель</h1>
        <Button onClick={loadData} disabled={loading} className="w-full sm:w-auto bg-blue-50 hover:bg-blue-100 text-blue-700 border-blue-200 transition-all duration-200 hover:scale-105 hover:shadow-lg hover:-translate-y-0.5">
          {loading ? 'Загрузка...' : 'Обновить'}
        </Button>
      </div>

      {/* Статистика */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
        <Card className="group hover:shadow-lg hover:shadow-blue-500/10 transition-all duration-300 hover:-translate-y-1 hover:scale-[1.02] border-0 bg-gradient-to-br from-white to-slate-50/50 backdrop-blur-sm rounded-xl">
          <CardContent className="pt-6">
            <div className="flex items-center">
              <Users className="h-6 w-6 sm:h-8 sm:w-8 text-blue-600 flex-shrink-0 group-hover:scale-110 transition-transform duration-300" />
              <div className="ml-2 sm:ml-4 min-w-0">
                <p className="text-xs sm:text-sm font-medium text-gray-600 truncate group-hover:text-blue-600 transition-colors duration-300">Всего пользователей</p>
                <p className="text-xl sm:text-2xl font-bold group-hover:text-blue-700 transition-colors duration-300">{users.length}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="group hover:shadow-lg hover:shadow-yellow-500/10 transition-all duration-300 hover:-translate-y-1 hover:scale-[1.02] border-0 bg-gradient-to-br from-white to-slate-50/50 backdrop-blur-sm rounded-xl">
          <CardContent className="pt-6">
            <div className="flex items-center">
              <Clock className="h-6 w-6 sm:h-8 sm:w-8 text-yellow-600 flex-shrink-0 group-hover:scale-110 transition-transform duration-300" />
              <div className="ml-2 sm:ml-4 min-w-0">
                <p className="text-xs sm:text-sm font-medium text-gray-600 truncate group-hover:text-yellow-600 transition-colors duration-300">Ожидают одобрения</p>
                <p className="text-xl sm:text-2xl font-bold group-hover:text-yellow-700 transition-colors duration-300">{pendingApprovals.length}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="group hover:shadow-lg hover:shadow-green-500/10 transition-all duration-300 hover:-translate-y-1 hover:scale-[1.02] border-0 bg-gradient-to-br from-white to-slate-50/50 backdrop-blur-sm rounded-xl">
          <CardContent className="pt-6">
            <div className="flex items-center">
              <UserCheck className="h-6 w-6 sm:h-8 sm:w-8 text-green-600 flex-shrink-0 group-hover:scale-110 transition-transform duration-300" />
              <div className="ml-2 sm:ml-4 min-w-0">
                <p className="text-xs sm:text-sm font-medium text-gray-600 truncate group-hover:text-green-600 transition-colors duration-300">Активные прорабы</p>
                <p className="text-xl sm:text-2xl font-bold group-hover:text-green-700 transition-colors duration-300">
                  {users.filter(u => u.role === 'foreman' && u.is_active).length}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="group hover:shadow-lg hover:shadow-red-500/10 transition-all duration-300 hover:-translate-y-1 hover:scale-[1.02] border-0 bg-gradient-to-br from-white to-slate-50/50 backdrop-blur-sm rounded-xl">
          <CardContent className="pt-6">
            <div className="flex items-center">
              <AlertCircle className="h-6 w-6 sm:h-8 sm:w-8 text-red-600 flex-shrink-0 group-hover:scale-110 transition-transform duration-300" />
              <div className="ml-2 sm:ml-4 min-w-0">
                <p className="text-xs sm:text-sm font-medium text-gray-600 truncate group-hover:text-red-600 transition-colors duration-300">Заблокированные</p>
                <p className="text-xl sm:text-2xl font-bold group-hover:text-red-700 transition-colors duration-300">
                  {users.filter(u => !u.is_active).length}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Пользователи */}
      <Card>
        <CardHeader>
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <CardTitle className="flex items-center gap-2">
              <Users className="h-5 w-5" />
              Пользователи системы
            </CardTitle>
            <Dialog open={showAddUserDialog} onOpenChange={setShowAddUserDialog}>
              <DialogTrigger asChild>
                <Button className="w-full sm:w-auto bg-green-50 hover:bg-green-100 text-green-700 border-green-200 transition-all duration-200 hover:scale-105 hover:shadow-lg hover:-translate-y-0.5">
                  <UserPlus className="h-4 w-4 mr-2" />
                  Добавить пользователя
                </Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Добавить нового пользователя</DialogTitle>
                </DialogHeader>
                <AddUserForm 
                  onSuccess={() => {
                    setShowAddUserDialog(false)
                    loadUsers()
                  }}
                  projects={projects}
                />
              </DialogContent>
            </Dialog>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {users.map((user) => (
              <div key={user.id} className="flex flex-col sm:flex-row sm:items-center justify-between p-3 sm:p-4 border rounded-lg gap-3">
                <div className="flex items-center space-x-4 min-w-0 flex-1">
                  <div className="min-w-0 flex-1">
                    <p className="font-medium truncate">
                      {user.first_name} {user.last_name}
                    </p>
                    <p className="text-sm text-gray-600 truncate">@{user.username}</p>
                    <p className="text-xs text-gray-500">ID: {user.telegram_id}</p>
                  </div>
                </div>
                <div className="flex flex-wrap items-center gap-2">
                  <Badge className={getRoleColor(user.role)}>
                    {getRoleLabel(user.role)}
                  </Badge>
                  <Badge variant={user.is_active ? "default" : "destructive"}>
                    {user.is_active ? "Активен" : "Заблокирован"}
                  </Badge>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Запросы на одобрение */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Clock className="h-5 w-5" />
            Запросы на одобрение
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {pendingApprovals.length === 0 ? (
              <p className="text-center text-gray-500 py-8">
                Нет запросов на одобрение
              </p>
            ) : (
              pendingApprovals.map((approval) => (
                <div key={approval.id} className="border rounded-lg p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-medium">
                        {getActionTypeLabel(approval.action_type)}
                      </p>
                      <p className="text-sm text-gray-600">
                        От: {approval.requester.first_name} {approval.requester.last_name}
                      </p>
                      <p className="text-xs text-gray-500">
                        {new Date(approval.created_at).toLocaleString('ru-RU')}
                      </p>
                    </div>
                    <div className="flex space-x-2">
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => setSelectedApproval(approval)}
                        className="hover:bg-blue-50 hover:border-blue-300 transition-all duration-200 hover:scale-105 hover:shadow-lg hover:-translate-y-0.5"
                      >
                        <Eye className="h-4 w-4 mr-2" />
                        Просмотр
                      </Button>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </CardContent>
      </Card>

      {/* Модальное окно для просмотра запроса */}
      {selectedApproval && (
        <ApprovalReviewModal
          approval={selectedApproval}
          onApprove={(comment) => handleApproval(selectedApproval.id, 'approved', comment)}
          onReject={(comment) => handleApproval(selectedApproval.id, 'rejected', comment)}
          onClose={() => setSelectedApproval(null)}
        />
      )}
    </div>
  )
}

// Компонент для добавления пользователя
function AddUserForm({ onSuccess, projects }: { onSuccess: () => void, projects: Project[] }) {
  const { toast } = useToast()
  const [formData, setFormData] = useState({
    telegram_id: '',
    first_name: '',
    last_name: '',
    project_id: '',
    role: 'worker'
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await apiService.addUser(formData)
      toast({
        title: "Пользователь добавлен",
        description: "Новый пользователь успешно добавлен в систему",
      })
      onSuccess()
    } catch (error) {
      toast({
        title: "Ошибка",
        description: "Не удалось добавить пользователя",
        variant: "destructive"
      })
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <Label htmlFor="telegram_id">Telegram ID</Label>
        <Input
          id="telegram_id"
          type="number"
          value={formData.telegram_id}
          onChange={(e) => setFormData({...formData, telegram_id: e.target.value})}
          required
        />
      </div>
      <div>
        <Label htmlFor="first_name">Имя</Label>
        <Input
          id="first_name"
          value={formData.first_name}
          onChange={(e) => setFormData({...formData, first_name: e.target.value})}
          required
        />
      </div>
      <div>
        <Label htmlFor="last_name">Фамилия</Label>
        <Input
          id="last_name"
          value={formData.last_name}
          onChange={(e) => setFormData({...formData, last_name: e.target.value})}
        />
      </div>
      <div>
        <Label htmlFor="project_id">Проект</Label>
        <Select value={formData.project_id} onValueChange={(value) => setFormData({...formData, project_id: value})}>
          <SelectTrigger>
            <SelectValue placeholder="Выберите проект" />
          </SelectTrigger>
          <SelectContent>
            {projects.map((project) => (
              <SelectItem key={project.id} value={project.id.toString()}>
                {project.name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
      <div>
        <Label htmlFor="role">Роль</Label>
        <Select value={formData.role} onValueChange={(value) => setFormData({...formData, role: value})}>
          <SelectTrigger>
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="foreman">Прораб</SelectItem>
            <SelectItem value="worker">Рабочий</SelectItem>
            <SelectItem value="viewer">Наблюдатель</SelectItem>
          </SelectContent>
        </Select>
      </div>
      <Button type="submit" className="w-full bg-green-600 hover:bg-green-700 transition-all duration-200 hover:scale-105 hover:shadow-lg hover:-translate-y-0.5">
        Добавить пользователя
      </Button>
    </form>
  )
}

// Компонент для просмотра и одобрения запроса
function ApprovalReviewModal({ 
  approval, 
  onApprove, 
  onReject, 
  onClose 
}: {
  approval: ApprovalRequest
  onApprove: (comment?: string) => void
  onReject: (comment?: string) => void
  onClose: () => void
}) {
  const [comment, setComment] = useState('')

  return (
    <Dialog open={true} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>Запрос на одобрение</DialogTitle>
        </DialogHeader>
        
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>Тип действия</Label>
              <p className="font-medium">{approval.action_type}</p>
            </div>
            <div>
              <Label>Запросил</Label>
              <p className="font-medium">
                {approval.requester.first_name} {approval.requester.last_name}
              </p>
            </div>
          </div>

          <div>
            <Label>Данные действия</Label>
            <pre className="bg-gray-100 p-4 rounded text-sm overflow-auto">
              {JSON.stringify(JSON.parse(approval.action_data || '{}'), null, 2)}
            </pre>
          </div>

          <div>
            <Label htmlFor="comment">Комментарий (необязательно)</Label>
            <Textarea
              id="comment"
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              placeholder="Оставьте комментарий к решению..."
            />
          </div>

          <div className="flex justify-end space-x-2">
            <Button variant="outline" onClick={onClose} className="hover:bg-gray-50 hover:border-gray-300 transition-all duration-200 hover:scale-105 hover:shadow-lg hover:-translate-y-0.5">
              Отмена
            </Button>
            <Button 
              variant="destructive" 
              onClick={() => onReject(comment)}
              className="hover:bg-red-600 hover:border-red-700 transition-all duration-200 hover:scale-105 hover:shadow-lg hover:-translate-y-0.5"
            >
              <XCircle className="h-4 w-4 mr-2" />
              Отклонить
            </Button>
            <Button onClick={() => onApprove(comment)} className="bg-green-600 hover:bg-green-700 transition-all duration-200 hover:scale-105 hover:shadow-lg hover:-translate-y-0.5">
              <CheckCircle className="h-4 w-4 mr-2" />
              Одобрить
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}
