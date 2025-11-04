// stores/auth.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/v1'

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref<string | null>(null)
  const refreshToken = ref<string | null>(null)
  const isAuthenticated = computed(() => !!accessToken.value)

  // بارگذاری از localStorage
  if (typeof window !== 'undefined') {
    accessToken.value = localStorage.getItem('accessToken')
    refreshToken.value = localStorage.getItem('refreshToken')
  }

  // ورود با ایمیل و رمز
  const login = async (email: string, password: string) => {
    const res = await $fetch(`${API_BASE_URL}/user/token/`, {
      method: 'POST',
      body: { email, password }
    })

    if (!res.access) throw new Error('ورود ناموفق: توکن دریافت نشد')

    accessToken.value = res.access
    refreshToken.value = res.refresh || null

    localStorage.setItem('accessToken', res.access)
    if (res.refresh) localStorage.setItem('refreshToken', res.refresh)
  }

  // ورود با گوگل (در GoogleLoginButton انجام میشه)
  const loginWithGoogle = async (idToken: string) => {
    const res = await $fetch(`${API_BASE_URL}/user/auth/google/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: { id_token: idToken }
    })

    if (!res.access_token) throw new Error('ورود با گوگل ناموفق')

    accessToken.value = res.access_token
    refreshToken.value = res.refresh_token || null

    localStorage.setItem('accessToken', res.access_token)
    if (res.refresh_token) localStorage.setItem('refreshToken', res.refresh_token)
  }

  // رفرش توکن
  const refresh = async () => {
    if (!refreshToken.value) throw new Error('رفرش توکن موجود نیست')

    const res = await $fetch(`${API_BASE_URL}/user/token/refresh/`, {
      method: 'POST',
      body: { refresh: refreshToken.value }
    })

    if (!res.access) throw new Error('رفرش ناموفق')

    accessToken.value = res.access
    localStorage.setItem('accessToken', res.access)
  }

  const logout = () => {
    accessToken.value = null
    refreshToken.value = null
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
  }

  return { accessToken, refreshToken, isAuthenticated, login, loginWithGoogle, refresh, logout }
})