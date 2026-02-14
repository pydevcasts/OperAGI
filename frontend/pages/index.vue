<!-- pages/index.vue -->
<script setup lang="ts">
const session = useUserSession() // بدون import – auto-import فعال است
const loggedIn = computed(() => !!session.value?.user)
const loadingSession = ref(true)
const fetchError = ref<string | null>(null)

const fetchSession = async (source = 'initial') => {
  try {
    console.log(`[${source}] Fetching session...`)
    await session.fetch()
    console.log(`[${source}] Session after fetch:`, session.value)
    console.log(`[${source}] loggedIn:`, loggedIn.value)
    console.log(`[${source}] User:`, session.value?.user)
  } catch (err) {
    fetchError.value = err.message || 'خطا در لود session'
    console.error(`[${source}] Fetch session error:`, err)
  }
}

// لود در server و client
onServerPrefetch(async () => {
  await fetchSession('SSR prefetch')
})

onMounted(async () => {
  await fetchSession('Client onMounted')
  loadingSession.value = false

  // retry بعد از ۵۰۰ms اگر هنوز لود نشده
  setTimeout(async () => {
    if (!session.value?.user) {
      console.log('Retry fetch after delay...')
      await fetchSession('Retry after delay')
    }
  }, 500)
})

// خروج ساده
const simpleLogout = async () => {
  await session.clear()
  console.log('Session cleared')
}

// خروج کامل
const fullLogout = async () => {
  await session.clear()
  await navigateTo('/logout')
}
</script>

<template>
  <div class="p-8 text-white min-h-screen bg-gray-900">
    <div v-if="loadingSession" class="text-center text-xl mt-20">
      در حال بررسی وضعیت ورود...
    </div>

    <div v-else-if="fetchError" class="text-center text-red-400 text-xl mt-20">
      خطا: {{ fetchError }}
    </div>

    <div v-else-if="loggedIn" class="max-w-2xl mx-auto">
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
            @click="fullLogout"
            class="bg-red-600 hover:bg-red-700 text-white font-bold py-4 px-8 rounded-xl transition shadow-lg"
          >
            خروج کامل
          </button>

          <button
            @click="simpleLogout"
            class="bg-gray-600 hover:bg-gray-700 text-white font-bold py-4 px-8 rounded-xl transition shadow-lg"
          >
            خروج ساده
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