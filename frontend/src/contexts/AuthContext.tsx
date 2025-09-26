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
  role: 'creator' | 'foreman' | 'worker' | 'viewer'
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
    // Добавляем отладочную информацию
    console.log('AuthContext: Initializing...')
    console.log('User Agent:', navigator.userAgent)
    console.log('Window Telegram:', window.Telegram)
    
    initializeAuth()
  }, [])

  const initializeAuth = async () => {
    try {
      // Ждем загрузки Telegram WebApp API
      let attempts = 0
      const maxAttempts = 50 // 5 секунд максимум
      
      while (!window.Telegram?.WebApp && attempts < maxAttempts) {
        await new Promise(resolve => setTimeout(resolve, 100))
        attempts++
      }
      
      // Проверяем, запущено ли приложение в Telegram WebApp
      if (window.Telegram?.WebApp) {
        const tg = window.Telegram.WebApp
        console.log('Telegram WebApp detected:', tg)
        
        // Инициализируем WebApp
        tg.ready()
        tg.expand()
        
        // Получаем данные пользователя из Telegram
        const userData = tg.initDataUnsafe?.user
        console.log('Telegram user data:', userData)
        
        if (userData) {
          await login(userData.id)
        } else {
          // Пользователь не авторизован в Telegram WebApp
          console.log('User not authorized in Telegram WebApp')
          setUser(null)
        }
      } else {
        // Приложение запущено не в Telegram WebApp
        console.log('Application not running in Telegram WebApp')
        
        // Проверяем, есть ли сохраненный токен для тестирования
        const savedToken = localStorage.getItem('auth_token')
        if (savedToken) {
          console.log('Found saved token, attempting to restore session...')
          try {
            api.defaults.headers.common['Authorization'] = `Bearer ${savedToken}`
            const response = await api.get('/v1/users/me')
            setToken(savedToken)
            setUser(response.data)
            console.log('Session restored successfully')
          } catch (error) {
            console.log('Failed to restore session:', error)
            localStorage.removeItem('auth_token')
            setUser(null)
          }
        } else {
          setUser(null)
        }
      }
      
    } catch (error) {
      console.error('Ошибка инициализации авторизации:', error)
      setUser(null)
    } finally {
      setIsLoading(false)
    }
  }

  const login = async (telegramId: number) => {
    try {
      console.log('Attempting login with telegram_id:', telegramId)
      const response = await api.post('/v1/users/auth', { telegram_id: telegramId })
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
