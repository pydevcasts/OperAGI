// server/utils/auth.ts
import { betterAuth } from "better-auth"
import { useRuntimeConfig } from "#imports"
import { readBody } from "h3"

// سینگلتون: فقط یک بار ایجاد می‌شود
let authInstance: ReturnType<typeof betterAuth> | null = null

export function getAuth() {
  if (authInstance) {
    return authInstance
  }

  const config = useRuntimeConfig()

  const googleClientId = config.public.googleOAuthClientId || '789229636175-bu1825lmonjksmamece8o31g2injdmu6.apps.googleusercontent.com'
  const googleClientSecret = config.googleClientSecret || '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'
  const betterAuthSecret = config.betterAuthSecret || 'TELYwzIqb26qJKbWR1MD47eHdduN22AQ'

  console.log('=== Creating Better Auth Instance ===')
  console.log('Base URL:', config.public.betterAuthUrl)
  console.log('Google Client ID:', googleClientId)
  console.log('Google Client Secret exists:', !!googleClientSecret)
  console.log('Better Auth Secret exists:', !!betterAuthSecret)
  console.log('⚠️ Email/Password login is DISABLED')
  console.log('======================================')

  // ✅ غیرفعال کردن کامل ورود با ایمیل/رمز
  authInstance = betterAuth({
    baseURL: config.public.betterAuthUrl,
    secret: betterAuthSecret,
    
    // ❌ غیرفعال کردن ورود با ایمیل/رمز
    emailAndPassword: {
      enabled: false  // ✅ این خط مشکل را حل می‌کند
    },
    
    socialProviders: {
      google: {
        clientId: googleClientId,
        clientSecret: googleClientSecret,
        prompt: "select_account",
        accessType: "offline"
      }
    },
    
    // تنظیمات جلسه
    session: {
      cookieName: 'better-auth.session_token',
      expiresIn: 604800 // 7 روز
    },
    
    // ✅ تنظیم صفحه کالبک پیش‌فرض
    callbacks: {
      async signIn({ user, account }) {
        console.log('✅ [Better Auth] User signed in:', user)
        return true
      }
    }
  })

  return authInstance
}

// تابع برای ایجاد درخواست سازگار با Fetch API
export async function createFetchRequest(event: any) {
  const config = useRuntimeConfig()
  
  const method = event.node.req.method || 'GET'
  let body = null
  
  if (method !== 'GET' && method !== 'HEAD') {
    try {
      body = await readBody(event)
    } catch (error) {
      console.error('Error reading body:', error)
    }
  }

  return {
    url: new URL(event.node.req.url || '/', config.public.betterAuthUrl).toString(),
    method: method,
    headers: new Headers(event.node.req.headers as Record<string, string>),
    body: body ? JSON.stringify(body) : null,
    
    async json() {
      return body
    },
    
    async text() {
      return body ? JSON.stringify(body) : ''
    },
    
    clone() {
      return this
    }
  }
}