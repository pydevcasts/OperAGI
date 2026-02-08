// middleware/auth.ts
export default defineNuxtRouteMiddleware(async (to, from) => {
  const authStore = await import('~/stores/auth').then(m => m.useAuthStore())
  
  try {
    // بررسی احراز هویت
    if (!authStore.isAuthenticated && to.path !== '/login' && to.path !== '/login/callback') {
      console.log('User not authenticated, redirecting to login')
      return navigateTo('/login')
    }
    
    // اگر کاربر لاگین است و به صفحه لاگین می‌رود
    if (authStore.isAuthenticated && (to.path === '/login' || to.path === '/login/callback')) {
      console.log('User already authenticated, redirecting to home')
      return navigateTo('/')
    }
  } catch (error) {
    console.error('Auth middleware error:', error)
    if (to.path !== '/login' && to.path !== '/login/callback') {
      return navigateTo('/login')
    }
  }
})