// types/nuxt.d.ts
import type { H3Event } from 'h3'

declare global {
  // Nuxt auto-imports پایه
  const defineNuxtPlugin: typeof import('#app')['defineNuxtPlugin']
  const defineEventHandler: typeof import('h3')['defineEventHandler']
  const createError: typeof import('h3')['createError']
  const readBody: typeof import('h3')['readBody']
  const setUserSession: typeof import('#auth-utils')['setUserSession']
  const navigateTo: typeof import('#app')['navigateTo']

  // $fetch رو اینجا declare کن (این خط قرمز رو برمی‌داره)
  const $fetch: typeof import('ofetch')['$fetch']

  // declare قبلی برای useUserSession (که کار کرد)
  export function useUserSession(): {
    loggedIn: import('vue').ComputedRef<boolean>
    user: import('vue').ComputedRef<User | null>     // اگر augmentation User داری
    session: import('vue').Ref<UserSession>          // اگر augmentation UserSession داری
    fetch: () => Promise<void>
    clear: () => Promise<void>
    ready: import('vue').ComputedRef<boolean>
  }
}

export {}