import { useAuth } from '@/contexts/AuthContext'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { User, Settings as SettingsIcon, LogOut } from 'lucide-react'

export function Settings() {
  const { user, logout } = useAuth()

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Настройки</h1>
        <p className="text-gray-600 mt-2">
          Управление профилем и настройками приложения
        </p>
      </div>

      {/* User Profile */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <User className="h-5 w-5" />
            Профиль пользователя
          </CardTitle>
          <CardDescription>
            Информация о вашем аккаунте
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium text-gray-700">Имя</label>
              <p className="text-gray-900">{user?.first_name} {user?.last_name}</p>
            </div>
            <div>
              <label className="text-sm font-medium text-gray-700">Username</label>
              <p className="text-gray-900">@{user?.username || 'user'}</p>
            </div>
            <div>
              <label className="text-sm font-medium text-gray-700">Telegram ID</label>
              <p className="text-gray-900">{user?.telegram_id}</p>
            </div>
            <div>
              <label className="text-sm font-medium text-gray-700">Роль</label>
              <p className="text-gray-900 capitalize">{user?.role}</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* App Settings */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <SettingsIcon className="h-5 w-5" />
            Настройки приложения
          </CardTitle>
          <CardDescription>
            Персонализация интерфейса и поведения
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="font-medium">Темная тема</h3>
              <p className="text-sm text-gray-500">Переключить на темную тему</p>
            </div>
            <Button variant="outline" size="sm">
              Скоро
            </Button>
          </div>
          <div className="flex items-center justify-between">
            <div>
              <h3 className="font-medium">Уведомления</h3>
              <p className="text-sm text-gray-500">Настройка уведомлений</p>
            </div>
            <Button variant="outline" size="sm">
              Скоро
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Danger Zone */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-red-600">
            <LogOut className="h-5 w-5" />
            Выход из системы
          </CardTitle>
          <CardDescription>
            Выйти из текущего аккаунта
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Button variant="destructive" onClick={logout}>
            <LogOut className="h-4 w-4 mr-2" />
            Выйти
          </Button>
        </CardContent>
      </Card>
    </div>
  )
}
