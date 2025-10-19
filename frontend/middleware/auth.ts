// middleware/auth.ts
export default defineNuxtRouteMiddleware((to, from) => {
  const token = localStorage.getItem('accessToken')
  if (!token && to.path !== '/login' && to.path !== '/register') {
    return navigateTo('/login')
  }
})