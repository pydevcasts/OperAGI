<!-- pages/login.vue -->
<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'
import { nextTick } from 'vue'



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
    const session = useUserSession()
    await session.fetch()
    await nextTick()
    window.location.href = '/'
  } catch (err: any) {
    error.value =
      err?.data?.non_field_errors?.[0] ||
      err?.data?.detail ||
      err?.data?.message ||
      err?.message ||
      'ورود ناموفق بود. لطفاً ایمیل و رمز عبور را بررسی کنید.'
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

        <!-- Google Login -->
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
                <path
                  d="M8 1a7 7 0 100 14A7 7 0 008 1zm.75 4a.75.75 0 00-1.5 0v3.5a.75.75 0 001.5 0V5zm-.75 6.5a1 1 0 110-2 1 1 0 010 2z" />
              </svg>
              {{ error }}
            </div>
          </Transition>

          <!-- Email -->
          <div class="field">
            <label class="field-label">ایمیل</label>
            <div class="field-input-wrap">
              <svg class="field-icon" width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                <path
                  d="M2 4a2 2 0 012-2h8a2 2 0 012 2v8a2 2 0 01-2 2H4a2 2 0 01-2-2V4zm2-.5a.5.5 0 00-.5.5v.379l4.5 3 4.5-3V4a.5.5 0 00-.5-.5H4zm8.5 2.121l-4.5 3-4.5-3V12a.5.5 0 00.5.5h8a.5.5 0 00.5-.5V5.621z" />
              </svg>
              <input v-model="email" type="email" placeholder="example@email.com" class="field-input"
                autocomplete="email" dir="ltr" required />
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
                <path
                  d="M8 1a4 4 0 00-4 4v1H3a1 1 0 00-1 1v7a1 1 0 001 1h10a1 1 0 001-1V7a1 1 0 00-1-1h-1V5a4 4 0 00-4-4zm0 1.5A2.5 2.5 0 0110.5 5v1h-5V5A2.5 2.5 0 018 2.5zm0 7a1.5 1.5 0 110-3 1.5 1.5 0 010 3z" />
              </svg>
              <input v-model="password" :type="showPassword ? 'text' : 'password'"
                placeholder="رمز عبور خود را وارد کنید" class="field-input" autocomplete="current-password" dir="ltr"
                required />
              <button type="button" class="eye-btn" @click="showPassword = !showPassword">
                <svg v-if="!showPassword" width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                  <path
                    d="M8 3C4.5 3 1.5 5.5 1 8c.5 2.5 3.5 5 7 5s6.5-2.5 7-5c-.5-2.5-3.5-5-7-5zm0 8a3 3 0 110-6 3 3 0 010 6zm0-4.5a1.5 1.5 0 100 3 1.5 1.5 0 000-3z" />
                </svg>
                <svg v-else width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                  <path
                    d="M2 2l12 12M8 3C4.5 3 1.5 5.5 1 8c.3 1.3 1 2.5 2 3.4M6.1 6.1A3 3 0 0111 11M8 13c3.5 0 6.5-2.5 7-5-.3-1.3-1-2.5-2-3.4" />
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

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700&display=swap');

* {
  box-sizing: border-box;
}

.login-page {
  font-family: 'Vazirmatn', sans-serif;
  min-height: 100vh;
  background: #080b14;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  direction: rtl;
  padding: 2rem 1rem;
}

.bg-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  pointer-events: none;
}

.bg-orb-1 {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(99, 102, 241, 0.15) 0%, transparent 70%);
  top: -150px;
  right: -100px;
  animation: float 8s ease-in-out infinite;
}

.bg-orb-2 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(16, 185, 129, 0.1) 0%, transparent 70%);
  bottom: -100px;
  left: -80px;
  animation: float 10s ease-in-out infinite reverse;
}

.bg-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
  background-size: 40px 40px;
  pointer-events: none;
}

@keyframes float {

  0%,
  100% {
    transform: translateY(0) scale(1);
  }

  50% {
    transform: translateY(-30px) scale(1.05);
  }
}

.login-container {
  width: 100%;
  max-width: 420px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
  position: relative;
  z-index: 1;
  animation: fadeUp 0.5s ease forwards;
}

@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  color: #e2e8f0;
}

.brand-icon {
  width: 44px;
  height: 44px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 8px 24px rgba(99, 102, 241, 0.35);
}

.brand-name {
  font-size: 1.4rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  background: linear-gradient(135deg, #e2e8f0, #94a3b8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.card {
  width: 100%;
  background: rgba(15, 20, 35, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.07);
  border-radius: 20px;
  padding: 2rem;
  backdrop-filter: blur(20px);
  box-shadow:
    0 25px 60px rgba(0, 0, 0, 0.5),
    0 0 0 1px rgba(99, 102, 241, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.06);
}

.card-header {
  margin-bottom: 1.5rem;
}

.card-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #f1f5f9;
  margin: 0 0 0.3rem;
  letter-spacing: -0.02em;
}

.card-subtitle {
  font-size: 0.875rem;
  color: #64748b;
  margin: 0;
}

/* Google btn */
.google-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  color: #e2e8f0;
  font-family: 'Vazirmatn', sans-serif;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s, border-color 0.2s;
}

.google-btn:hover {
  background: rgba(255, 255, 255, 0.09);
  border-color: rgba(255, 255, 255, 0.18);
}

/* Divider */
.divider {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin: 1.25rem 0;
}

.divider-line {
  flex: 1;
  height: 1px;
  background: rgba(255, 255, 255, 0.07);
}

.divider-text {
  font-size: 0.8rem;
  color: #475569;
  white-space: nowrap;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 1.1rem;
}

.error-banner {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.25);
  border-radius: 10px;
  padding: 0.75rem 1rem;
  color: #fca5a5;
  font-size: 0.85rem;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.field-label-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.field-label {
  font-size: 0.825rem;
  font-weight: 500;
  color: #94a3b8;
}

.forgot-link {
  font-size: 0.775rem;
  color: #6366f1;
  text-decoration: none;
  transition: color 0.15s;
}

.forgot-link:hover {
  color: #818cf8;
}

.field-input-wrap {
  position: relative;
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.field-input-wrap:focus-within {
  border-color: rgba(99, 102, 241, 0.6);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.12);
}

.field-icon {
  position: absolute;
  right: 0.85rem;
  color: #475569;
  pointer-events: none;
}

.field-input {
  width: 100%;
  background: transparent;
  border: none;
  outline: none;
  color: #e2e8f0;
  font-family: 'Vazirmatn', sans-serif;
  font-size: 0.9rem;
  padding: 0.75rem 2.4rem 0.75rem 2.8rem;
  direction: ltr;
  text-align: left;
}

.field-input::placeholder {
  color: #334155;
}

.eye-btn {
  position: absolute;
  left: 0.7rem;
  background: none;
  border: none;
  color: #475569;
  cursor: pointer;
  padding: 0.2rem;
  display: flex;
  align-items: center;
  transition: color 0.15s;
}

.eye-btn:hover {
  color: #94a3b8;
}

.submit-btn {
  margin-top: 0.5rem;
  width: 100%;
  padding: 0.85rem;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border: none;
  border-radius: 10px;
  color: white;
  font-family: 'Vazirmatn', sans-serif;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s, transform 0.15s, box-shadow 0.2s;
  box-shadow: 0 4px 20px rgba(99, 102, 241, 0.35);
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 48px;
}

.submit-btn:hover:not(:disabled) {
  opacity: 0.92;
  transform: translateY(-1px);
  box-shadow: 0 8px 28px rgba(99, 102, 241, 0.45);
}

.submit-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.loading-dots {
  display: flex;
  gap: 5px;
  align-items: center;
}

.loading-dots span {
  width: 6px;
  height: 6px;
  background: white;
  border-radius: 50%;
  animation: bounce 1.2s ease-in-out infinite;
}

.loading-dots span:nth-child(2) {
  animation-delay: 0.2s;
}

.loading-dots span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes bounce {

  0%,
  80%,
  100% {
    transform: scale(0.6);
    opacity: 0.5;
  }

  40% {
    transform: scale(1);
    opacity: 1;
  }
}

.card-footer {
  margin-top: 1.5rem;
  text-align: center;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
}

.footer-text {
  color: #475569;
}

.footer-link {
  color: #818cf8;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.15s;
}

.footer-link:hover {
  color: #a5b4fc;
}

.shake-enter-active {
  animation: shake 0.4s ease;
}

@keyframes shake {

  0%,
  100% {
    transform: translateX(0);
  }

  25% {
    transform: translateX(-6px);
  }

  75% {
    transform: translateX(6px);
  }
}
</style>