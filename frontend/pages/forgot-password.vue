<script setup lang="ts">
const email = ref('')
const message = ref('')
const error = ref('')

const submit = async () => {
  message.value = ''
  error.value = ''

  try {
    const res = await $fetch('http://127.0.0.1:8000/api/v1/user/password/reset/', {
      method: 'POST',
      body: { email: email.value }
    })
    message.value = res.message
  } catch (err: any) {
    error.value = err.data?.error || 'خطا در ارسال درخواست'
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-900 px-4">
    <div class="w-full max-w-md">
      <div class="bg-gray-800 rounded-xl shadow-xl p-8">
        <h2 class="text-2xl font-bold text-white text-center mb-6">فراموشی رمز عبور</h2>
        
        <form @submit.prevent="submit" class="space-y-4">
          <input
            v-model="email"
            type="email"
            placeholder="ایمیل خود را وارد کنید"
            class="w-full px-4 py-3 rounded bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            required
          />
          
          <button
            type="submit"
            class="w-full bg-indigo-600 hover:bg-indigo-700 text-white py-3 rounded font-bold transition"
          >
            ارسال لینک ریست
          </button>
        </form>

        <p v-if="message" class="mt-4 text-green-400 text-center text-sm">{{ message }}</p>
        <p v-if="error" class="mt-4 text-red-400 text-center text-sm">{{ error }}</p>

        <p class="mt-6 text-center text-gray-400 text-sm">
          <NuxtLink to="/login" class="text-indigo-400 hover:underline">برگشت به ورود</NuxtLink>
        </p>
      </div>
    </div>
  </div>
</template>