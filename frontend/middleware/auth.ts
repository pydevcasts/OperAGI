
// middleware/auth.ts
export default defineNuxtRouteMiddleware(() => {
  const token = localStorage.getItem('accessToken')
  if (!token) {
    return navigateTo('/login')
  }
})