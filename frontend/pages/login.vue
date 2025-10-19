<!-- pages/login.vue -->
<script setup lang="ts">
const email = ref('')
const password = ref('')
const error = ref('')

const handleLogin = async () => {
  try {
    const response = await $fetch('/api/v1/user/token/', {
      method: 'POST',
      body: {
        email: email.value,
        password: password.value
      }
    })

    // ✅ Fixed: use 'response', not 'res'
    localStorage.setItem('accessToken', response.access)
    localStorage.setItem('refreshToken', response.refresh)

    navigateTo('/')
  } catch (err) {
    error.value = 'Invalid email or password.'
    console.error(err)
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-900">
    <form @submit.prevent="handleLogin" class="bg-gray-800 p-8 rounded shadow w-full max-w-md">
      <h2 class="text-2xl font-bold mb-6 text-center text-white">Sign in to Operagi</h2>

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