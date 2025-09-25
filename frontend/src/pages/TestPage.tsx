import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { apiService } from '@/lib/api'

export function TestPage() {
  const [telegramId, setTelegramId] = useState('434532312')
  const [authToken, setAuthToken] = useState('')
  const [testResults, setTestResults] = useState<string[]>([])
  const [isLoading, setIsLoading] = useState(false)

  const addResult = (message: string) => {
    setTestResults(prev => [...prev, `${new Date().toLocaleTimeString()}: ${message}`])
  }

  const testAuth = async () => {
    setIsLoading(true)
    try {
      addResult(`Тестируем авторизацию для telegram_id: ${telegramId}`)
      const response = await apiService.auth(parseInt(telegramId))
      setAuthToken(response.data.access_token)
      addResult(`✅ Авторизация успешна! Токен получен`)
      addResult(`Пользователь: ${response.data.user.first_name} ${response.data.user.last_name}`)
    } catch (error: any) {
      addResult(`❌ Ошибка авторизации: ${error.response?.data?.detail || error.message}`)
    }
    setIsLoading(false)
  }

  const testProjects = async () => {
    if (!authToken) {
      addResult('❌ Сначала выполните авторизацию')
      return
    }

    setIsLoading(true)
    try {
      // Сохраняем токен в localStorage
      localStorage.setItem('auth_token', authToken)
      addResult('🔑 Токен сохранен в localStorage')

      // Тестируем получение проектов
      addResult('📋 Получаем список проектов...')
      const projectsResponse = await apiService.getProjects()
      addResult(`✅ Проекты получены: ${projectsResponse.data.length} штук`)

      // Тестируем создание проекта
      addResult('➕ Создаем тестовый проект...')
      const newProject = await apiService.createProject({
        name: `Тестовый проект ${Date.now()}`,
        description: 'Проект создан через тестовую страницу',
        color: '#3B82F6'
      })
      addResult(`✅ Проект создан: ${newProject.data.name} (ID: ${newProject.data.id})`)

    } catch (error: any) {
      addResult(`❌ Ошибка: ${error.response?.data?.detail || error.message}`)
      if (error.response?.status === 401) {
        addResult('🔑 Токен авторизации недействителен')
      }
    }
    setIsLoading(false)
  }

  const clearResults = () => {
    setTestResults([])
    setAuthToken('')
    localStorage.removeItem('auth_token')
  }

  return (
    <div className="container mx-auto p-6 space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Тестовая страница API</h1>
        <p className="text-gray-600 mt-2">
          Проверка работы API и авторизации
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Панель управления */}
        <Card>
          <CardHeader>
            <CardTitle>Управление тестами</CardTitle>
            <CardDescription>
              Выполните тесты для проверки работы API
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label htmlFor="telegramId">Telegram ID</Label>
              <Input
                id="telegramId"
                value={telegramId}
                onChange={(e) => setTelegramId(e.target.value)}
                placeholder="Введите Telegram ID"
              />
            </div>

            <div className="space-y-2">
              <Button 
                onClick={testAuth} 
                disabled={isLoading}
                className="w-full"
              >
                🔑 Тест авторизации
              </Button>
              
              <Button 
                onClick={testProjects} 
                disabled={isLoading || !authToken}
                variant="outline"
                className="w-full"
              >
                📋 Тест проектов
              </Button>
              
              <Button 
                onClick={clearResults} 
                variant="destructive"
                className="w-full"
              >
                🗑️ Очистить результаты
              </Button>
            </div>

            {authToken && (
              <div className="p-3 bg-green-50 border border-green-200 rounded">
                <p className="text-sm text-green-800">
                  <strong>Токен получен:</strong><br />
                  <code className="text-xs break-all">{authToken.substring(0, 50)}...</code>
                </p>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Результаты тестов */}
        <Card>
          <CardHeader>
            <CardTitle>Результаты тестов</CardTitle>
            <CardDescription>
              Лог выполнения тестов
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-96 overflow-y-auto bg-gray-50 p-4 rounded border">
              {testResults.length === 0 ? (
                <p className="text-gray-500 text-center">
                  Нажмите "Тест авторизации" для начала
                </p>
              ) : (
                <div className="space-y-1">
                  {testResults.map((result, index) => (
                    <div 
                      key={index}
                      className={`text-sm p-2 rounded ${
                        result.includes('✅') ? 'bg-green-100 text-green-800' :
                        result.includes('❌') ? 'bg-red-100 text-red-800' :
                        result.includes('🔑') ? 'bg-blue-100 text-blue-800' :
                        'bg-gray-100 text-gray-800'
                      }`}
                    >
                      {result}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
