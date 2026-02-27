<!-- pages/verify-email/[token].vue  -->
<script setup lang="ts">
definePageMeta({ middleware: 'guest' })

const route = useRoute()
const token = route.params.token as string
const loading = ref(true)
const success = ref(false)
const error = ref('')

onMounted(async () => {
  try {
    await $fetch('/api/auth/verify-email', {
      method: 'POST',
      body: { key: token }
    })
    success.value = true
  } catch (err: any) {
    error.value = 'The verification link is invalid or has expired.'
  } finally {
    loading.value = false
  }
})
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

        <!-- Loading -->
        <div v-if="loading" class="state-box">
          <div class="spinner" />
          <p class="state-text">Verifying your email...</p>
        </div>

        <!-- Success -->
        <div v-else-if="success" class="state-box">
          <div class="success-icon">
            <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
              <circle cx="16" cy="16" r="15" stroke="#34d399" stroke-width="1.5"/>
              <path d="M9 16l5 5 9-9" stroke="#34d399" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <h2 class="state-title">Email Verified!</h2>
          <p class="state-desc">Your account has been successfully activated.</p>
          <NuxtLink to="/login" class="submit-btn">Sign In</NuxtLink>
        </div>

        <!-- Error -->
        <div v-else class="state-box">
          <div class="error-icon">
            <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
              <circle cx="16" cy="16" r="15" stroke="#f87171" stroke-width="1.5"/>
              <path d="M10 10l12 12M22 10L10 22" stroke="#f87171" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </div>
          <h2 class="state-title">Invalid Link</h2>
          <p class="state-desc">{{ error }}</p>
          <NuxtLink to="/login" class="submit-btn">Back to Login</NuxtLink>
        </div>

      </div>
    </div>
  </div>
</template>