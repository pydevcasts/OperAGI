
// middleware/auth.ts
import { defineNuxtRouteMiddleware } from "nuxt/app"


export default defineNuxtRouteMiddleware((to) => {
  const { loggedIn, user  } = useUserSession()
  
  if (import.meta.server) return // ← در SSR چک نکن
  if (!loggedIn.value && to.path !== '/login') {
    return navigateTo('/login')
  }
   // اگه ایمیل تأیید نشده
  if (!(user.value as any)?.is_email_verified) {
    return navigateTo('/email-not-verified')
  }
})
