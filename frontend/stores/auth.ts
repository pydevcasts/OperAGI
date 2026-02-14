// stores/auth.ts
import { defineStore } from 'pinia'
import { ref, computed, watch, onMounted } from 'vue'
import { useUserSession } from '#imports'

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
  // وضعیت محلی (فقط برای UI)
  const accessToken = ref<string | null>(null)
  const refreshToken = ref<string | null>(null)
  const user = ref<User | null>(null)

  const isAuthenticated = computed(() => !!accessToken.value)

  // همگام‌سازی خودکار با session سمت سرور
  const syncWithSession = () => {
    const session = useUserSession()

    const updateFromSession = () => {
      const s = session.value
      if (s?.user && s.tokens?.access) {
        accessToken.value = s.tokens.access
        refreshToken.value = s.tokens.refresh || null
        user.value = s.user as User
      } else {
        // لاگ‌آوت: پاک کردن وضعیت
        accessToken.value = null
        refreshToken.value = null
        user.value = null
      }
    }

    // اولین بار: بروزرسانی فوری
    updateFromSession()

    // هر بار که session تغییر کند، وضعیت Pinia بروز شود
    watch(
      () => session.value,
      () => updateFromSession(),
      { deep: true, immediate: false }
    )
  }

  // فراخوانی همگام‌سازی در صورتی که در محیط کلاینت باشیم
  if (typeof window !== 'undefined') {
    onMounted(() => {
      syncWithSession()
    })
  } else {
    // در SSR، مستقیماً همگام‌سازی کن (چون onMounted اجرا نمی‌شود)
    syncWithSession()
  }

  // متد لاگین (فقط فراخوانی API — همگام‌سازی خودکار است)
  const login = async (email: string, password: string) => {
    const res = await $fetch('/api/auth/login', {
      method: 'POST',
      body: { email: email.trim(), password }
    })

    // بعد از لاگین، session خودکار fetch و همگام می‌شود
    // نیازی به دستکاری دستی نیست
    return res
  }

  // مثال: logout (در صورت نیاز)
  const logout = async () => {
    await $fetch('/api/auth/logout', { method: 'POST' })
    // session.clear() معمولاً در سرور انجام می‌شود
    // ولی برای اطمینان، session را دوباره fetch می‌کنیم
    const session = useUserSession()
    await session.clear()
    // همگام‌سازی خودکار از طریق watch انجام می‌شود
  }

  return {
    // state
    accessToken,
    refreshToken,
    user,
    isAuthenticated,

    // actions
    login,
    logout
    // سایر متدها (مثل refresh token) را اینجا اضافه کنید
  }
})