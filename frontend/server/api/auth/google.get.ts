// server/routes/auth/google.get.ts
import { sendRedirect } from 'h3'

export default defineOAuthGoogleEventHandler({
  config: {
    emailRequired: true, // اگر ایمیل نداشته باشه، error می‌ده
    scope: ['openid', 'email', 'profile'] // پیش‌فرض خوبه، اما صریح بهتره
  },

  async onSuccess(event, { user, tokens }) {
    console.log('[Google OAuth Success] User:', user)
    console.log('[Google OAuth] Tokens received:', !!tokens.access_token)

    // ذخیره session (فقط داده‌های ضروری)
    await setUserSession(event, {
      user: {
        id: user.sub || user.id, // Google از sub استفاده می‌کنه
        email: user.email,
        name: user.name,
        picture: user.picture,
        // اگر نیاز به refresh token داری (برای API گوگل):
        // googleAccessToken: tokens.access_token,
        // googleRefreshToken: tokens.refresh_token
      },
      authProvider: 'google',
      lastLogin: new Date().toISOString()
    })

    // اگر می‌خوای به Django sync کنی (اختیاری):
    // await $fetch('http://127.0.0.1:8000/api/v1/sync-google-user', {
    //   method: 'POST',
    //   body: { googleId: user.sub, email: user.email, name: user.name }
    // })

    return sendRedirect(event, '/') // یا '/' یا هر صفحه‌ای
  },

  onError(event, error) {
    console.error('[Google OAuth Error]:', error.message || error)
    return sendRedirect(event, '/login?error=google-failed')
  }
})