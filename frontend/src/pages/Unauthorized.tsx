import { Shield } from 'lucide-react'

export function Unauthorized() {
  return (
    <div className="min-h-screen bg-background flex items-center justify-center">
      <div className="text-center">
        <Shield className="h-24 w-24 mx-auto text-red-500 mb-6" />
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Доступ ограничен
        </h1>
        <p className="text-lg text-gray-600 mb-8">
          Этот сайт доступен только через Telegram WebApp
        </p>
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 max-w-md mx-auto">
          <p className="text-blue-800">
            Для доступа к системе управления проектами:
          </p>
          <ol className="text-blue-700 text-left mt-3 space-y-2">
            <li>1. Откройте Telegram</li>
            <li>2. Найдите бота @ProjectManagerRuBot</li>
            <li>3. Нажмите /start</li>
            <li>4. Выберите "Открыть веб-приложение"</li>
          </ol>
        </div>
      </div>
    </div>
  )
}