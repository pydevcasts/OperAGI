// types/nuxt.d.ts
import type { H3Event } from 'h3'
import type { Ref, ComputedRef } from 'vue'

declare global {
  // Vue core
  const ref: typeof import('vue')['ref']
  const computed: typeof import('vue')['computed']
  const useRoute: typeof import('vue-router')['useRoute']

  // Nuxt auto-imports
  const defineNuxtPlugin: typeof import('#app')['defineNuxtPlugin']
  const defineEventHandler: typeof import('h3')['defineEventHandler']
  const createError: typeof import('h3')['createError']
  const readBody: typeof import('h3')['readBody']
  const setUserSession: typeof import('#auth-utils')['setUserSession']
  const navigateTo: typeof import('#app')['navigateTo']
  const $fetch: typeof import('ofetch')['$fetch']
  const useRuntimeConfig: typeof import('#app')['useRuntimeConfig'] 
  
  export function useUserSession(): {
    loggedIn: ComputedRef<boolean>
    user: ComputedRef<any>
    session: Ref<any>
    fetch: () => Promise<void>
    clear: () => Promise<void>
    ready: ComputedRef<boolean>
  }
}

export {}