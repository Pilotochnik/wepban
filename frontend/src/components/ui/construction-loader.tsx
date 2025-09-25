import React from 'react'
import { cn } from '@/lib/utils'

interface ConstructionLoaderProps {
  size?: 'sm' | 'md' | 'lg'
  className?: string
}

export function ConstructionLoader({ size = 'md', className }: ConstructionLoaderProps) {
  const sizeClasses = {
    sm: 'w-8 h-8',
    md: 'w-12 h-12',
    lg: 'w-16 h-16'
  }

  return (
    <div className={cn("flex flex-col items-center justify-center space-y-4", className)}>
      {/* Строительный кран */}
      <div className={cn("relative", sizeClasses[size])}>
        {/* База крана */}
        <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-2 h-8 bg-gray-600 rounded-t-lg">
          {/* Горизонтальная балка */}
          <div className="absolute top-0 left-1/2 transform -translate-x-1/2 w-16 h-1 bg-blue-600 rounded-sm">
            {/* Канат */}
            <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-0.5 h-8 bg-gray-400 animate-pulse">
              {/* Груз */}
              <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-3 h-3 bg-yellow-500 rounded-sm animate-bounce">
                <div className="absolute inset-0 bg-yellow-400 rounded-sm animate-ping opacity-75"></div>
              </div>
            </div>
          </div>
          
          {/* Кабина оператора */}
          <div className="absolute -top-2 left-1/2 transform -translate-x-1/2 w-3 h-2 bg-orange-500 rounded-sm">
            <div className="absolute inset-0 bg-orange-400 rounded-sm animate-pulse"></div>
          </div>
        </div>
      </div>

      {/* Строительные блоки */}
      <div className="flex space-x-1">
        <div className="w-2 h-2 bg-red-500 rounded animate-bounce" style={{ animationDelay: '0ms' }}></div>
        <div className="w-2 h-2 bg-blue-500 rounded animate-bounce" style={{ animationDelay: '150ms' }}></div>
        <div className="w-2 h-2 bg-green-500 rounded animate-bounce" style={{ animationDelay: '300ms' }}></div>
        <div className="w-2 h-2 bg-yellow-500 rounded animate-bounce" style={{ animationDelay: '450ms' }}></div>
      </div>

      {/* Текст загрузки */}
      <div className="text-center">
        <p className="text-sm font-medium text-gray-600 animate-pulse">
          Строим проект...
        </p>
        <div className="flex justify-center mt-1">
          <div className="w-1 h-1 bg-blue-500 rounded-full animate-ping mx-1"></div>
          <div className="w-1 h-1 bg-blue-500 rounded-full animate-ping mx-1" style={{ animationDelay: '200ms' }}></div>
          <div className="w-1 h-1 bg-blue-500 rounded-full animate-ping mx-1" style={{ animationDelay: '400ms' }}></div>
        </div>
      </div>
    </div>
  )
}

// Компонент для полноэкранной загрузки
export function ConstructionLoadingScreen({ message = "Загружаем проект..." }: { message?: string }) {
  return (
    <div className="fixed inset-0 bg-gradient-to-br from-blue-50 via-white to-orange-50 flex items-center justify-center z-50">
      <div className="text-center space-y-8">
        <ConstructionLoader size="lg" />
        <div className="space-y-2">
          <h2 className="text-xl font-semibold text-gray-800">{message}</h2>
          <p className="text-sm text-gray-600">Пожалуйста, подождите...</p>
        </div>
        
        {/* Прогресс-бар в виде строительных блоков */}
        <div className="flex justify-center space-x-1">
          {[0, 1, 2, 3, 4, 5, 6, 7].map((i) => (
            <div
              key={i}
              className="w-3 h-3 bg-blue-500 rounded animate-pulse"
              style={{ 
                animationDelay: `${i * 100}ms`,
                animationDuration: '1s'
              }}
            ></div>
          ))}
        </div>
      </div>
    </div>
  )
}