// vite.config.ts یا vitest.config.ts
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    setupFiles: ['./vitest.setup.ts'], // ✅ این خط مهم است
    environment: 'jsdom', // ✅ برای شبیه‌سازی محیط مرورگر
  },
  server: {
    headers: {
      // 'Cross-Origin-Opener-Policy': 'same-origin',
      'Cross-Origin-Embedder-Policy': 'require-corp',
      'Cross-Origin-Opener-Policy': 'unsafe-none',
    },
  },
})


