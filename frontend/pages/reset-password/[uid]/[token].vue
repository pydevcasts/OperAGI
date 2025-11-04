<script setup lang="ts">
const route = useRoute()
const uid = route.params.uid
const token = route.params.token

const password = ref('')
const confirm = ref('')
const message = ref('')
const error = ref('')

const submit = async () => {
  if (password.value !== confirm.value) {
    error.value = 'رمزها مطابقت ندارند'
    return
  }

  try {
    const res = await $fetch('http://127.0.0.1:8000/api/v1/user/password/reset/confirm/', {
      method: 'POST',
      body: { uid, token, password: password.value }
    })
    message.value = res.message
  } catch (err: any) {
    error.value = err.data?.error || 'خطا در تنظیم رمز'
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-900 px-4">
    <div class="w-full max-w-md">
      <div class="bg-gray-800 rounded-xl shadow-xl p-8">
        <h2 class="text-2xl font-bold text-white text-center mb-6">تنظیم رمز جدید</h2>
        
        <form @submit.prevent="submit" class="space-y-4">
          <input
            v-model="password"
            type="password"
            placeholder="رمز جدید"
            class="w-full px-4 py-3 rounded bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            required
          />
          <input
            v-model="confirm"
            type="password"
            placeholder="تکرار رمز"
            class="w-full px-4 py-3 rounded bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            required
          />
          
          <button
            type="submit"
            class="w-full bg-indigo-600 hover:bg-indigo-700 text-white py-3 rounded font-bold transition"
          >
            تغییر رمز
          </button>
        </form>

        <p v-if="message" class="mt-4 text-green-400 text-center text-sm">{{ message }}</p>
        <p v-if="error" class="mt-4 text-red-400 text-center text-sm">{{ error }}</p>
      </div>
    </div>
  </div>
</template>