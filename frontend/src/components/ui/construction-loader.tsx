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
      {/* Стоковая анимация загрузки */}
      <div className={cn("animate-spin", sizeClasses[size])}>
        <svg 
          className="w-full h-full text-blue-600" 
          fill="none" 
          viewBox="0 0 24 24"
        >
          <circle 
            className="opacity-25" 
            cx="12" 
            cy="12" 
            r="10" 
            stroke="currentColor" 
            strokeWidth="4"
          />
          <path 
            className="opacity-75" 
            fill="currentColor" 
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          />
        </svg>
      </div>

      {/* Текст загрузки */}
      <div className="text-center">
        <p className="text-sm font-medium text-gray-600 animate-pulse">
          Загружаем...
        </p>
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