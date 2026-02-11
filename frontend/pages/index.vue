<!-- #pages/index.vue  -->
<script setup lang="ts">
const { loggedIn, user, session, fetch, clear } = useUserSession()

// اگر نیاز به refresh دستی داری (معمولاً اتوماتیک fetch می‌شه)
onMounted(() => {
  fetch() // مطمئن شو session لود شده
})
</script>

<template>
  <div>
    <div v-if="loggedIn">
      <h1>خوش آمدی {{ user?.name }}!</h1>
      <img v-if="user?.picture" :src="user.picture" alt="Profile" width="100" />
      <p>ایمیل: {{ user?.email }}</p>
      <button @click="clear()">خروج</button>
    </div>

    <div v-else>
      <a href="/auth/google">ورود با حساب گوگل</a>
      <!-- یا اگر می‌خوای popup باز کنه: -->
      <!-- <button @click="openInPopup('/auth/google')">ورود با گوگل (popup)</button> -->
    </div>

    <!-- برای نمایش وضعیت لودینگ یا خطا -->
    <p v-if="!loggedIn && session.status === 'loading'">در حال بارگذاری...</p>
  </div>
</template>