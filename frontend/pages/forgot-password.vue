<!-- pages/forgot-password.vue -->
<script setup lang="ts">
import { ref } from 'vue'

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
    message.value = (res as any).message || 'لینک بازیابی به ایمیل شما ارسال شد.'
    submitted.value = true
  } catch (err: any) {
    error.value = err.data?.error || 'خطا در ارسال درخواست. لطفاً دوباره تلاش کنید.'
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
                <path d="M9 16l5 5 9-9" stroke="#34d399" stroke-width="2" stroke-linecap="round"
                  stroke-linejoin="round" />
              </svg>
            </div>
            <h2 class="success-title">ایمیل ارسال شد</h2>
            <p class="success-desc">{{ message }}</p>
            <p class="success-hint">اگر ایمیل دریافت نکردید، پوشه اسپم را بررسی کنید.</p>
            <NuxtLink to="/login" class="back-btn">بازگشت به ورود</NuxtLink>
          </div>
        </Transition>

        <!-- Form state -->
        <Transition name="fade">
          <div v-if="!submitted">
            <div class="card-header">
              <div class="lock-icon">
                <svg width="22" height="22" viewBox="0 0 16 16" fill="currentColor">
                  <path
                    d="M8 1a4 4 0 00-4 4v1H3a1 1 0 00-1 1v7a1 1 0 001 1h10a1 1 0 001-1V7a1 1 0 00-1-1h-1V5a4 4 0 00-4-4zm0 1.5A2.5 2.5 0 0110.5 5v1h-5V5A2.5 2.5 0 018 2.5zm0 7a1.5 1.5 0 110-3 1.5 1.5 0 010 3z" />
                </svg>
              </div>
              <h1 class="card-title">فراموشی رمز عبور</h1>
              <p class="card-subtitle">ایمیل خود را وارد کنید تا لینک بازیابی برایتان ارسال شود.</p>
            </div>

            <form @submit.prevent="submit" class="form" novalidate>
              <!-- Error -->
              <Transition name="shake">
                <div v-if="error" class="error-banner">
                  <svg width="15" height="15" viewBox="0 0 16 16" fill="currentColor">
                    <path
                      d="M8 1a7 7 0 100 14A7 7 0 008 1zm.75 4a.75.75 0 00-1.5 0v3.5a.75.75 0 001.5 0V5zm-.75 6.5a1 1 0 110-2 1 1 0 010 2z" />
                  </svg>
                  {{ error }}
                </div>
              </Transition>

              <!-- Email field -->
              <div class="field">
                <label class="field-label">آدرس ایمیل</label>
                <div class="field-input-wrap">
                  <svg class="field-icon" width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                    <path
                      d="M2 4a2 2 0 012-2h8a2 2 0 012 2v8a2 2 0 01-2 2H4a2 2 0 01-2-2V4zm2-.5a.5.5 0 00-.5.5v.379l4.5 3 4.5-3V4a.5.5 0 00-.5-.5H4zm8.5 2.121l-4.5 3-4.5-3V12a.5.5 0 00.5.5h8a.5.5 0 00.5-.5V5.621z" />
                  </svg>
                  <input v-model="email" type="email" placeholder="example@email.com" class="field-input"
                    autocomplete="email" dir="ltr" required />
                </div>
              </div>

              <!-- Submit -->
              <button type="submit" class="submit-btn" :disabled="loading || !email">
                <span v-if="!loading">ارسال لینک بازیابی</span>
                <span v-else class="loading-dots">
                  <span /><span /><span />
                </span>
              </button>
            </form>

            <div class="card-footer">
              <NuxtLink to="/login" class="footer-link">
                <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor">
                  <path
                    d="M15 8a.5.5 0 01-.5.5H2.707l3.147 3.146a.5.5 0 01-.708.708l-4-4a.5.5 0 010-.708l4-4a.5.5 0 01.708.708L2.707 7.5H14.5A.5.5 0 0115 8z" />
                </svg>
                برگشت به ورود
              </NuxtLink>
            </div>
          </div>
        </Transition>

      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700&display=swap');

*,
*::before,
*::after {
  box-sizing: border-box;
}

.page {
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

.container {
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

/* Brand */
.brand {
  display: flex;
  align-items: center;
  gap: 0.6rem;
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

/* Card */
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
  min-height: 300px;
}

/* Lock icon */
.lock-icon {
  width: 52px;
  height: 52px;
  background: rgba(99, 102, 241, 0.12);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #818cf8;
  margin-bottom: 1rem;
}

.card-header {
  margin-bottom: 1.75rem;
}

.card-title {
  font-size: 1.4rem;
  font-weight: 700;
  color: #f1f5f9;
  margin: 0 0 0.4rem;
  letter-spacing: -0.02em;
}

.card-subtitle {
  font-size: 0.875rem;
  color: #64748b;
  margin: 0;
  line-height: 1.6;
}

/* Form */
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

.field-label {
  font-size: 0.825rem;
  font-weight: 500;
  color: #94a3b8;
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
  padding: 0.75rem 2.4rem 0.75rem 1rem;
  direction: ltr;
  text-align: left;
}

.field-input::placeholder {
  color: #334155;
}

.submit-btn {
  margin-top: 0.25rem;
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
  display: flex;
  justify-content: center;
}

.footer-link {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  color: #64748b;
  font-size: 0.875rem;
  text-decoration: none;
  transition: color 0.15s;
}

.footer-link:hover {
  color: #818cf8;
}

/* Success state */
.success-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 1rem 0;
  gap: 0.75rem;
}

.success-icon {
  width: 64px;
  height: 64px;
  background: rgba(16, 185, 129, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.5rem;
  animation: popIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
}

@keyframes popIn {
  from {
    transform: scale(0.5);
    opacity: 0;
  }

  to {
    transform: scale(1);
    opacity: 1;
  }
}

.success-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #f1f5f9;
  letter-spacing: -0.02em;
}

.success-desc {
  font-size: 0.875rem;
  color: #34d399;
}

.success-hint {
  font-size: 0.8rem;
  color: #475569;
}

.back-btn {
  margin-top: 0.75rem;
  display: inline-flex;
  align-items: center;
  padding: 0.7rem 1.5rem;
  background: rgba(99, 102, 241, 0.12);
  border: 1px solid rgba(99, 102, 241, 0.25);
  border-radius: 10px;
  color: #818cf8;
  font-family: 'Vazirmatn', sans-serif;
  font-size: 0.875rem;
  font-weight: 600;
  text-decoration: none;
  transition: background 0.15s;
}

.back-btn:hover {
  background: rgba(99, 102, 241, 0.2);
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
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