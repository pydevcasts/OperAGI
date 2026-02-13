<!-- pages/login.vue -->
<script setup lang="ts">
import GoogleLoginButton from '~/components/GoogleLoginButton.vue'
import { useAuthStore } from '~/stores/auth'

const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const error = ref<string>('')
const loading = ref(false)

const handleCredentialsLogin = async (e: Event) => {
  e.preventDefault()
  
  error.value = ''
  loading.value = true

  try {
    console.log('Attempting credentials login with:', { email: email.value.trim() })

    await authStore.login(email.value.trim(), password.value)

    console.log('Credentials login successful → redirecting')

    await navigateTo('/dashboard') // یا '/' یا مسیر دلخواه

  } catch (err: any) {
    console.error('Credentials login error:', err)

    const serverMessage = err?.data?.non_field_errors?.[0] ||
                           err?.data?.detail ||
                           err?.data?.message ||
                           err?.message ||
                           'Login failed. Please check your email and password.'

    error.value = serverMessage
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 to-indigo-900 px-4">
    <div class="w-full max-w-md">
      <div class="bg-gray-800/90 backdrop-blur rounded-2xl shadow-xl p-8 border border-gray-700">
        
        <h2 class="text-3xl font-bold text-white text-center mb-8">
          Sign in to Operagi
        </h2>

        <GoogleLoginButton />

        <div class="relative my-8">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-600"></div>
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-4 bg-gray-800 text-gray-400">or continue with email</span>
          </div>
        </div>

        <form @submit="handleCredentialsLogin" class="space-y-6">
          <input
            v-model="email"
            type="email"
            placeholder="Email"
            required
            autocomplete="email"
            class="w-full px-4 py-3 rounded-lg bg-gray-700 border border-gray-600 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition"
          />

          <input
            v-model="password"
            type="password"
            placeholder="Password"
            required
            autocomplete="current-password"
            class="w-full px-4 py-3 rounded-lg bg-gray-700 border border-gray-600 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition"
          />

          <button
            type="submit"
            :disabled="loading"
            class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 rounded-lg transition duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-md"
          >
            {{ loading ? 'Signing in...' : 'Sign In' }}
          </button>

          <p v-if="error" class="text-red-400 text-center text-sm mt-4 animate-pulse">
            {{ error }}
          </p>
        </form>

        <div class="mt-6 text-center text-gray-400 text-sm space-y-2">
          <div>
            Don't have an account?
            <NuxtLink to="/register" class="text-indigo-400 hover:underline ml-1">
              Sign up
            </NuxtLink>
          </div>
          <div>
            <NuxtLink to="/forgot-password" class="text-indigo-400 hover:underline">
              Forgot password?
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>