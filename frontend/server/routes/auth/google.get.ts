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

    const googleUser = {
      google_id: user.sub,
      email: user.email,
      name: user.name || `${user.given_name || ''} ${user.family_name || ''}`.trim(),
      picture: user.picture,
      email_verified: user.email_verified,
      last_login: new Date().toISOString()
    }

    try {
      const djangoResponse = await $fetch('http://127.0.0.1:8000/api/v1/auth/google/', {
        method: 'POST',
        body: googleUser,
        headers: { 'Content-Type': 'application/json' },
        timeout: 10000
      })

      console.log('[Django Sync Success for Google]:', djangoResponse)

      await setUserSession(event, {
        user: {
          ...googleUser,
          django_id: djangoResponse?.user_id || djangoResponse?.id
        },
        tokens: djangoResponse?.tokens || {},
        authProvider: 'google',
        lastLogin: new Date().toISOString()
      })

      console.log('[Session set for Google] - redirecting to /')
    } catch (err: any) {
      console.error('[Django Sync Error for Google]:', err.data || err.message || err)
    }

    return sendRedirect(event, '/')  // ← به صفحه اصلی ریدایرکت می‌شه
  },

  onError(event, error) {
    console.error('[Google OAuth Error]:', error)
    return sendRedirect(event, '/login?error=google-failed')
  }
})