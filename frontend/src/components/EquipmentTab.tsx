import React, { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { useToast } from '@/hooks/use-toast'
import { ConstructionLoader } from '@/components/ui/construction-loader'
import { 
  Camera, 
  Upload, 
  Eye, 
  Trash2, 
  Calendar,
  Wrench,
  Truck,
  Hammer,
  Plus,
  Grid3X3,
  List,
  Search,
  Filter
} from 'lucide-react'
import { cn } from '@/lib/utils'

interface EquipmentPhoto {
  id: number
  equipment_id: number
  photo_url: string
  stage: 'start' | 'end'
  description?: string
  taken_at: string
  taken_by?: string
}

interface Equipment {
  id: number
  project_id: number
  name: string
  type: string
  model?: string
  status: 'active' | 'inactive' | 'maintenance'
  photos: EquipmentPhoto[]
  created_at: string
}

interface EquipmentTabProps {
  projectId: number
}

const equipmentTypes = [
  { value: 'excavator', label: 'Экскаватор', icon: '🚜' },
  { value: 'crane', label: 'Кран', icon: '🏗️' },
  { value: 'bulldozer', label: 'Бульдозер', icon: '🚧' },
  { value: 'truck', label: 'Грузовик', icon: '🚛' },
  { value: 'concrete_mixer', label: 'Бетономешалка', icon: '🔄' },
  { value: 'generator', label: 'Генератор', icon: '⚡' },
  { value: 'compressor', label: 'Компрессор', icon: '💨' },
  { value: 'other', label: 'Другое', icon: '🔧' }
]

export function EquipmentTab({ projectId }: EquipmentTabProps) {
  const { toast } = useToast()
  const [equipment, setEquipment] = useState<Equipment[]>([])
  const [loading, setLoading] = useState(false)
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid')
  const [selectedEquipment, setSelectedEquipment] = useState<Equipment | null>(null)
  const [showAddDialog, setShowAddDialog] = useState(false)
  const [showPhotoDialog, setShowPhotoDialog] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const [filterType, setFilterType] = useState('all')

  // Фильтрация оборудования
  const filteredEquipment = equipment.filter(item => {
    const matchesSearch = item.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         item.type.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesType = filterType === 'all' || item.type === filterType
    return matchesSearch && matchesType
  })

  const handleAddEquipment = async (data: any) => {
    setLoading(true)
    try {
      // Здесь будет API вызов для добавления техники
      const newEquipment: Equipment = {
        id: Date.now(),
        project_id: projectId,
        name: data.name,
        type: data.type,
        model: data.model,
        status: 'active',
        photos: [],
        created_at: new Date().toISOString()
      }
      setEquipment(prev => [...prev, newEquipment])
      setShowAddDialog(false)
      toast({
        title: "Техника добавлена",
        description: `${data.name} успешно добавлена в проект`,
      })
    } catch (error) {
      toast({
        title: "Ошибка",
        description: "Не удалось добавить технику",
        variant: "destructive"
      })
    } finally {
      setLoading(false)
    }
  }

  const handleAddPhoto = async (equipmentId: number, photoData: any) => {
    try {
      // Здесь будет API вызов для добавления фото
      const newPhoto: EquipmentPhoto = {
        id: Date.now(),
        equipment_id: equipmentId,
        photo_url: URL.createObjectURL(photoData.file),
        stage: photoData.stage,
        description: photoData.description,
        taken_at: new Date().toISOString(),
        taken_by: 'Текущий пользователь'
      }
      
      setEquipment(prev => prev.map(item => 
        item.id === equipmentId 
          ? { ...item, photos: [...item.photos, newPhoto] }
          : item
      ))
      
      toast({
        title: "Фото добавлено",
        description: "Фото техники успешно загружено",
      })
    } catch (error) {
      toast({
        title: "Ошибка",
        description: "Не удалось загрузить фото",
        variant: "destructive"
      })
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800'
      case 'inactive': return 'bg-gray-100 text-gray-800'
      case 'maintenance': return 'bg-yellow-100 text-yellow-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'active': return 'Активна'
      case 'inactive': return 'Неактивна'
      case 'maintenance': return 'На ремонте'
      default: return status
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <ConstructionLoader size="lg" />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
            <Wrench className="h-6 w-6 text-blue-600" />
            Техника проекта
          </h2>
          <p className="text-gray-600 mt-1">
            Управление строительной техникой и фотоотчеты
          </p>
        </div>
        <Button 
          onClick={() => setShowAddDialog(true)}
          className="bg-blue-600 hover:bg-blue-700 transition-all duration-200 hover:scale-105 hover:shadow-lg hover:-translate-y-0.5"
        >
          <Plus className="h-4 w-4 mr-2" />
          Добавить технику
        </Button>
      </div>

      {/* Фильтры и поиск */}
      <Card>
        <CardContent className="p-4">
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                <Input
                  placeholder="Поиск техники..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>
            <Select value={filterType} onValueChange={setFilterType}>
              <SelectTrigger className="w-full sm:w-48">
                <SelectValue placeholder="Тип техники" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Все типы</SelectItem>
                {equipmentTypes.map(type => (
                  <SelectItem key={type.value} value={type.value}>
                    {type.icon} {type.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            <div className="flex gap-2">
              <Button
                variant={viewMode === 'grid' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setViewMode('grid')}
                className="hover:scale-105 transition-transform duration-200"
              >
                <Grid3X3 className="h-4 w-4" />
              </Button>
              <Button
                variant={viewMode === 'list' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setViewMode('list')}
                className="hover:scale-105 transition-transform duration-200"
              >
                <List className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Список техники */}
      {filteredEquipment.length === 0 ? (
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-12">
            <Truck className="h-16 w-16 text-gray-400 mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">Нет техники</h3>
            <p className="text-gray-500 text-center mb-6">
              Добавьте строительную технику для отслеживания работ
            </p>
            <Button onClick={() => setShowAddDialog(true)}>
              <Plus className="h-4 w-4 mr-2" />
              Добавить технику
            </Button>
          </CardContent>
        </Card>
      ) : (
        <div className={cn(
          "grid gap-4",
          viewMode === 'grid' 
            ? "grid-cols-1 sm:grid-cols-2 lg:grid-cols-3" 
            : "grid-cols-1"
        )}>
          {filteredEquipment.map((item) => (
            <EquipmentCard
              key={item.id}
              equipment={item}
              onAddPhoto={handleAddPhoto}
              viewMode={viewMode}
            />
          ))}
        </div>
      )}

      {/* Диалог добавления техники */}
      <AddEquipmentDialog
        open={showAddDialog}
        onOpenChange={setShowAddDialog}
        onSubmit={handleAddEquipment}
        loading={loading}
      />

      {/* Диалог просмотра фото */}
      {selectedEquipment && (
        <EquipmentPhotoDialog
          equipment={selectedEquipment}
          open={!!selectedEquipment}
          onClose={() => setSelectedEquipment(null)}
          onAddPhoto={handleAddPhoto}
        />
      )}
    </div>
  )
}

// Карточка техники
function EquipmentCard({ 
  equipment, 
  onAddPhoto, 
  viewMode 
}: { 
  equipment: Equipment
  onAddPhoto: (equipmentId: number, photoData: any) => void
  viewMode: 'grid' | 'list'
}) {
  const startPhotos = equipment.photos.filter(p => p.stage === 'start')
  const endPhotos = equipment.photos.filter(p => p.stage === 'end')
  const equipmentType = equipmentTypes.find(t => t.value === equipment.type)

  return (
    <Card className="group hover:shadow-lg hover:shadow-blue-500/10 transition-all duration-300 hover:-translate-y-1 hover:scale-[1.02] border-0 bg-gradient-to-br from-white to-slate-50/50 backdrop-blur-sm rounded-xl">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="text-2xl">{equipmentType?.icon || '🔧'}</div>
            <div>
              <CardTitle className="text-lg group-hover:text-blue-600 transition-colors duration-300">
                {equipment.name}
              </CardTitle>
              {equipment.model && (
                <CardDescription className="text-sm">
                  {equipmentType?.label} • {equipment.model}
                </CardDescription>
              )}
            </div>
          </div>
          <Badge className={getStatusColor(equipment.status)}>
            {getStatusLabel(equipment.status)}
          </Badge>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {/* Фото отчеты */}
          <div className="grid grid-cols-2 gap-3">
            <div className="text-center">
              <div className="text-sm font-medium text-green-700 mb-2">Начало работ</div>
              <div className="bg-green-50 border-2 border-dashed border-green-200 rounded-lg p-3 min-h-[80px] flex items-center justify-center">
                {startPhotos.length > 0 ? (
                  <div className="relative">
                    <img 
                      src={startPhotos[0].photo_url} 
                      alt="Начало работ"
                      className="w-full h-16 object-cover rounded"
                    />
                    {startPhotos.length > 1 && (
                      <Badge className="absolute -top-2 -right-2 bg-green-600">
                        +{startPhotos.length - 1}
                      </Badge>
                    )}
                  </div>
                ) : (
                  <div className="text-green-600">
                    <Camera className="h-6 w-6 mx-auto mb-1" />
                    <div className="text-xs">Нет фото</div>
                  </div>
                )}
              </div>
            </div>
            <div className="text-center">
              <div className="text-sm font-medium text-blue-700 mb-2">Конец работ</div>
              <div className="bg-blue-50 border-2 border-dashed border-blue-200 rounded-lg p-3 min-h-[80px] flex items-center justify-center">
                {endPhotos.length > 0 ? (
                  <div className="relative">
                    <img 
                      src={endPhotos[0].photo_url} 
                      alt="Конец работ"
                      className="w-full h-16 object-cover rounded"
                    />
                    {endPhotos.length > 1 && (
                      <Badge className="absolute -top-2 -right-2 bg-blue-600">
                        +{endPhotos.length - 1}
                      </Badge>
                    )}
                  </div>
                ) : (
                  <div className="text-blue-600">
                    <Camera className="h-6 w-6 mx-auto mb-1" />
                    <div className="text-xs">Нет фото</div>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Кнопки действий */}
          <div className="flex gap-2">
            <Button 
              size="sm" 
              className="flex-1 bg-blue-50 hover:bg-blue-100 text-blue-700 border-blue-200 transition-all duration-200 hover:scale-105 hover:shadow-lg hover:-translate-y-0.5"
              onClick={() => {/* Открыть просмотр фото */}}
            >
              <Eye className="h-4 w-4 mr-2" />
              Просмотр
            </Button>
            <Button 
              size="sm" 
              variant="outline"
              className="flex-1 hover:bg-green-50 hover:border-green-300 transition-all duration-200 hover:scale-105 hover:shadow-lg hover:-translate-y-0.5"
              onClick={() => {/* Добавить фото */}}
            >
              <Camera className="h-4 w-4 mr-2" />
              Фото
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

// Диалог добавления техники
function AddEquipmentDialog({ 
  open, 
  onOpenChange, 
  onSubmit, 
  loading 
}: {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSubmit: (data: any) => void
  loading: boolean
}) {
  const [formData, setFormData] = useState({
    name: '',
    type: '',
    model: ''
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit(formData)
    setFormData({ name: '', type: '', model: '' })
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Wrench className="h-5 w-5 text-blue-600" />
            Добавить технику
          </DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <Label htmlFor="name">Название техники</Label>
            <Input
              id="name"
              value={formData.name}
              onChange={(e) => setFormData({...formData, name: e.target.value})}
              placeholder="Например: Экскаватор CAT 320"
              required
            />
          </div>
          <div>
            <Label htmlFor="type">Тип техники</Label>
            <Select value={formData.type} onValueChange={(value) => setFormData({...formData, type: value})}>
              <SelectTrigger>
                <SelectValue placeholder="Выберите тип техники" />
              </SelectTrigger>
              <SelectContent>
                {equipmentTypes.map(type => (
                  <SelectItem key={type.value} value={type.value}>
                    {type.icon} {type.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div>
            <Label htmlFor="model">Модель (необязательно)</Label>
            <Input
              id="model"
              value={formData.model}
              onChange={(e) => setFormData({...formData, model: e.target.value})}
              placeholder="Например: CAT 320D"
            />
          </div>
          <div className="flex justify-end space-x-2">
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
              Отмена
            </Button>
            <Button type="submit" disabled={loading}>
              {loading ? (
                <>
                  <ConstructionLoader size="sm" className="mr-2" />
                  Добавление...
                </>
              ) : (
                'Добавить'
              )}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  )
}

// Диалог просмотра фото техники
function EquipmentPhotoDialog({ 
  equipment, 
  open, 
  onClose, 
  onAddPhoto 
}: {
  equipment: Equipment
  open: boolean
  onClose: () => void
  onAddPhoto: (equipmentId: number, photoData: any) => void
}) {
  const [activeStage, setActiveStage] = useState<'start' | 'end'>('start')
  const photos = equipment.photos.filter(p => p.stage === activeStage)

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Wrench className="h-5 w-5 text-blue-600" />
            Фото техники: {equipment.name}
          </DialogTitle>
        </DialogHeader>
        
        <div className="space-y-4">
          {/* Переключатель этапов */}
          <div className="flex gap-2">
            <Button
              variant={activeStage === 'start' ? 'default' : 'outline'}
              onClick={() => setActiveStage('start')}
              className="flex-1"
            >
              Начало работ ({equipment.photos.filter(p => p.stage === 'start').length})
            </Button>
            <Button
              variant={activeStage === 'end' ? 'default' : 'outline'}
              onClick={() => setActiveStage('end')}
              className="flex-1"
            >
              Конец работ ({equipment.photos.filter(p => p.stage === 'end').length})
            </Button>
          </div>

          {/* Галерея фото */}
          {photos.length === 0 ? (
            <div className="text-center py-12">
              <Camera className="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-500">Нет фото для этапа "{activeStage === 'start' ? 'Начало работ' : 'Конец работ'}"</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {photos.map((photo) => (
                <div key={photo.id} className="relative group">
                  <img
                    src={photo.photo_url}
                    alt={photo.description || 'Фото техники'}
                    className="w-full h-48 object-cover rounded-lg hover:scale-105 transition-transform duration-200"
                  />
                  <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-all duration-200 rounded-lg flex items-center justify-center">
                    <Button
                      size="sm"
                      variant="secondary"
                      className="opacity-0 group-hover:opacity-100 transition-opacity duration-200"
                    >
                      <Eye className="h-4 w-4 mr-2" />
                      Просмотр
                    </Button>
                  </div>
                  {photo.description && (
                    <div className="absolute bottom-0 left-0 right-0 bg-black bg-opacity-50 text-white p-2 rounded-b-lg">
                      <p className="text-sm truncate">{photo.description}</p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  )
}

function getStatusColor(status: string) {
  switch (status) {
    case 'active': return 'bg-green-100 text-green-800'
    case 'inactive': return 'bg-gray-100 text-gray-800'
    case 'maintenance': return 'bg-yellow-100 text-yellow-800'
    default: return 'bg-gray-100 text-gray-800'
  }
}

function getStatusLabel(status: string) {
  switch (status) {
    case 'active': return 'Активна'
    case 'inactive': return 'Неактивна'
    case 'maintenance': return 'На ремонте'
    default: return status
  }
}
