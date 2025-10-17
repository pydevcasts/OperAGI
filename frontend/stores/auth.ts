// stores/auth.ts
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(null)
  const isAuthenticated = computed(() => !!token.value)

  const login = async (email: string, password: string) => {
    const res = await $fetch('/api/v1/user/token/', {
      method: 'POST',
      body: { email, password }
    })
    token.value = res.token // فرض می‌کنیم پاسخ شامل token باشد
    localStorage.setItem('authToken', token.value)
  }

  const logout = () => {
    token.value = null
    localStorage.removeItem('authToken')
  }

  // بارگذاری توکن از localStorage در ابتدای اجرا
  if (typeof window !== 'undefined') {
    const saved = localStorage.getItem('authToken')
    if (saved) token.value = saved
  }

  return { token, isAuthenticated, login, logout }
})