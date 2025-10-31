<!-- pages/login.vue -->
<script setup lang="ts">
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const error = ref('')
const authStore = useAuthStore()
const router = useRouter()

const handleLogin = async () => {
  console.log("کلیک روی دکمه ورود"); // لاگ کلیک
  error.value = ''; // پاک کردن خطا قبلی
  try {
    console.log("فراخوانی authStore.login"); // لاگ فراخوانی
    await authStore.login(email.value, password.value)
    console.log("ورود موفقیت‌آمیز، هدایت به صفحه اصلی"); // لاگ موفقیت
    router.push('/')
  } catch (err) {
    console.error("خطا در handleLogin:", err); // لاگ خطا در handleLogin
    // نمایش خطا به کاربر
    error.value = 'ورود ناموفق بود. لطفاً اطلاعات را بررسی کنید.';
    // یا نمایش پیام خطا از سمت سرور اگر در دسترس باشد
    // error.value = err.message || 'ورود ناموفق بود.';
  }
}
</script>

<!-- pages/login.vue -->
<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-900">
    <form class="bg-gray-800 p-8 rounded shadow w-full max-w-md">
      <h2 class="text-2xl font-bold mb-6 text-center text-white">Sign in to Operagi</h2>

      <GoogleLoginButton />

      <div class="mt-6 text-center text-gray-400">
        Or sign in with email
      </div>

      <!-- فرم ایمیل و رمز -->
      <input
        v-model="email"
        type="email"
        placeholder="Email"
        class="w-full p-3 mb-4 rounded bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500"
        required
      />
      <input
        v-model="password"
        type="password"
        placeholder="Password"
        class="w-full p-3 mb-4 rounded bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500"
        required
      />
      <button
        type="submit"
        class="w-full bg-indigo-600 hover:bg-indigo-700 text-white py-3 rounded font-medium transition duration-200"
      >
        Sign In
      </button>
      <p v-if="error" class="mt-4 text-red-400 text-center">{{ error }}</p>
    </form>
  </div>
</template>