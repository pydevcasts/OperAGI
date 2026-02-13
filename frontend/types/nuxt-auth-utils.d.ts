// types/nuxt-auth-utils.d.ts
declare module '#auth-utils' {
  export * from 'nuxt-auth-utils'
}

declare module 'nuxt-auth-utils' {
  // اگر نیاز به declare خاص داری
  export const useUserSession: () => any // یا نوع دقیق‌تر
}