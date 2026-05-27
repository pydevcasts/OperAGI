// server/routes/auth/instagram.ts
import { sendRedirect } from 'h3'
// import { OAuth2Client } from 'google-auth-library' // توجه: این برای گوگل است، باید از کلاینت مناسب اینستاگرام استفاده کنیم.
                                                // برای اینستاگرام، بهتر است از کتابخانه‌ای مثل `passport-instagram` استفاده شود
                                                // یا مستقیماً با `ofetch` درخواست‌ها را ارسال کرد.
                                                // در این مثال، من روش مستقیم را نشان می‌دهم.

// فرض می‌کنیم این مقادیر را از متغیرهای محیطی Nuxt دریافت می‌کنید
// NUXT_PUBLIC_INSTAGRAM_CLIENT_ID
// NUXT_PUBLIC_INSTAGRAM_CLIENT_SECRET
// NUXT_INSTAGRAM_REDIRECT_URI (این نباید public باشد)

// اطلاعاتی که از Nuxt می‌گیریم (بهتر است از useRuntimeConfig استفاده کنید)
const runtimeConfig = useRuntimeConfig()
const INSTAGRAM_CLIENT_ID = runtimeConfig.public.instagramClientId
const INSTAGRAM_CLIENT_SECRET = runtimeConfig.instagramClientSecret
const INSTAGRAM_REDIRECT_URI = runtimeConfig.instagramRedirectUri // این باید در داشبورد اینستاگرام ثبت شده باشد

// URL اصلی احراز هویت اینستاگرام
const INSTAGRAM_AUTH_URL = 'https://www.instagram.com/oauth/authorize'
// URL تبادل کد با توکن
const INSTAGRAM_TOKEN_URL = 'https://api.instagram.com/oauth/access_token'
// URL دریافت اطلاعات پروفایل کاربر
const INSTAGRAM_USER_INFO_URL = 'https://graph.instagram.com/me'

export default defineEventHandler(async (event) => {
  // const query = await readQuery(event)
  const query = getQuery(event) as { code?: string; error?: string; state?: string }
  const code = query.code as string | undefined
  const error = query.error as string | undefined
  const state = query.state as string | undefined // برای امنیت، باید state را هم مدیریت کنید

  // 1. اگر خطایی در پارامترهای ورودی وجود داشت
  if (error) {
    console.error('[Instagram OAuth Error]:', error)
    return sendRedirect(event, '/login?error=instagram-failed')
  }

  // 2. اگر کد دریافت نشد، کاربر را به صفحه احراز هویت اینستاگرام هدایت کن
  if (!code) {
    // برای امنیت، یک state تصادفی تولید و ذخیره کنید (مثلاً در session)
    // const generatedState = Math.random().toString(36).substring(7)
    // await setUserSession(event, { instagramState: generatedState }) // نیاز به پیاده‌سازی setUserSession برای state

    const authUrl = `${INSTAGRAM_AUTH_URL}?client_id=${INSTAGRAM_CLIENT_ID}&redirect_uri=${INSTAGRAM_REDIRECT_URI}&scope=user_profile,user_media&response_type=code`
    // &state=${generatedState} // اضافه کردن state برای امنیت
    return sendRedirect(event, authUrl)
  }

  // 3. اگر کد دریافت شد، آن را با اینستاگرام تبادل کن تا توکن بگیری
  try {
    const tokenResponse = await $fetch(INSTAGRAM_TOKEN_URL, {
      method: 'POST',
      body: new URLSearchParams({
        client_id: INSTAGRAM_CLIENT_ID,
        client_secret: INSTAGRAM_CLIENT_SECRET,
        grant_type: 'authorization_code',
        redirect_uri: INSTAGRAM_REDIRECT_URI,
        code: code,
      }),
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      timeout: 10000
    })

    const accessToken = tokenResponse.access_token
    const userId = tokenResponse.user.id // آیدی کاربر از اینستاگرام

    if (!accessToken || !userId) {
      throw new Error('Failed to retrieve access token or user ID from Instagram.')
    }

    // 4. با استفاده از access_token، اطلاعات پروفایل کاربر را بگیر
    const userInfoResponse = await $fetch(`${INSTAGRAM_USER_INFO_URL}?fields=id,name,profile_picture,username&access_token=${accessToken}`)

    const instagramUser = {
      instagram_id: userInfoResponse.id,
      username: userInfoResponse.username,
      name: userInfoResponse.name,
      picture: userInfoResponse.profile_picture, // این URL پروفایل عکس است
      last_login: new Date().toISOString()
    }

    // 5. اطلاعات کاربر را به بک‌اند Django خود بفرست (مشابه مثال گوگل)
    // توجه: شما باید یک endpoint مشابه 'api/v1/auth/google/' برای اینستاگرام در Django داشته باشید.
    // فرض می‌کنیم آن endpoint 'api/v1/auth/instagram/' باشد.
    const djangoResponse = await $fetch('http://127.0.0.1:8000/api/v1/auth/instagram/', {
      method: 'POST',
      body: instagramUser,
      headers: { 'Content-Type': 'application/json' },
      timeout: 10000
    })

    console.log('[Django Sync Success for Instagram]:', djangoResponse)

    // 6. Session را تنظیم کن و کاربر را ریدایرکت کن
    await setUserSession(event, {
      user: {
        ...instagramUser,
        django_id: djangoResponse?.user_id || djangoResponse?.id // فرض می‌کنیم Django یک id برمی‌گرداند
      },
      tokens: djangoResponse?.tokens || {}, // فرض می‌کنیم Django توکن هم برمی‌گرداند
      authProvider: 'instagram',
      lastLogin: new Date().toISOString()
    })

    console.log('[Session set for Instagram] - redirecting to /')
    return sendRedirect(event, '/')

  } catch (err: any) {
    console.error('[Instagram OAuth Flow Error]:', err.data || err.message || err)
    // ممکن است نیاز باشد خطای دقیق‌تری را به کاربر نمایش دهید
    return sendRedirect(event, '/login?error=instagram-sync-failed')
  }
})

// ---- توابع کمکی (اگر از ماژول خاصی استفاده نمی‌کنید) ----

// تابع شبیه‌سازی شده برای دریافت توکن (باید با $fetch پیاده‌سازی شود)
// این تابع فقط نمایشی است و باید با درخواست واقعی به API اینستاگرام جایگزین شود.
async function getInstagramTokens(code: string): Promise<{ access_token: string; user: { id: string } }> {
  // این بخش نیاز به پیاده‌سازی دقیق با $fetch دارد
  // اطلاعات لازم: INSTAGRAM_CLIENT_ID, INSTAGRAM_CLIENT_SECRET, INSTAGRAM_REDIRECT_URI
  // body: new URLSearchParams({ ... })
  // headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  throw new Error("Functionality not implemented: Replace with actual $fetch call to Instagram token endpoint.")
}

// تابع شبیه‌سازی شده برای دریافت اطلاعات کاربر
async function getInstagramUserInfo(accessToken: string): Promise<{ id: string; username: string; name: string; profile_picture: string }> {
  // این بخش نیز نیاز به پیاده‌سازی دقیق با $fetch دارد
  // URL: `https://graph.instagram.com/me?fields=id,name,profile_picture,username&access_token=${accessToken}`
  throw new Error("Functionality not implemented: Replace with actual $fetch call to Instagram user info endpoint.")
}

// تابع شبیه‌سازی شده برای تنظیم Session (اگر از Nuxt Auth استفاده نمی‌کنید)
async function setUserSession(event: any, data: any) {
  // این تابع باید Session کاربر را در سرور Nuxt شما مدیریت کند
  // یا از طریق کوکی‌ها، یا یک سیستم session دیگر.
  // اگر از `@sidebase/nuxt-auth` استفاده می‌کنید، این تابع توسط آن ارائه می‌شود.
  console.log("Simulating setUserSession:", data);
  // event.context.session = data; // این فقط یک مثال ساده است
  // شما باید این را با منطق مدیریت session خود جایگزین کنید
}

// یک تابع mock برای useRuntimeConfig برای تست
function useRuntimeConfig() {
  return {
    public: {
      instagramClientId: process.env.NUXT_PUBLIC_INSTAGRAM_CLIENT_ID || 'YOUR_INSTAGRAM_CLIENT_ID',
    },
    instagramClientSecret: process.env.NUXT_INSTAGRAM_CLIENT_SECRET || 'YOUR_INSTAGRAM_CLIENT_SECRET',
    instagramRedirectUri: process.env.NUXT_INSTAGRAM_REDIRECT_URI || 'http://localhost:3000/auth/instagram' // اطمینان حاصل کنید که این URI در اینستاگرام ثبت شده است
  }
}
