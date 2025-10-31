// vite.config.ts یا vitest.config.ts
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    setupFiles: ['./vitest.setup.ts'], // ✅ این خط مهم است
    environment: 'jsdom', // ✅ برای شبیه‌سازی محیط مرورگر
  },
})