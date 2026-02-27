<!-- pages/forgot-password.vue -->
<script setup lang="ts">
const email = ref('')
const message = ref('')
const error = ref('')
const loading = ref(false)
const submitted = ref(false)

const submit = async () => {
  message.value = ''
  error.value = ''
  loading.value = true

  try {
    const res = await $fetch('/api/auth/forgot-password', {
      method: 'POST',
      body: { email: email.value }
    })
    message.value = (res as any).message || 'Recovery link has been sent to your email.'
    submitted.value = true
  } catch (err: any) {
    const data = err?.data

    // Various error response structures from server
    const serverMsg =
      data?.message ||
      data?.error ||
      data?.detail ||
      (typeof data === 'string' ? data : null)

    // English error messages based on status code
    const statusMessages: Record<number, string> = {
      400: 'The entered email is invalid.',
      404: 'No account found with this email.',
      429: 'Too many requests. Please try again later.',
      500: 'Server error. Please try again later.',
    }

    const status = err?.status || err?.statusCode || data?.statusCode
    error.value =
      (typeof serverMsg === 'string' ? serverMsg : null) ||
      statusMessages[status] ||
      'Error sending request. Please try again.'
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
      <!-- Brand -->
      <div class="brand">
        <div class="brand-icon">
          <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
            <path d="M14 2L26 8V20L14 26L2 20V8L14 2Z" stroke="currentColor" stroke-width="1.5" fill="none" />
            <path d="M14 8L20 11V17L14 20L8 17V11L14 8Z" fill="currentColor" opacity="0.4" />
            <circle cx="14" cy="14" r="2.5" fill="currentColor" />
          </svg>
        </div>
        <span class="brand-name">OperAGI</span>
      </div>

      <!-- Card -->
      <div class="card">

        <!-- Success state -->
        <Transition name="fade">
          <div v-if="submitted" class="success-state">
            <div class="success-icon">
              <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                <circle cx="16" cy="16" r="15" stroke="#34d399" stroke-width="1.5" />
                <path d="M9 16l5 5 9-9" stroke="#34d399" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
            </div>
            <h2 class="success-title">Email Sent</h2>
            <p class="success-desc">{{ message }}</p>
            <p class="success-hint">If you don't receive the email, please check your spam folder.</p>
            <NuxtLink to="/login" class="back-btn">Back to Login</NuxtLink>
          </div>
        </Transition>

        <!-- Form state -->
        <Transition name="fade">
          <div v-if="!submitted">
            <div class="card-header">
              <div class="lock-icon">
                <svg width="22" height="22" viewBox="0 0 16 16" fill="currentColor">
                  <path d="M8 1a4 4 0 00-4 4v1H3a1 1 0 00-1 1v7a1 1 0 001 1h10a1 1 0 001-1V7a1 1 0 00-1-1h-1V5a4 4 0 00-4-4zm0 1.5A2.5 2.5 0 0110.5 5v1h-5V5A2.5 2.5 0 018 2.5zm0 7a1.5 1.5 0 110-3 1.5 1.5 0 010 3z" />
                </svg>
              </div>
              <h1 class="card-title">Forgot Password</h1>
              <p class="card-subtitle">Enter your email and we'll send you a recovery link.</p>
            </div>

            <form @submit.prevent="submit" class="form" novalidate>
              <!-- Error -->
              <Transition name="shake">
                <div v-if="error" class="error-banner">
                  <svg width="15" height="15" viewBox="0 0 16 16" fill="currentColor">
                    <path d="M8 1a7 7 0 100 14A7 7 0 008 1zm.75 4a.75.75 0 00-1.5 0v3.5a.75.75 0 001.5 0V5zm-.75 6.5a1 1 0 110-2 1 1 0 010 2z" />
                  </svg>
                  {{ error }}
                </div>
              </Transition>

              <!-- Email field -->
              <div class="field">
                <label class="field-label">Email Address</label>
                <div class="field-input-wrap">
                  <svg class="field-icon" width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                    <path d="M2 4a2 2 0 012-2h8a2 2 0 012 2v8a2 2 0 01-2 2H4a2 2 0 01-2-2V4zm2-.5a.5.5 0 00-.5.5v.379l4.5 3 4.5-3V4a.5.5 0 00-.5-.5H4zm8.5 2.121l-4.5 3-4.5-3V12a.5.5 0 00.5.5h8a.5.5 0 00.5-.5V5.621z" />
                  </svg>
                  <input
                    v-model="email"
                    type="email"
                    placeholder="example@email.com"
                    class="field-input"
                    autocomplete="email"
                    dir="ltr"
                    required
                  />
                </div>
              </div>

              <!-- Submit -->
              <button type="submit" class="submit-btn" :disabled="loading || !email">
                <span v-if="!loading">Send Recovery Link</span>
                <span v-else class="loading-dots">
                  <span /><span /><span />
                </span>
              </button>
            </form>

            <div class="card-footer">
              <NuxtLink to="/login" class="footer-link">
                <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor">
                  <path d="M15 8a.5.5 0 01-.5.5H2.707l3.147 3.146a.5.5 0 01-.708.708l-4-4a.5.5 0 010-.708l4-4a.5.5 0 01.708.708L2.707 7.5H14.5A.5.5 0 0115 8z" />
                </svg>
                Back to Login
              </NuxtLink>
            </div>
          </div>
        </Transition>

      </div>
    </div>
  </div>
</template>