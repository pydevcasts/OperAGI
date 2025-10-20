// stores/auth.spec.ts
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useAuthStore } from './auth'

// Mock کردن $fetch
const mockFetch = vi.fn()
vi.stubGlobal('$fetch', mockFetch)

describe('Auth Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.clear()
    mockFetch.mockClear()
  })

  it('should login successfully and store tokens', async () => {
    const mockResponse = {
      access: 'mock-access-token',
      refresh: 'mock-refresh-token'
    }
    mockFetch.mockResolvedValue(mockResponse)

    const store = useAuthStore()

    await store.login('user@example.com', 'password123')

    expect(mockFetch).toHaveBeenCalledWith('/api/v1/user/token/', {
      method: 'POST',
      body: { email: 'user@example.com', password: 'password123' }
    })

    expect(store.accessToken).toBe('mock-access-token')
    expect(store.refreshToken).toBe('mock-refresh-token')
    expect(store.isAuthenticated).toBe(true)

    expect(localStorage.getItem('accessToken')).toBe('mock-access-token')
    expect(localStorage.getItem('refreshToken')).toBe('mock-refresh-token')
  })

  it('should logout and clear tokens', () => {
    const store = useAuthStore()
    store.accessToken = 'old-token'
    store.refreshToken = 'old-refresh'
    localStorage.setItem('accessToken', 'old-token')
    localStorage.setItem('refreshToken', 'old-refresh')

    store.logout()

    expect(store.accessToken).toBeNull()
    expect(store.refreshToken).toBeNull()
    expect(store.isAuthenticated).toBe(false)
    expect(localStorage.getItem('accessToken')).toBeNull()
    expect(localStorage.getItem('refreshToken')).toBeNull()
  })
})