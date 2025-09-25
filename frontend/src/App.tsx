import { Routes, Route } from 'react-router-dom'
import { Toaster } from '@/components/ui/toaster'
import { AuthProvider, useAuth } from '@/contexts/AuthContext'
import { Layout } from '@/components/Layout'
import { Dashboard } from '@/pages/Dashboard'
import { Projects } from '@/pages/Projects'
import { Kanban } from '@/pages/Kanban'
import { Settings } from '@/pages/Settings'
import { TestPage } from '@/pages/TestPage'
import { AdminPanel } from '@/pages/AdminPanel'
import { Unauthorized } from '@/pages/Unauthorized'

function AppContent() {
  const { user, isLoading } = useAuth()

  if (isLoading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Загрузка...</p>
        </div>
      </div>
    )
  }

  if (!user) {
    return <Unauthorized />
  }

  return (
    <div className="min-h-screen bg-background">
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/projects" element={<Projects />} />
          <Route path="/kanban/:projectId" element={<Kanban />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/test" element={<TestPage />} />
          {user.role === 'creator' && (
            <Route path="/admin" element={<AdminPanel />} />
          )}
        </Routes>
      </Layout>
      <Toaster />
    </div>
  )
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  )
}

export default App
