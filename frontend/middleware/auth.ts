export default defineNuxtRouteMiddleware(async (to, from) => {
  const authStore = useAuthStore()
  const token = authStore.accessToken

  if (!token) return navigateTo('/login')

  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    if (payload.exp * 1000 < Date.now()) {
      await authStore.refresh()
    }
  } catch {
    return navigateTo('/login')
  }
})