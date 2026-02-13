// server/routes/auth/google.get.ts
import { sendRedirect } from 'h3'

export default defineOAuthGoogleEventHandler({
  config: {
    emailRequired: true,
    scope: ['openid', 'email', 'profile']
  },

  async onSuccess(event, { user, tokens }) {
    console.log('[Google OAuth Success] User:', user)
    console.log('[Google OAuth] Tokens received:', !!tokens.access_token)

    // ۱. اطلاعات کاربر از گوگل
    const googleUser = {
      google_id: user.sub,          // unique ID گوگل (sub)
      email: user.email,
      name: user.name || `${user.given_name || ''} ${user.family_name || ''}`.trim(),
      picture: user.picture,
      email_verified: user.email_verified,
      last_login: new Date().toISOString()
    }

    try {
      // ۲. ارسال به Django API برای ذخیره/به‌روزرسانی کاربر
      const djangoResponse = await $fetch('http://127.0.0.1:8000/api/v1/auth/google/', {
        method: 'POST',
        body: googleUser,
        headers: {
          'Content-Type': 'application/json',
        },
        timeout: 10000  // ۱۰ ثانیه تایم‌اوت
      })

      console.log('[Django Sync Success]:', djangoResponse)

      // ۳. می‌تونی ID کاربر از Django رو در session ذخیره کنی (اختیاری)
      await setUserSession(event, {
  user: {
    ...googleUser,
    django_id: djangoResponse?.user_id || djangoResponse?.id
  },
  tokens: djangoResponse?.tokens || {}, // اگر Django توکن برگردوند
  authProvider: 'google',
  lastLogin: new Date().toISOString()
})

    } catch (err: any) {
      console.error('[Django Sync Error]:', err.data || err.message || err)
    }

    // ۴. redirect به داشبورد یا صفحه اصلی
    return sendRedirect(event, '/dashboard')  // یا '/' اگر صفحه dashboard هنوز نساختی
  },

  onError(event, error) {
    console.error('[Google OAuth Error]:', error)
    return sendRedirect(event, '/login?error=google-failed')
  }
})