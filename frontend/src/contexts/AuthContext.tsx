import { createContext, useContext, useState, useEffect, ReactNode } from 'react'

declare global {
  interface Window {
    Telegram?: {
      WebApp: any
    }
  }
}
import { api } from '@/lib/api'

interface User {
  id: number
  telegram_id: number
  username?: string
  first_name?: string
  last_name?: string
  role: 'admin' | 'user' | 'viewer'
  is_active: boolean
}

interface AuthContextType {
  user: User | null
  token: string | null
  login: (telegramId: number) => Promise<void>
  logout: () => void
  isLoading: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    initializeAuth()
  }, [])

  const initializeAuth = async () => {
    try {
      // Проверяем, запущено ли приложение в Telegram WebApp
      if (window.Telegram?.WebApp) {
        const tg = window.Telegram.WebApp
        tg.ready()
        
        // Получаем данные пользователя из Telegram
        const userData = tg.initDataUnsafe.user
        if (userData) {
          await login(userData.id)
        }
      } else {
        // Для разработки - автоматически авторизуемся как тестовый пользователь
        console.log('Running in development mode, auto-login as test user')
        await login(434532312) // Используем ваш Telegram ID
      }
      
    } catch (error) {
      console.error('Ошибка инициализации авторизации:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const login = async (telegramId: number) => {
    try {
      console.log('Attempting login with telegram_id:', telegramId)
      const response = await api.post('/api/v1/users/auth', { telegram_id: telegramId })
      console.log('Login response:', response.data)
      const { access_token, user: userData } = response.data
      
      setToken(access_token)
      setUser(userData)
      
      // Сохраняем токен в localStorage
      localStorage.setItem('auth_token', access_token)
      
      // Устанавливаем токен для API запросов
      api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
      console.log('Login successful for user:', userData)
    } catch (error) {
      console.error('Ошибка авторизации:', error)
      throw error
    }
  }

  const logout = () => {
    setUser(null)
    setToken(null)
    localStorage.removeItem('auth_token')
    delete api.defaults.headers.common['Authorization']
  }

  const value = {
    user,
    token,
    login,
    logout,
    isLoading
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth должен использоваться внутри AuthProvider')
  }
  return context
}
