<!-- pages/logout.vue -->
<script setup lang="ts">
import { useUserSession } from 'nuxt-auth-utils'

onMounted(async () => {
  const session = useUserSession()

  // ۱. پاک کردن session Nuxt
  await session.clear()
  console.log('Nuxt session cleared')

  // ۲. پاک کردن localStorage (اگر استفاده می‌کنید)
  if (typeof window !== 'undefined') {
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
    localStorage.removeItem('user')
  }

  // ۳. ریدایرکت به logout گوگل (برای revoke session گوگل)
  const googleLogoutUrl = 'https://accounts.google.com/Logout?continue=' + encodeURIComponent('http://localhost:3000/login')

  console.log('Redirecting to Google logout...')
  window.location.href = googleLogoutUrl
})
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-900 text-white">
    <p>در حال خروج... لطفاً صبر کنید</p>
  </div>
</template>