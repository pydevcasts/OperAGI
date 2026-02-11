<!-- components/GoogleLoginButton.vue -->
<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'

// اگر نیاز به popup داری، از useUserSession استفاده کن (auto-import شده)
const { openInPopup } = useUserSession()  // ← بدون import!

const googleLogin = () => {
  openInPopup('/auth/google', { width: 500, height: 600 })
  // اگر popup نمی‌خوای: navigateTo('/auth/google')
}

// پاک کردن لاگ‌ها هنگام آن‌مونت (اختیاری)
onUnmounted(() => {
  console.log('Component unmounted')
})
</script>

<template>
  <button
    @click="googleLogin"
    class="w-full bg-red-600 hover:bg-red-700 text-white font-bold py-3 px-4 rounded-lg transition duration-200 shadow-md hover:shadow-lg flex items-center justify-center gap-2"
  >
    <!-- SVG گوگل که داری -->
    <svg class="w-5 h-5" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
      <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4" />
      <!-- بقیه pathها بدون تغییر -->
    </svg>
    ورود با گوگل
  </button>
</template>