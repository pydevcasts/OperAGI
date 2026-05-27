<script setup lang="ts">
import { onUnmounted } from 'vue'

// تابعی که به سمت مسیر احراز هویت یوتیوب هدایت می‌کند
const youtubeLogin = () => {
  console.log('Redirecting to /auth/youtube')
  // فرض می‌کنیم مسیر احراز هویت یوتیوب در بک‌اند شما '/auth/youtube' است
  window.location.href = '/auth/youtube'
}

// Unmount log (برای دیباگ کردن)
onUnmounted(() => {
  console.log('YouTube button component unmounted')
})
</script>

<template>
  <button
    @click="youtubeLogin"
    class="youtube-btn" type="button"
  >
    <!-- YouTube SVG Icon -->
    <!-- این SVG را می‌توانید از منابع معتبر آیکون یوتیوب دریافت کنید -->
 <svg width="24" height="24" viewBox="0 0 24 24" fill="#FF0000" xmlns="http://www.w3.org/2000/svg">
  <path d="M22.45 7.45C22.04 5.79 20.81 4.56 19.15 4.15C17.34 3.74 11.99 3.74 11.99 3.74C11.99 3.74 7.25 3.74 5.44 4.15C3.78 4.56 2.55 5.79 2.14 7.45C1.73 9.26 1.73 11.99 1.73 11.99C1.73 11.99 1.73 14.73 2.14 16.54C2.55 18.2 3.78 19.43 5.44 19.85C7.25 20.26 11.99 20.26 11.99 20.26C11.99 20.26 17.34 20.26 19.15 19.85C20.81 19.43 22.04 18.2 22.45 16.54C22.87 14.73 22.87 11.99 22.87 11.99C22.87 11.99 22.87 9.26 22.45 7.45ZM9.49 15.04V8.959L14.95 11.99L9.49 15.04Z"/>
</svg>


  </button>
</template>
