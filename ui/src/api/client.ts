import axios from 'axios'

// Chapter 15 (API Architecture): one base client, consistent error
// envelope handling (§15.6), bearer auth (Ch.17 §17.5).
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
})

const TOKEN_KEY = 'farmos_token'

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY)
}

export function setToken(token: string | null) {
  if (token) localStorage.setItem(TOKEN_KEY, token)
  else localStorage.removeItem(TOKEN_KEY)
}

apiClient.interceptors.request.use((config) => {
  const token = getToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export interface ApiErrorShape {
  error: { code: string; message: string; field_errors?: unknown }
}

export function extractErrorMessage(err: unknown): string {
  if (axios.isAxiosError(err)) {
    const data = err.response?.data as ApiErrorShape | undefined
    if (data?.error?.message) return data.error.message
    return err.message
  }
  return 'Something went wrong.'
}
