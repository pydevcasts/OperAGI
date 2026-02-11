<!-- pages/login.vue -->
<script setup lang="ts">
import GoogleLoginButton from '~/components/GoogleLoginButton.vue'

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const handleLogin = async (e: Event) => {
  e.preventDefault()
  error.value = ''
  loading.value = true

  try {
    const response = await $fetch('/api/auth/login', {
      method: 'POST',
      body: { email: email.value, password: password.value }
    })
    // اگر موفق بود، redirect
    await navigateTo('/')
  } catch (err: any) {
    error.value = err.data?.message || 'ورود ناموفق بود'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 to-indigo-900 px-4">
    <div class="w-full max-w-md">
      <!-- ... هدر و استایل‌ها ... -->

      <form @submit="handleLogin" class="space-y-6">
        <GoogleLoginButton />

        <div class="relative my-6"> <!-- خط یا --> </div>

        <input v-model="email" type="email" placeholder="ایمیل" required class="..." />
        <input v-model="password" type="password" placeholder="رمز عبور" required class="..." />

        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 rounded-lg transition"
        >
          {{ loading ? 'در حال ورود...' : 'ورود' }}
        </button>

        <p v-if="error" class="text-red-400 text-center text-sm">{{ error }}</p>
      </form>

      <!-- لینک‌های ثبت‌نام و فراموشی -->
    </div>
  </div>
</template>