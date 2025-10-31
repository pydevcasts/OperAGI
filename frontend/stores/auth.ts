// stores/auth.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref<string | null>(null)
  const refreshToken = ref<string | null>(null)
  const isAuthenticated = computed(() => !!accessToken.value)

  const login = async (email: string, password: string) => {
    const res = await $fetch('/api/v1/user/token/', {
      method: 'POST',
      body: { email, password }
    })

    // ✅ استفاده از access/refresh (نه token)
    accessToken.value = res.access
    refreshToken.value = res.refresh

    localStorage.setItem('accessToken', res.access)
    localStorage.setItem('refreshToken', res.refresh)
  }

  const logout = () => {
    accessToken.value = null
    refreshToken.value = null
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
  }

  // بارگذاری اولیه
  if (typeof window !== 'undefined') {
    accessToken.value = localStorage.getItem('accessToken')
    refreshToken.value = localStorage.getItem('refreshToken')
  }

  return { accessToken, refreshToken, isAuthenticated, login, logout }
})