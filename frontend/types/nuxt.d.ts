// types/nuxt.d.ts
import type { H3Event } from 'h3'

declare global {
  // Nuxt auto-imports
  const defineNuxtPlugin: typeof import('#app')['defineNuxtPlugin']
  const defineEventHandler: typeof import('h3')['defineEventHandler']
  const createError: typeof import('h3')['createError']
  const readBody: typeof import('h3')['readBody']
  const setUserSession: typeof import('#auth-utils')['setUserSession']
  const navigateTo: typeof import('#app')['navigateTo']
  const $fetch: typeof import('ofetch')['$fetch']
}

export {}