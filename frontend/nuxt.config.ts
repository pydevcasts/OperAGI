export default defineNuxtConfig({
  ssr: true,

  modules: [
    'nuxt-auth-utils',
    '@pinia/nuxt',
    '@nuxtjs/tailwindcss'
  ],

  runtimeConfig: {
    // ✅ session باید مستقیم زیر runtimeConfig باشه، نه داخل public
    session: {
      password: process.env.NUXT_SESSION_PASSWORD, // حداقل ۳۲ کاراکتر
      cookie: {
        httpOnly: true,
        secure: false,
        sameSite: 'lax',
        maxAge: 60 * 60 * 24 * 7,
        path: '/'
      }
    },
    public: {
      apiBase: 'http://127.0.0.1:8000/api/v1'
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
        // ❌ '/api/_auth' رو کامل حذف کن
      }
    }
  },

  nitro: {
    compressPublicAssets: true
    // ❌ prerender برای صفحاتی که auth دارن نباشه
  }
})