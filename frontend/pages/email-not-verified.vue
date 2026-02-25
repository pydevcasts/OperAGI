<script setup lang="ts">
const { user } = useUserSession()
const route = useRoute()
const loading = ref(false)
const sent = ref(false)
const error = ref('')

const userEmail = computed(() => 
  (user.value as any)?.email || route.query.email as string || ''
)

const resend = async () => {
  if (!userEmail.value) {
    error.value = 'ایمیل یافت نشد. لطفاً دوباره ثبت‌نام کنید.'
    return
  }
  
  loading.value = true
  error.value = ''
  try {
    await $fetch('/api/auth/resend-verification', {
      method: 'POST',
      body: { email: userEmail.value }
    })
    sent.value = true
  } catch (err: any) {
    error.value = err?.data?.message || 'خطا در ارسال ایمیل.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="page">
    <div class="bg-orb bg-orb-1" />
    <div class="bg-orb bg-orb-2" />
    <div class="bg-grid" />

    <div class="container">
      <div class="brand">
        <div class="brand-icon">
          <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
            <path d="M14 2L26 8V20L14 26L2 20V8L14 2Z" stroke="currentColor" stroke-width="1.5" fill="none"/>
            <path d="M14 8L20 11V17L14 20L8 17V11L14 8Z" fill="currentColor" opacity="0.4"/>
            <circle cx="14" cy="14" r="2.5" fill="currentColor"/>
          </svg>
        </div>
        <span class="brand-name">OperAGI</span>
      </div>

      <div class="card">
        <div v-if="!sent" class="state-box">
          <div class="mail-icon">📧</div>
          <h2 class="state-title">ایمیل خود را تأیید کنید</h2>
          <p class="state-desc">
            برای استفاده از خدمات، ابتدا باید ایمیل
            <strong style="color:#818cf8">{{ (user as any)?.email }}</strong>
            را تأیید کنید.
          </p>

          <div v-if="error" class="error-banner">{{ error }}</div>

          <button class="submit-btn" :disabled="loading" @click="resend">
            <span v-if="!loading">ارسال مجدد ایمیل تأیید</span>
            <span v-else class="loading-dots"><span /><span /><span /></span>
          </button>

          <NuxtLink to="/" class="footer-link">برگشت به خانه</NuxtLink>
        </div>

        <div v-else class="state-box">
          <div class="success-icon">
            <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
              <circle cx="16" cy="16" r="15" stroke="#34d399" stroke-width="1.5"/>
              <path d="M9 16l5 5 9-9" stroke="#34d399" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <h2 class="state-title">ایمیل ارسال شد</h2>
          <p class="state-desc">پوشه inbox و spam خود را بررسی کنید.</p>
          <NuxtLink to="/" class="footer-link">برگشت به خانه</NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>
