// stores/auth.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRuntimeConfig } from '#imports'

// انترفیس کاربر
interface User {
  id?: string
  name?: string
  email?: string
  image?: string
  emailVerified?: boolean
  createdAt?: string
  updatedAt?: string
}

// انترفیس‌ها
interface TokenResponse {
  access: string
  refresh?: string | null
  user?: User
}

interface GoogleAuthResponse {
  access: string
  refresh?: string | null
  user?: User
}

export const useAuthStore = defineStore('auth', () => {
  const config = useRuntimeConfig()
  const API_BASE_URL = config.public.apiBase

  const accessToken = ref<string | null>(null)
  const refreshToken = ref<string | null>(null)
  const user = ref<User | null>(null)
  const isAuthenticated = computed(() => !!accessToken.value)

  // بارگذاری از localStorage
  if (typeof window !== 'undefined') {
    accessToken.value = localStorage.getItem('accessToken')
    refreshToken.value = localStorage.getItem('refreshToken')
    
    // بارگذاری اطلاعات کاربر
    const storedUser = localStorage.getItem('user')
    if (storedUser) {
      try {
        user.value = JSON.parse(storedUser)
        console.log('✅ [Auth Store] اطلاعات کاربر از localStorage بارگذاری شد')
      } catch (error) {
        console.error('❌ [Auth Store] خطا در بارگذاری اطلاعات کاربر:', error)
      }
    }
  }

  // ورود با ایمیل و رمز
  const login = async (email: string, password: string) => {
    const res = await $fetch<TokenResponse>(`${API_BASE_URL}/user/token/`, {
      method: 'POST',
      body: { email, password }
    })

    if (!res.access) throw new Error('ورود ناموفق: توکن دریافت نشد')

    // ذخیره در استور
    accessToken.value = res.access
    refreshToken.value = res.refresh || null
    user.value = res.user || null

    // ذخیره در localStorage
    localStorage.setItem('accessToken', res.access)
    if (res.refresh) localStorage.setItem('refreshToken', res.refresh)
    if (res.user) localStorage.setItem('user', JSON.stringify(res.user))
    
    console.log('✅ [Auth Store] ورود با ایمیل موفقیت‌آمیز بود')
    
    return res
  }

  // ورود با گوگل - فقط ارسال به بک‌اند
  const loginWithGoogle = async (googleUserData: User) => {
    try {
      console.log('📤 [Auth Store] ارسال اطلاعات به بک‌اند...')
      console.log('👤 [Auth Store] اطلاعات کاربر:', googleUserData)
      
      // ارسال اطلاعات کاربر به بک‌اند
      const res = await $fetch<GoogleAuthResponse>(`${API_BASE_URL}/auth/google/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          id_token: googleUserData.id,
          email: googleUserData.email,
          name: googleUserData.name,
          picture: googleUserData.image
        })
      })

      console.log('✅ [Auth Store] پاسخ بک‌اند دریافت شد:', res)

      if (!res.access) {
        throw new Error('توکن دسترسی در پاسخ وجود ندارد')
      }

      // ذخیره در استور
      accessToken.value = res.access
      refreshToken.value = res.refresh || null
      user.value = res.user || googleUserData

      // ذخیره در localStorage
      localStorage.setItem('accessToken', res.access)
      if (res.refresh) localStorage.setItem('refreshToken', res.refresh)
      localStorage.setItem('user', JSON.stringify(user.value))

      console.log('✅ [Auth Store] اطلاعات کاربر با موفقیت ذخیره شد')
      console.log('🔑 [Auth Store] Access Token:', res.access.substring(0, 30) + '...')
      
      return res
    } catch (err: any) {
      console.error('❌ [Auth Store] خطای fetch در loginWithGoogle:', err)
      throw err
    }
  }

  // رفرش توکن
  const refresh = async () => {
    if (!refreshToken.value) throw new Error('رفرش توکن موجود نیست')

    const res = await $fetch<TokenResponse>(`${API_BASE_URL}/user/token/refresh/`, {
      method: 'POST',
      body: { refresh: refreshToken.value }
    })

    if (!res.access) throw new Error('رفرش ناموفق')

    accessToken.value = res.access
    if (res.user) {
      user.value = res.user
      localStorage.setItem('user', JSON.stringify(res.user))
    }
    localStorage.setItem('accessToken', res.access)
  }

  const logout = () => {
    accessToken.value = null
    refreshToken.value = null
    user.value = null
    
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
    localStorage.removeItem('user')
    
    console.log('✅ [Auth Store] کاربر با موفقیت خارج شد')
  }

  return { 
    accessToken, 
    refreshToken, 
    user,
    isAuthenticated, 
    login, 
    loginWithGoogle, 
    refresh, 
    logout
  }
})