// middleware/guest.ts
import { defineNuxtRouteMiddleware } from "nuxt/app"


export default defineNuxtRouteMiddleware((to) => {
  const { loggedIn } = useUserSession()
  
  if (import.meta.server) return // ← در SSR چک نکن
  if (loggedIn.value && to.path !== '/') {
    return navigateTo('/')
  }
})