import { createContext, useContext, useEffect, useState, type ReactNode } from 'react'
import { apiClient, getToken, setToken as persistToken } from '@/api/client'

// Chapter 17 (Security): every user authenticates individually
// (RULE-SEC-103) - no shared/anonymous device login.
export type UserRole = 'owner' | 'manager' | 'worker' | 'veterinarian' | 'finance' | 'read_only'

export interface CurrentUser {
  id: string
  farm_id: string
  email: string
  full_name: string
  role: UserRole
  active: boolean
}

interface AuthState {
  user: CurrentUser | null
  loading: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthState | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<CurrentUser | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = getToken()
    if (!token) {
      setLoading(false)
      return
    }
    apiClient
      .get<CurrentUser>('/auth/me')
      .then((res) => setUser(res.data))
      .catch(() => persistToken(null))
      .finally(() => setLoading(false))
  }, [])

  async function login(email: string, password: string) {
    const form = new URLSearchParams()
    form.set('username', email)
    form.set('password', password)
    const res = await apiClient.post('/auth/login', form, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })
    persistToken(res.data.access_token)
    setUser(res.data.user)
  }

  function logout() {
    persistToken(null)
    setUser(null)
  }

  return <AuthContext.Provider value={{ user, loading, login, logout }}>{children}</AuthContext.Provider>
}

export function useAuth(): AuthState {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
