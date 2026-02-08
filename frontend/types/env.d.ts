declare namespace NodeJS {
  interface ProcessEnv {
    // متغیرهای بدون پیشوند (معمولاً برای سرور-side)
    BETTER_AUTH_URL?: string
    BETTER_AUTH_SECRET?: string
    GOOGLE_CLIENT_ID?: string
    GOOGLE_CLIENT_SECRET?: string

    // متغیرهای فرانت‌اند (Vite/Nuxt) – با پیشوند VITE_
    VITE_GOOGLE_OAUTH_CLIENT_ID?: string
    VITE_GOOGLE_CLIENT_SECRET?: string
    VITE_BETTER_AUTH_SECRET?: string
    VITE_BETTER_AUTH_URL?: string
    VITE_API_BASE_URL?: string

    // اگر متغیرهای دیگری در .env داری (مثلاً OpenAI یا چیزهای دیگر)، اینجا اضافه کن
    // مثال:
    // OPENAI_API_KEY?: string
    // NODE_ENV?: "development" | "production" | "test"
  }
}