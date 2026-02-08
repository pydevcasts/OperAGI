<!-- pages/login/callback.vue -->
<script setup lang="ts">
console.log('========================================')
console.log('✅ صفحه کالبک لاگین بارگذاری شد!')
console.log('URL فعلی:', window.location.href)
console.log('========================================')

import { createAuthClient } from "better-auth/client"
import { useAuthStore } from '~/stores/auth'
import { useRuntimeConfig } from '#imports'
import { useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'

definePageMeta({
  layout: false
})

const config = useRuntimeConfig()
const router = useRouter()
const authStore = useAuthStore()
const status = ref('در حال بررسی احراز هویت...')
const error = ref('')

onMounted(async () => {
  console.log('🔍 [Callback] onMounted اجرا شد')
  
  try {
    // بررسی پارامترهای کالبک
    const urlParams = new URLSearchParams(window.location.search)
    const state = urlParams.get('state')
    const code = urlParams.get('code')
    
    if (state || code) {
      console.log('✅ [Callback] پارامترهای کالبک دریافت شدند')
      console.log('  State:', state?.substring(0, 20) + '...')
      console.log('  Code:', code?.substring(0, 20) + '...')
    }

    status.value = 'دریافت اطلاعات از گوگل...'
    console.log('🌐 [Callback] ایجاد کلاینت Better Auth')
    
    const authClient = createAuthClient({
      baseURL: config.public.betterAuthUrl
    })

    // انتظار برای تکمیل پردازش
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    console.log('👤 [Callback] دریافت session از Better Auth')
    const session = await authClient.getSession()
    
    if (!session?.user) {
      console.error('❌ [Callback] session یا user یافت نشد')
      throw new Error('احراز هویت با گوگل ناموفق بود')
    }

    // نمایش اطلاعات کاربر
    console.log('✅ [Callback] اطلاعات کاربر دریافت شد:')
    const userInfo = {
      id: session.user.id,
      name: session.user.name,
      email: session.user.email,
      image: session.user.image,
      emailVerified: session.user.emailVerified,
      createdAt: session.user.createdAt,
      updatedAt: session.user.updatedAt
    }
    console.table(userInfo)

    // ✅ ارسال اطلاعات به بک‌اند
    status.value = 'ارسال اطلاعات به سرور...'
    console.log('📤 [Callback] ارسال به بک‌اند:', config.public.apiBase)
    
    await authStore.loginWithGoogle(userInfo)

    console.log('✅ [Callback] اطلاعات با موفقیت به بک‌اند ارسال شد')
    console.log('👤 [Callback] کاربر در استور:', authStore.user)
    console.log('🔑 [Callback] Access Token:', authStore.accessToken?.substring(0, 30) + '...')

    // بررسی ذخیره‌سازی در localStorage
    console.log('💾 [Callback] بررسی localStorage:')
    console.log('  Access Token:', !!localStorage.getItem('accessToken'))
    console.log('  User:', !!localStorage.getItem('user'))

    // ریدایرکت
    status.value = 'ورود موفق! در حال انتقال...'
    console.log('➡️ [Callback] ریدایرکت به صفحه اصلی')
    
    setTimeout(() => {
      router.push('/')
    }, 1000)
    
  } catch (err) {
    console.error('❌ [Callback] خطا:', err)
    error.value = err instanceof Error ? err.message : 'خطای ناشناخته'
    status.value = 'خطا در پردازش'
    
    setTimeout(() => {
      router.push('/login?error=google_login_failed')
    }, 3000)
  }
})
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
    <div class="bg-white rounded-2xl shadow-xl p-8 w-full max-w-md text-center">
      <div class="flex justify-center mb-6">
        <div class="animate-spin rounded-full h-16 w-16 border-b-2 border-indigo-600"></div>
      </div>
      
      <h1 class="text-2xl font-bold text-gray-800 mb-2">در حال ورود با گوگل</h1>
      <p class="text-gray-600">{{ status }}</p>
      
      <div v-if="error" class="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700">
        {{ error }}
      </div>
    </div>
  </div>
</template>