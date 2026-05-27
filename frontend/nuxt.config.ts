// nuxt.config.ts
import tailwindcss from '@tailwindcss/vite';

export default defineNuxtConfig({
  ssr: true,

  modules: [
    'nuxt-auth-utils',
    '@pinia/nuxt',
  ],

  css: [
    '~/assets/scss/tailwind.css',
    '~/assets/scss/main.scss',
  ],

  runtimeConfig: {
    // PRIVATE variables (server-side only)
    INSTAGRAM_CLIENT_ID: process.env.NUXT_INSTAGRAM_CLIENT_ID, // PRIVATE
    INSTAGRAM_CLIENT_SECRET: process.env.NUXT_INSTAGRAM_CLIENT_SECRET, // PRIVATE
    INSTAGRAM_REDIRECT_URI: process.env.NUXT_INSTAGRAM_REDIRECT_URI, // PRIVATE

    // Google OAuth variables (if used - PRIVATE)
    NUXT_OAUTH_GOOGLE_CLIENT_ID: process.env.NUXT_OAUTH_GOOGLE_CLIENT_ID,
    NUXT_OAUTH_GOOGLE_CLIENT_SECRET: process.env.NUXT_OAUTH_GOOGLE_CLIENT_SECRET,

    session: {
      password: process.env.NUXT_SESSION_PASSWORD,
      cookie: {
        httpOnly: true,
        secure: false, // در محیط production باید true باشد
        sameSite: 'lax',
        maxAge: 60 * 60 * 24 * 7,
        path: '/'
      }
    },

    // PUBLIC variables (accessible in client-side and server-side)
    public: {
      API_BASE_URL: process.env.NUXT_PUBLIC_API_BASE_URL,
      // اگر بخواهید Google Client ID را Public کنید (معمولاً توصیه نمی‌شود)
      // GOOGLE_CLIENT_ID: process.env.NUXT_PUBLIC_GOOGLE_CLIENT_ID,
    },
  },

  plugins: [
    '~/plugins/polyfill.client.ts',
    '~/plugins/authFetch.client.ts'
  ],

  vite: {
     plugins: [
          tailwindcss(),
        ],
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
