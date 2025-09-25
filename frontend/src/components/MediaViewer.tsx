import React, { useState, useRef } from 'react'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { ConstructionLoader } from '@/components/ui/construction-loader'
import { 
  X, 
  ChevronLeft, 
  ChevronRight, 
  Download, 
  Play, 
  Pause, 
  Volume2, 
  VolumeX,
  Maximize2,
  RotateCw,
  Calendar,
  User,
  Eye,
  EyeOff
} from 'lucide-react'
import { cn } from '@/lib/utils'

interface MediaItem {
  id: number
  url: string
  type: 'image' | 'video'
  thumbnail?: string
  title?: string
  description?: string
  uploaded_at: string
  uploaded_by?: string
  file_size?: string
}

interface MediaViewerProps {
  media: MediaItem[]
  isOpen: boolean
  onClose: () => void
  initialIndex?: number
}

export function MediaViewer({ media, isOpen, onClose, initialIndex = 0 }: MediaViewerProps) {
  const [currentIndex, setCurrentIndex] = useState(initialIndex)
  const [isFullscreen, setIsFullscreen] = useState(false)
  const [isPlaying, setIsPlaying] = useState(false)
  const [isMuted, setIsMuted] = useState(true)
  const [showInfo, setShowInfo] = useState(false)
  const [loading, setLoading] = useState(false)
  const videoRef = useRef<HTMLVideoElement>(null)
  const containerRef = useRef<HTMLDivElement>(null)

  const currentMedia = media[currentIndex]
  const isVideo = currentMedia?.type === 'video'

  const handlePrevious = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1)
      setIsPlaying(false)
    }
  }

  const handleNext = () => {
    if (currentIndex < media.length - 1) {
      setCurrentIndex(currentIndex + 1)
      setIsPlaying(false)
    }
  }

  const handlePlayPause = () => {
    if (isVideo && videoRef.current) {
      if (isPlaying) {
        videoRef.current.pause()
      } else {
        videoRef.current.play()
      }
      setIsPlaying(!isPlaying)
    }
  }

  const handleMuteToggle = () => {
    if (videoRef.current) {
      videoRef.current.muted = !isMuted
      setIsMuted(!isMuted)
    }
  }

  const handleDownload = () => {
    if (currentMedia) {
      const link = document.createElement('a')
      link.href = currentMedia.url
      link.download = currentMedia.title || `media_${currentMedia.id}`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }
  }

  const handleFullscreen = () => {
    if (containerRef.current) {
      if (!isFullscreen) {
        containerRef.current.requestFullscreen()
        setIsFullscreen(true)
      } else {
        document.exitFullscreen()
        setIsFullscreen(false)
      }
    }
  }

  const handleKeyDown = (e: KeyboardEvent) => {
    switch (e.key) {
      case 'ArrowLeft':
        handlePrevious()
        break
      case 'ArrowRight':
        handleNext()
        break
      case ' ':
        e.preventDefault()
        handlePlayPause()
        break
      case 'Escape':
        onClose()
        break
      case 'f':
      case 'F':
        handleFullscreen()
        break
    }
  }

  React.useEffect(() => {
    if (isOpen) {
      document.addEventListener('keydown', handleKeyDown)
      return () => document.removeEventListener('keydown', handleKeyDown)
    }
  }, [isOpen, currentIndex, isPlaying])

  React.useEffect(() => {
    if (isOpen) {
      setCurrentIndex(initialIndex)
    }
  }, [isOpen, initialIndex])

  if (!isOpen || !currentMedia) return null

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-[95vw] max-h-[95vh] p-0 overflow-hidden">
        <div 
          ref={containerRef}
          className="relative bg-black flex flex-col h-full"
        >
          {/* Header */}
          <DialogHeader className="absolute top-0 left-0 right-0 z-10 bg-gradient-to-b from-black/80 to-transparent p-4">
            <div className="flex items-center justify-between text-white">
              <DialogTitle className="flex items-center gap-2">
                <Eye className="h-5 w-5" />
                Медиа файлы ({currentIndex + 1} из {media.length})
              </DialogTitle>
              <div className="flex items-center gap-2">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setShowInfo(!showInfo)}
                  className="text-white hover:bg-white/20"
                >
                  {showInfo ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={handleFullscreen}
                  className="text-white hover:bg-white/20"
                >
                  <Maximize2 className="h-4 w-4" />
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={onClose}
                  className="text-white hover:bg-white/20"
                >
                  <X className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </DialogHeader>

          {/* Main Content */}
          <div className="flex-1 flex items-center justify-center relative">
            {loading && (
              <div className="absolute inset-0 flex items-center justify-center bg-black/50 z-20">
                <ConstructionLoader size="lg" />
              </div>
            )}

            {/* Media Content */}
            <div className="relative w-full h-full flex items-center justify-center">
              {isVideo ? (
                <video
                  ref={videoRef}
                  src={currentMedia.url}
                  className="max-w-full max-h-full object-contain"
                  onLoadStart={() => setLoading(true)}
                  onLoadedData={() => setLoading(false)}
                  onPlay={() => setIsPlaying(true)}
                  onPause={() => setIsPlaying(false)}
                  onEnded={() => setIsPlaying(false)}
                  poster={currentMedia.thumbnail}
                  loop
                />
              ) : (
                <img
                  src={currentMedia.url}
                  alt={currentMedia.title || 'Изображение'}
                  className="max-w-full max-h-full object-contain"
                  onLoadStart={() => setLoading(true)}
                  onLoad={() => setLoading(false)}
                />
              )}

              {/* Video Controls Overlay */}
              {isVideo && (
                <div className="absolute inset-0 flex items-center justify-center">
                  <Button
                    size="lg"
                    variant="ghost"
                    onClick={handlePlayPause}
                    className="text-white hover:bg-white/20 bg-black/50 rounded-full w-16 h-16"
                  >
                    {isPlaying ? (
                      <Pause className="h-8 w-8" />
                    ) : (
                      <Play className="h-8 w-8 ml-1" />
                    )}
                  </Button>
                </div>
              )}
            </div>

            {/* Navigation Arrows */}
            {media.length > 1 && (
              <>
                <Button
                  variant="ghost"
                  size="lg"
                  onClick={handlePrevious}
                  disabled={currentIndex === 0}
                  className="absolute left-4 top-1/2 transform -translate-y-1/2 text-white hover:bg-white/20 bg-black/50 rounded-full w-12 h-12"
                >
                  <ChevronLeft className="h-6 w-6" />
                </Button>
                <Button
                  variant="ghost"
                  size="lg"
                  onClick={handleNext}
                  disabled={currentIndex === media.length - 1}
                  className="absolute right-4 top-1/2 transform -translate-y-1/2 text-white hover:bg-white/20 bg-black/50 rounded-full w-12 h-12"
                >
                  <ChevronRight className="h-6 w-6" />
                </Button>
              </>
            )}
          </div>

          {/* Footer Controls */}
          <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-4">
            <div className="flex items-center justify-between text-white">
              <div className="flex items-center gap-4">
                {isVideo && (
                  <>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={handleMuteToggle}
                      className="text-white hover:bg-white/20"
                    >
                      {isMuted ? <VolumeX className="h-4 w-4" /> : <Volume2 className="h-4 w-4" />}
                    </Button>
                    <div className="text-sm">
                      {isPlaying ? 'Воспроизведение' : 'Пауза'}
                    </div>
                  </>
                )}
              </div>

              <div className="flex items-center gap-2">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={handleDownload}
                  className="text-white hover:bg-white/20"
                >
                  <Download className="h-4 w-4 mr-2" />
                  Скачать
                </Button>
              </div>
            </div>

            {/* Thumbnail Strip */}
            {media.length > 1 && (
              <div className="mt-4 flex gap-2 overflow-x-auto">
                {media.map((item, index) => (
                  <button
                    key={item.id}
                    onClick={() => setCurrentIndex(index)}
                    className={cn(
                      "flex-shrink-0 w-16 h-16 rounded-lg overflow-hidden border-2 transition-all duration-200",
                      index === currentIndex 
                        ? "border-blue-500 scale-110" 
                        : "border-transparent hover:border-white/50"
                    )}
                  >
                    {item.type === 'video' ? (
                      <div className="relative w-full h-full bg-gray-800 flex items-center justify-center">
                        <Play className="h-4 w-4 text-white" />
                        {item.thumbnail && (
                          <img 
                            src={item.thumbnail} 
                            alt="Thumbnail"
                            className="absolute inset-0 w-full h-full object-cover"
                          />
                        )}
                      </div>
                    ) : (
                      <img 
                        src={item.url} 
                        alt={`Thumbnail ${index + 1}`}
                        className="w-full h-full object-cover"
                      />
                    )}
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Info Panel */}
          {showInfo && (
            <div className="absolute top-16 left-4 right-4 bg-black/80 backdrop-blur-sm rounded-lg p-4 text-white">
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <Badge variant="secondary">
                    {currentMedia.type === 'video' ? 'Видео' : 'Изображение'}
                  </Badge>
                  {currentMedia.file_size && (
                    <Badge variant="outline" className="text-white border-white/30">
                      {currentMedia.file_size}
                    </Badge>
                  )}
                </div>
                
                {currentMedia.title && (
                  <h3 className="font-semibold">{currentMedia.title}</h3>
                )}
                
                {currentMedia.description && (
                  <p className="text-sm text-gray-300">{currentMedia.description}</p>
                )}
                
                <div className="flex items-center gap-4 text-xs text-gray-400">
                  <div className="flex items-center gap-1">
                    <Calendar className="h-3 w-3" />
                    {new Date(currentMedia.uploaded_at).toLocaleDateString('ru-RU')}
                  </div>
                  {currentMedia.uploaded_by && (
                    <div className="flex items-center gap-1">
                      <User className="h-3 w-3" />
                      {currentMedia.uploaded_by}
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  )
}

// Компонент для отображения медиа в карточке задачи
export function TaskMediaPreview({ 
  media, 
  onView 
}: { 
  media: MediaItem[]
  onView: (index: number) => void 
}) {
  if (media.length === 0) return null

  const images = media.filter(item => item.type === 'image')
  const videos = media.filter(item => item.type === 'video')

  return (
    <div className="space-y-2">
      {/* Изображения */}
      {images.length > 0 && (
        <div className="grid grid-cols-2 gap-2">
          {images.slice(0, 4).map((item, index) => (
            <button
              key={item.id}
              onClick={() => onView(media.indexOf(item))}
              className="relative group rounded-lg overflow-hidden aspect-square bg-gray-100 hover:scale-105 transition-transform duration-200"
            >
              <img
                src={item.url}
                alt={item.title || 'Изображение'}
                className="w-full h-full object-cover"
              />
              <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-all duration-200 flex items-center justify-center">
                <Eye className="h-4 w-4 text-white opacity-0 group-hover:opacity-100 transition-opacity duration-200" />
              </div>
              {images.length > 4 && index === 3 && (
                <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center">
                  <span className="text-white text-sm font-medium">+{images.length - 4}</span>
                </div>
              )}
            </button>
          ))}
        </div>
      )}

      {/* Видео */}
      {videos.length > 0 && (
        <div className="space-y-2">
          {videos.map((item, index) => (
            <button
              key={item.id}
              onClick={() => onView(media.indexOf(item))}
              className="w-full relative group rounded-lg overflow-hidden bg-gray-100 hover:scale-105 transition-transform duration-200"
            >
              <div className="aspect-video relative">
                {item.thumbnail ? (
                  <img
                    src={item.thumbnail}
                    alt={item.title || 'Видео'}
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <div className="w-full h-full bg-gray-800 flex items-center justify-center">
                    <Play className="h-8 w-8 text-white" />
                  </div>
                )}
                <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-all duration-200 flex items-center justify-center">
                  <Play className="h-8 w-8 text-white opacity-0 group-hover:opacity-100 transition-opacity duration-200" />
                </div>
                <Badge className="absolute top-2 left-2 bg-red-600">
                  Видео
                </Badge>
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
