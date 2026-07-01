import type { ReactNode } from 'react'
import { Navigate, Route, Routes } from 'react-router-dom'
import { Layout } from '@/components/Layout'
import { useAuth } from '@/context/AuthContext'
import { LoginPage } from '@/pages/LoginPage'
import { BriefingPage } from '@/pages/BriefingPage'
import { AnimalsListPage } from '@/pages/AnimalsListPage'
import { AnimalProfilePage } from '@/pages/AnimalProfilePage'
import { FlocksListPage } from '@/pages/FlocksListPage'
import { FlockProfilePage } from '@/pages/FlockProfilePage'
import { RecommendationsPage } from '@/pages/RecommendationsPage'

function RequireAuth({ children }: { children: ReactNode }) {
  const { user, loading } = useAuth()
  if (loading) return <div className="p-8 text-center text-muted-foreground">Loading...</div>
  if (!user) return <Navigate to="/login" replace />
  return <>{children}</>
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route
        element={
          <RequireAuth>
            <Layout />
          </RequireAuth>
        }
      >
        <Route path="/" element={<BriefingPage />} />
        <Route path="/animals" element={<AnimalsListPage />} />
        <Route path="/animals/:id" element={<AnimalProfilePage />} />
        <Route path="/flocks" element={<FlocksListPage />} />
        <Route path="/flocks/:id" element={<FlockProfilePage />} />
        <Route path="/recommendations" element={<RecommendationsPage />} />
      </Route>
    </Routes>
  )
}
