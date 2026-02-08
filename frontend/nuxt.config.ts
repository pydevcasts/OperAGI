// https://nuxt.com/docs/api/configuration/nuxt-config
import { defineNuxtConfig } from 'nuxt/config'

export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  ssr: false,
  modules: ['@nuxtjs/tailwindcss', '@pinia/nuxt'],

  runtimeConfig: {
    betterAuthSecret: '',
    googleClientSecret: '',
    public: {
      betterAuthUrl: 'http://localhost:3000',
      googleOAuthClientId: '',
      apiBase: 'http://127.0.0.1:8000/api/v1'
    }
  },

  // حذف vite.config.ts و استفاده از اینجا
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
  },
  
  // اضافه کردن externals برای better-auth
  nitro: {
    externals: {
      inline: ['better-auth']
    }
  }
})