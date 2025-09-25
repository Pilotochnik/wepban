import { Routes, Route } from 'react-router-dom'
import { Toaster } from '@/components/ui/toaster'
import { AuthProvider } from '@/contexts/AuthContext'
import { Layout } from '@/components/Layout'
import { Dashboard } from '@/pages/Dashboard'
import { Projects } from '@/pages/Projects'
import { Kanban } from '@/pages/Kanban'
import { Settings } from '@/pages/Settings'
import { TestPage } from '@/pages/TestPage'
import { AdminPanel } from '@/pages/AdminPanel'

function App() {
  return (
    <AuthProvider>
      <div className="min-h-screen bg-background">
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/projects" element={<Projects />} />
            <Route path="/kanban/:projectId" element={<Kanban />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="/test" element={<TestPage />} />
            <Route path="/admin" element={<AdminPanel />} />
          </Routes>
        </Layout>
        <Toaster />
      </div>
    </AuthProvider>
  )
}

export default App
