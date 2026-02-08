<!-- pages/index.vue -->
<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'
import { useRouter } from 'vue-router'
import { onMounted } from 'vue'

definePageMeta({
  middleware: 'auth'
})

const authStore = useAuthStore()
const router = useRouter()

onMounted(() => {
  console.log('🏠 [Home Page] بارگذاری صفحه اصلی')
  console.log('👤 [Home Page] اطلاعات کاربر:', authStore.user)
  console.log('🔑 [Home Page] Access Token موجود:', !!authStore.accessToken)
  
  // بررسی localStorage
  console.log('💾 [Home Page] بررسی localStorage:')
  console.log('  Access Token:', !!localStorage.getItem('accessToken'))
  console.log('  User:', !!localStorage.getItem('user'))
})

const logout = async () => {
  await authStore.logout()
  router.push('/login')
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <div class="container mx-auto p-8">
      <div v-if="authStore.user" class="bg-white rounded-2xl shadow-md p-8 max-w-2xl mx-auto">
        <div class="text-center mb-8">
          <img 
            v-if="authStore.user.image" 
            :src="authStore.user.image" 
            :alt="authStore.user.name"
            class="w-24 h-24 rounded-full object-cover mx-auto mb-4 border-4 border-indigo-100"
          />
          <h1 class="text-3xl font-bold text-gray-800">خوش آمدید، {{ authStore.user.name }}! 👋</h1>
          <p class="text-gray-600 mt-2">{{ authStore.user.email }}</p>
        </div>
        
        <div class="bg-indigo-50 rounded-lg p-6 mb-6">
          <h2 class="text-xl font-semibold text-indigo-900 mb-3">اطلاعات حساب کاربری</h2>
          <div class="space-y-2 text-right text-gray-700">
            <div class="flex justify-between">
              <span>آی‌دی کاربر:</span>
              <span class="font-mono text-sm">{{ authStore.user.id }}</span>
            </div>
            <div class="flex justify-between">
              <span>ایمیل تأیید شده:</span>
              <span>{{ authStore.user.emailVerified ? '✅ بله' : '❌ خیر' }}</span>
            </div>
            <div class="flex justify-between">
              <span>تاریخ عضویت:</span>
              <span>{{ new Date(authStore.user.createdAt).toLocaleDateString('fa-IR') }}</span>
            </div>
          </div>
        </div>
        
        <div class="bg-green-50 rounded-lg p-4 mb-6">
          <h2 class="text-lg font-semibold text-green-900 mb-2">توکن‌های احراز هویت</h2>
          <div class="space-y-1 text-sm text-green-800 font-mono">
            <div>Access Token: {{ authStore.accessToken?.substring(0, 30) }}...</div>
            <div v-if="authStore.refreshToken">Refresh Token: {{ authStore.refreshToken.substring(0, 30) }}...</div>
          </div>
        </div>
        
        <div class="bg-blue-50 rounded-lg p-4 mb-6">
          <h2 class="text-lg font-semibold text-blue-900 mb-2">ذخیره‌سازی</h2>
          <div class="space-y-1 text-sm text-blue-800">
            <div>✅ اطلاعات کاربر در <code>localStorage</code> ذخیره شده است</div>
            <div>✅ توکن‌ها در <code>localStorage</code> ذخیره شده است</div>
            <div>⚠️ سیشن Better Auth در <code>cookies</code> ذخیره شده است</div>
          </div>
        </div>
        
        <button 
          @click="logout" 
          class="w-full bg-red-600 hover:bg-red-700 text-white font-bold py-3 px-6 rounded-lg transition duration-200 flex items-center justify-center gap-2"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z" clip-rule="evenodd" />
          </svg>
          خروج از حساب
        </button>
      </div>
      
      <div v-else class="text-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto mb-4"></div>
        <p class="text-gray-600">در حال بارگذاری اطلاعات کاربر...</p>
      </div>
    </div>
  </div>
</template>