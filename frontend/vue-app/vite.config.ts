import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  root: './', // اطمینان حاصل کنید که این مسیر به دایرکتوری حاوی index.html اشاره می‌کند
  build: {
    outDir: 'dist', // دایرکتوری خروجی برای ساخت
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
})
