// stores/auth.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRuntimeConfig } from '#imports'

// انترفیس‌ها (کامل‌تر کردم)
interface User {
  pk?: number
  email?: string
  first_name?: string
  last_name?: string
  // فیلدهای دیگر اگر نیاز داری اضافه کن
}

interface TokenResponse {
  access: string
  refresh?: string | null
  user?: User
}

export const useAuthStore = defineStore('auth', () => {
  const config = useRuntimeConfig()
  const API_BASE_URL = config.public.apiBase || 'http://127.0.0.1:8000/api/v1'

  const accessToken = ref<string | null>(null)
  const refreshToken = ref<string | null>(null)
  const user = ref<User | null>(null)
  const isAuthenticated = computed(() => !!accessToken.value)

  // بارگذاری از localStorage (قبلی)
  if (typeof window !== 'undefined') {
    setTimeout(() => {
      accessToken.value = localStorage.getItem('accessToken')
      refreshToken.value = localStorage.getItem('refreshToken')

      const storedUser = localStorage.getItem('user')
      if (storedUser) {
        try {
          user.value = JSON.parse(storedUser)
        } catch (error) {
          console.error('Error parsing stored user:', error)
        }
      }
    }, 200)
  }

  // ورود با ایمیل و رمز عبور
  const login = async (email: string, password: string) => {
    try {
      const res = await $fetch<TokenResponse>(`${API_BASE_URL}/rest-auth/login/`, {
        method: 'POST',
        body: {
          email: email.trim(),   // فقط email (چون Postman بدون login کار کرد)
          password
        },
        headers: { 'Content-Type': 'application/json' }
      })

      console.log('✅ Credentials login success from Django:', res)

      if (!res.access) {
        throw new Error('No access token received')
      }

      // ذخیره توکن‌ها در localStorage (سازگاری کد قدیمی)
      localStorage.setItem('accessToken', res.access)
      if (res.refresh) {
        localStorage.setItem('refreshToken', res.refresh)
      }

      // ذخیره کاربر (اگر برگشت)
      if (res.user) {
        user.value = res.user
        localStorage.setItem('user', JSON.stringify(res.user))
      }

      // همگام‌سازی با nuxt-auth-utils session (برای loggedIn و useUserSession)
      const session = useUserSession()
      await session.set({
        user: res.user || {
          email,
          name: `${res.user?.first_name || ''} ${res.user?.last_name || ''}`.trim() || email.split('@')[0]
        },
        tokens: {
          access: res.access,
          refresh: res.refresh
        },
        authProvider: 'credentials',
        lastLogin: new Date().toISOString()
      })

      // بروزرسانی refها
      accessToken.value = res.access
      refreshToken.value = res.refresh || null

      return res

    } catch (err: any) {
      console.error('❌ Credentials login error details:', err.data || err.message || err)
      throw err
    }
  }

  // بقیه متدها بدون تغییر (loginWithGoogle, refresh, logout)
  // ... کد قبلی شما

  return {
    accessToken,
    refreshToken,
    user,
    isAuthenticated,
    login,
    // loginWithGoogle,
    // refresh,
    // logout
  }
})