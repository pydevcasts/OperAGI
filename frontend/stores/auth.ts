// stores/auth.ts
import { navigateTo } from 'nuxt/app'
import { defineStore } from 'pinia'
import { computed } from 'vue'

interface User {
  pk?: number
  email?: string
  first_name?: string
  last_name?: string
  name?: string
  picture?: string
  django_id?: number
  [key: string]: any
}


export const useAuthStore = defineStore('auth', () => {
  const { user: sessionUser, loggedIn, fetch: refreshSession , clear } = useUserSession()

  // ── State (computed از session) ──────────────────────────
  const user = computed<User | null>(() => sessionUser.value as User | null)
  const accessToken = computed<string | null>(() => (sessionUser.value as any)?.tokens?.access ?? null)
  const refreshToken = computed<string | null>(() => (sessionUser.value as any)?.tokens?.refresh ?? null)
  const isAuthenticated = computed(() => loggedIn.value)

  // ── Actions ──────────────────────────────────────────────
  const login = async (email: string, password: string) => {
    await $fetch('/api/auth/login', {
      method: 'POST',
      body: { email: email.trim(), password }
    })

    // بعد از لاگین session را sync کن تا Vue DevTools هم نشون بده
    await refreshSession ()
  }
  const logout = async () => {
    await clear()
    await navigateTo('/login')
  }


  return {
    // state
    user,
    accessToken,
    refreshToken,
    isAuthenticated,

    // actions
    login,
    logout,
    refreshSession
  }
})