<!-- pages/login.vue -->
<script setup lang="ts">
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import GoogleLoginButton from '../components/GoogleLoginButton.vue'

const email = ref('')
const password = ref('')
const error = ref('')
const authStore = useAuthStore()
const router = useRouter()

const handleLogin = async (e: Event) => {
  e.preventDefault()
  error.value = ''

  if (!email.value || !password.value) {
    error.value = 'لطفاً ایمیل و رمز عبور را وارد کنید.'
    return
  }

  try {
    await authStore.login(email.value, password.value)
    router.push('/')
  } catch (err: any) {
    error.value = err.message || 'ورود ناموفق بود.'
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 to-indigo-900 px-4">
    <div class="w-full max-w-md">
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-white">Operagi</h1>
        <p class="text-gray-400 mt-2">ورود به حساب کاربری</p>
      </div>

      <div class="bg-gray-800/90 backdrop-blur rounded-2xl shadow-xl p-8 border border-gray-700">
        <form @submit="handleLogin" class="space-y-6">
          <!-- دکمه گوگل -->
          <GoogleLoginButton />

          <div class="relative my-6">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-gray-600"></div>
            </div>
            <div class="relative flex justify-center text-sm">
              <span class="px-4 bg-gray-800 text-gray-400">یا با ایمیل</span>
            </div>
          </div>

          <input
            v-model="email"
            type="email"
            placeholder="ایمیل"
            class="w-full px-4 py-3 rounded-lg bg-gray-700 border border-gray-600 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            required
          />
          <input
            v-model="password"
            type="password"
            placeholder="رمز عبور"
            class="w-full px-4 py-3 rounded-lg bg-gray-700 border border-gray-600 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            required
          />

          <button
            type="submit"
            class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 rounded-lg transition"
          >
            ورود
          </button>

          <p v-if="error" class="text-red-400 text-center text-sm animate-pulse">
            {{ error }}
          </p>
        </form>

        <p class="mt-6 text-center text-gray-400 text-sm">
          حساب ندارید؟
          <NuxtLink to="/register" class="text-indigo-400 hover:underline">ثبت‌نام کنید</NuxtLink>
        </p>
        <p class="mt-4 text-center text-gray-400 text-sm">
  <NuxtLink to="/forgot-password" class="text-indigo-400 hover:underline">فراموشی رمز عبور؟</NuxtLink>
</p>
      </div>
    </div>
  </div>
</template>