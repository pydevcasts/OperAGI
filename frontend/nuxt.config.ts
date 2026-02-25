import tailwindcss from '@tailwindcss/vite'

export default defineNuxtConfig({
  ssr: true,

  modules: [
    'nuxt-auth-utils',
    '@pinia/nuxt',
    // ❌ @nuxtjs/tailwindcss حذف شد
  ],

  css: [
  '~/assets/scss/tailwind.css',  // ✅ Tailwind — فایل CSS خالص
  '~/assets/scss/main.scss',     // ✅ SCSS — متغیرها + استایل‌های صفحات
],

  runtimeConfig: {
    session: {
      password: process.env.NUXT_SESSION_PASSWORD,
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
    plugins: [tailwindcss()], // ✅ اینجا فقط plugins
    server: {
      proxy: {
        '/api/v1': {
          target: 'http://127.0.0.1:8000',
          changeOrigin: true,
          rewrite: (path: string) => path.replace(/^\/api\/v1/, '')
        }
      }
    }
  },

  nitro: {
    compressPublicAssets: true
  }
})