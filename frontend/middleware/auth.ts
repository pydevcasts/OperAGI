import { defineNuxtRouteMiddleware } from "nuxt/app"

// middleware/auth.ts
export default defineNuxtRouteMiddleware(async (to) => {
  const { loggedIn } = useUserSession()

  if (!loggedIn.value) {
    return navigateTo('/?login-required')
  }
  
})