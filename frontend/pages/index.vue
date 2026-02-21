<!-- pages/index.vue -->
<script setup lang="ts">
const { user, loggedIn, fetch: fetchSession, clear } = useUserSession()

// لود session در client-side
onMounted(async () => {
  await fetchSession()
  console.log('Session loaded in client:', { loggedIn: loggedIn.value, user: user.value })
})

// خروج ساده
const simpleLogout = async () => {
  await clear()
  await navigateTo('/login')
}
</script>

<template>
  <div class="p-8 text-white min-h-screen bg-gray-900">
    <div v-if="loggedIn" class="max-w-2xl mx-auto">
      <h1 class="text-4xl font-bold mb-8 text-center">
        خوش آمدی {{ user?.name || 'کاربر' }}!
      </h1>

      <div class="bg-gray-800 p-8 rounded-2xl shadow-2xl border border-gray-700">
        <div class="text-center mb-6">
          <img
            v-if="user?.picture"
            :src="user.picture"
            alt="Profile"
            class="w-32 h-32 rounded-full mx-auto mb-4 border-4 border-indigo-500 shadow-lg object-cover"
          />
          <p class="text-2xl font-semibold">{{ user?.email }}</p>
        </div>

        <div class="flex justify-center gap-6 mt-8">
          <button
            @click="simpleLogout"
            class="bg-red-600 hover:bg-red-700 text-white font-bold py-4 px-8 rounded-xl transition shadow-lg"
          >
            خروج
          </button>
        </div>
      </div>
    </div>

    <div v-else class="text-center text-2xl mt-20">
      <p class="mb-6">شما لاگین نیستید</p>

      <a
        href="/auth/google"
        class="inline-block bg-red-600 hover:bg-red-700 text-white font-bold py-4 px-10 rounded-xl transition shadow-lg text-lg"
      >
        ورود با حساب گوگل
      </a>
    </div>
  </div>
</template>

<style scoped>
button:focus {
  outline: none;
  ring: 2px solid #6366f1;
  ring-offset: 2px;
}
</style>