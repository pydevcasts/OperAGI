export default defineNuxtConfig({
  // ssr: false,  ← این را حذف یا کامنت کن
  ssr: true,     // ← این را اضافه کن یا true کن

  modules: ['nuxt-auth-utils', '@pinia/nuxt', '@nuxtjs/tailwindcss'],

  runtimeConfig: {
    public: {
      apiBase: 'http://127.0.0.1:8000/api/v1'
    },
    session: {
      cookie: {
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'lax',
        maxAge: 60 * 60 * 24 * 7 // ۷ روز
      }
    }
  },

  vite: {
    server: {
      proxy: {
        '/api/v1': {
          target: 'http://127.0.0.1:8000',
          changeOrigin: true,
          rewrite: path => path.replace(/^\/api\/v1/, '')
        }
      }
    }
  }
})