<!-- pages/login.vue -->
<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'
import {  ref } from 'vue'



const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)
const showPassword = ref(false)
const handleLogin = async (e: Event) => {
  e.preventDefault()
  error.value = ''
  loading.value = true

  try {
    await authStore.login(email.value.trim(), password.value)
    window.location.href = '/'
  } catch (err: any) {
    const message = err?.data?.message || err?.message || ''

   if (err?.data?.statusCode === 403 || message === 'email_not_verified') {
  await navigateTo({
    path: '/email-not-verified',
    query: { email: email.value.trim() } // ← ایمیل رو پاس بده
  })
  return
}

    error.value = message || 'ورود ناموفق بود.'
  } finally {
    loading.value = false
  }
}
</script>
<template>
  <div class="login-page">
    <div class="bg-orb bg-orb-1" />
    <div class="bg-orb bg-orb-2" />
    <div class="bg-grid" />

    <div class="login-container">
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
        <div class="card-header">
          <h1 class="card-title">خوش برگشتید</h1>
          <p class="card-subtitle">وارد حساب کاربری خود شوید</p>
        </div>

        <GoogleLoginButton />

        <div class="divider">
          <span class="divider-line" />
          <span class="divider-text">یا با ایمیل</span>
          <span class="divider-line" />
        </div>

        <form @submit="handleLogin" class="form" novalidate>
          <!-- Error -->
          <Transition name="shake">
            <div v-if="error" class="error-banner">
              <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                <path d="M8 1a7 7 0 100 14A7 7 0 008 1zm.75 4a.75.75 0 00-1.5 0v3.5a.75.75 0 001.5 0V5zm-.75 6.5a1 1 0 110-2 1 1 0 010 2z" />
              </svg>
              {{ error }}
            </div>
          </Transition>

          <!-- Email -->
          <div class="field">
            <label class="field-label">ایمیل</label>
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

          <!-- Password -->
          <div class="field">
            <div class="field-label-row">
              <label class="field-label">رمز عبور</label>
              <NuxtLink to="/forgot-password" class="forgot-link">فراموشی رمز؟</NuxtLink>
            </div>
            <div class="field-input-wrap">
              <svg class="field-icon" width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                <path d="M8 1a4 4 0 00-4 4v1H3a1 1 0 00-1 1v7a1 1 0 001 1h10a1 1 0 001-1V7a1 1 0 00-1-1h-1V5a4 4 0 00-4-4zm0 1.5A2.5 2.5 0 0110.5 5v1h-5V5A2.5 2.5 0 018 2.5zm0 7a1.5 1.5 0 110-3 1.5 1.5 0 010 3z" />
              </svg>
              <input
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="رمز عبور خود را وارد کنید"
                class="field-input"
                autocomplete="current-password"
                dir="ltr"
                required
              />
              <button type="button" class="eye-btn" @click="showPassword = !showPassword">
                <svg v-if="!showPassword" width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                  <path d="M8 3C4.5 3 1.5 5.5 1 8c.5 2.5 3.5 5 7 5s6.5-2.5 7-5c-.5-2.5-3.5-5-7-5zm0 8a3 3 0 110-6 3 3 0 010 6zm0-4.5a1.5 1.5 0 100 3 1.5 1.5 0 000-3z" />
                </svg>
                <svg v-else width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                  <path d="M2 2l12 12M8 3C4.5 3 1.5 5.5 1 8c.3 1.3 1 2.5 2 3.4M6.1 6.1A3 3 0 0111 11M8 13c3.5 0 6.5-2.5 7-5-.3-1.3-1-2.5-2-3.4" />
                </svg>
              </button>
            </div>
          </div>

          <!-- Submit -->
          <button type="submit" class="submit-btn" :disabled="loading">
            <span v-if="!loading">ورود به حساب</span>
            <span v-else class="loading-dots">
              <span /><span /><span />
            </span>
          </button>
        </form>

        <div class="card-footer">
          <span class="footer-text">حساب کاربری ندارید؟</span>
          <NuxtLink to="/register" class="footer-link">ثبت‌نام کنید</NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>