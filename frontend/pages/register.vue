<!-- pages/register.vue -->
<script setup lang="ts">


const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const errorMsg = ref('')
const showPassword = ref(false)
const showConfirmPassword = ref(false)

const passwordMatch = computed(() =>
  confirmPassword.value === '' || password.value === confirmPassword.value
)

const isFormValid = computed(() =>
  email.value && password.value.length >= 8 && passwordMatch.value && confirmPassword.value
)

const register = async () => {
  if (!isFormValid.value) return
  loading.value = true
  errorMsg.value = ''

  try {
   await $fetch('/api/auth/register', {
  method: 'POST',
  body: { email: email.value, password: password.value }
})
    await navigateTo('/login')
  } catch (err: any) {
    errorMsg.value = err?.data?.message || 'خطایی رخ داد. لطفاً دوباره تلاش کنید.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="register-page">
    <!-- Background effects -->
    <div class="bg-orb bg-orb-1" />
    <div class="bg-orb bg-orb-2" />
    <div class="bg-grid" />

    <div class="register-container">
      <!-- Logo / Brand -->
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

      <!-- Card -->
      <div class="card">
        <div class="card-header">
          <h1 class="card-title">ایجاد حساب کاربری</h1>
          <p class="card-subtitle">به خانواده ما بپیوندید</p>
        </div>

        <form @submit.prevent="register" class="form" novalidate>
          <!-- Error -->
          <Transition name="shake">
            <div v-if="errorMsg" class="error-banner">
              <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                <path d="M8 1a7 7 0 100 14A7 7 0 008 1zm.75 4a.75.75 0 00-1.5 0v3.5a.75.75 0 001.5 0V5zm-.75 6.5a1 1 0 110-2 1 1 0 010 2z"/>
              </svg>
              {{ errorMsg }}
            </div>
          </Transition>

          <!-- Email -->
          <div class="field">
            <label class="field-label">ایمیل</label>
            <div class="field-input-wrap">
              <svg class="field-icon" width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                <path d="M2 4a2 2 0 012-2h8a2 2 0 012 2v8a2 2 0 01-2 2H4a2 2 0 01-2-2V4zm2-.5a.5.5 0 00-.5.5v.379l4.5 3 4.5-3V4a.5.5 0 00-.5-.5H4zm8.5 2.121l-4.5 3-4.5-3V12a.5.5 0 00.5.5h8a.5.5 0 00.5-.5V5.621z"/>
              </svg>
              <input
                v-model="email"
                type="email"
                placeholder="example@email.com"
                class="field-input"
                autocomplete="email"
                dir="ltr"
              />
            </div>
          </div>

          <!-- Password -->
          <div class="field">
            <label class="field-label">رمز عبور</label>
            <div class="field-input-wrap">
              <svg class="field-icon" width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                <path d="M8 1a4 4 0 00-4 4v1H3a1 1 0 00-1 1v7a1 1 0 001 1h10a1 1 0 001-1V7a1 1 0 00-1-1h-1V5a4 4 0 00-4-4zm0 1.5A2.5 2.5 0 0110.5 5v1h-5V5A2.5 2.5 0 018 2.5zm0 7a1.5 1.5 0 110-3 1.5 1.5 0 010 3z"/>
              </svg>
              <input
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="حداقل ۸ کاراکتر"
                class="field-input"
                autocomplete="new-password"
                dir="ltr"
              />
              <button type="button" class="eye-btn" @click="showPassword = !showPassword">
                <svg v-if="!showPassword" width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                  <path d="M8 3C4.5 3 1.5 5.5 1 8c.5 2.5 3.5 5 7 5s6.5-2.5 7-5c-.5-2.5-3.5-5-7-5zm0 8a3 3 0 110-6 3 3 0 010 6zm0-4.5a1.5 1.5 0 100 3 1.5 1.5 0 000-3z"/>
                </svg>
                <svg v-else width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                  <path d="M2 2l12 12M8 3C4.5 3 1.5 5.5 1 8c.3 1.3 1 2.5 2 3.4M6.1 6.1A3 3 0 0111 11M8 13c3.5 0 6.5-2.5 7-5-.3-1.3-1-2.5-2-3.4"/>
                </svg>
              </button>
            </div>
            <!-- Password strength -->
            <div class="strength-bar" v-if="password">
              <div
                class="strength-fill"
                :class="{
                  'strength-weak': password.length < 6,
                  'strength-medium': password.length >= 6 && password.length < 10,
                  'strength-strong': password.length >= 10
                }"
                :style="{ width: Math.min(password.length * 10, 100) + '%' }"
              />
            </div>
          </div>

          <!-- Confirm Password -->
          <div class="field">
            <label class="field-label">تکرار رمز عبور</label>
            <div class="field-input-wrap" :class="{ 'field-error': !passwordMatch }">
              <svg class="field-icon" width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                <path d="M8 1a4 4 0 00-4 4v1H3a1 1 0 00-1 1v7a1 1 0 001 1h10a1 1 0 001-1V7a1 1 0 00-1-1h-1V5a4 4 0 00-4-4zm0 1.5A2.5 2.5 0 0110.5 5v1h-5V5A2.5 2.5 0 018 2.5zm0 7a1.5 1.5 0 110-3 1.5 1.5 0 010 3z"/>
              </svg>
              <input
                v-model="confirmPassword"
                :type="showConfirmPassword ? 'text' : 'password'"
                placeholder="رمز عبور را تکرار کنید"
                class="field-input"
                autocomplete="new-password"
                dir="ltr"
              />
              <button type="button" class="eye-btn" @click="showConfirmPassword = !showConfirmPassword">
                <svg v-if="!showConfirmPassword" width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                  <path d="M8 3C4.5 3 1.5 5.5 1 8c.5 2.5 3.5 5 7 5s6.5-2.5 7-5c-.5-2.5-3.5-5-7-5zm0 8a3 3 0 110-6 3 3 0 010 6zm0-4.5a1.5 1.5 0 100 3 1.5 1.5 0 000-3z"/>
                </svg>
                <svg v-else width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                  <path d="M2 2l12 12M8 3C4.5 3 1.5 5.5 1 8c.3 1.3 1 2.5 2 3.4M6.1 6.1A3 3 0 0111 11M8 13c3.5 0 6.5-2.5 7-5-.3-1.3-1-2.5-2-3.4"/>
                </svg>
              </button>
            </div>
            <p v-if="!passwordMatch" class="field-hint-error">رمز عبور مطابقت ندارد</p>
          </div>

          <!-- Submit -->
          <button type="submit" class="submit-btn" :disabled="!isFormValid || loading">
            <span v-if="!loading">ایجاد حساب</span>
            <span v-else class="loading-dots">
              <span /><span /><span />
            </span>
          </button>
        </form>

        <div class="card-footer">
          <span class="footer-text">قبلاً حساب دارید؟</span>
          <NuxtLink to="/login" class="footer-link">ورود به حساب</NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700&display=swap');

* { box-sizing: border-box; }

.register-page {
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

/* Background */
.bg-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  pointer-events: none;
}
.bg-orb-1 {
  width: 500px; height: 500px;
  background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%);
  top: -150px; right: -100px;
  animation: float 8s ease-in-out infinite;
}
.bg-orb-2 {
  width: 400px; height: 400px;
  background: radial-gradient(circle, rgba(16,185,129,0.1) 0%, transparent 70%);
  bottom: -100px; left: -80px;
  animation: float 10s ease-in-out infinite reverse;
}
.bg-grid {
  position: absolute; inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
  background-size: 40px 40px;
  pointer-events: none;
}

@keyframes float {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-30px) scale(1.05); }
}

/* Container */
.register-container {
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
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Brand */
.brand {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  color: #e2e8f0;
}
.brand-icon {
  width: 44px; height: 44px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  color: white;
  box-shadow: 0 8px 24px rgba(99,102,241,0.35);
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
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 20px;
  padding: 2rem;
  backdrop-filter: blur(20px);
  box-shadow:
    0 25px 60px rgba(0,0,0,0.5),
    0 0 0 1px rgba(99,102,241,0.08),
    inset 0 1px 0 rgba(255,255,255,0.06);
}

.card-header { margin-bottom: 1.75rem; }
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

/* Form */
.form { display: flex; flex-direction: column; gap: 1.1rem; }

/* Error banner */
.error-banner {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(239,68,68,0.1);
  border: 1px solid rgba(239,68,68,0.25);
  border-radius: 10px;
  padding: 0.75rem 1rem;
  color: #fca5a5;
  font-size: 0.85rem;
}

/* Field */
.field { display: flex; flex-direction: column; gap: 0.4rem; }
.field-label {
  font-size: 0.825rem;
  font-weight: 500;
  color: #94a3b8;
}
.field-input-wrap {
  position: relative;
  display: flex;
  align-items: center;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 10px;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.field-input-wrap:focus-within {
  border-color: rgba(99,102,241,0.6);
  box-shadow: 0 0 0 3px rgba(99,102,241,0.12);
}
.field-input-wrap.field-error {
  border-color: rgba(239,68,68,0.5);
}
.field-icon {
  position: absolute;
  right: 0.85rem;
  color: #475569;
  pointer-events: none;
  flex-shrink: 0;
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
.field-input::placeholder { color: #334155; }

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
.eye-btn:hover { color: #94a3b8; }

.field-hint-error {
  font-size: 0.775rem;
  color: #f87171;
  margin: 0;
}

/* Strength bar */
.strength-bar {
  height: 3px;
  background: rgba(255,255,255,0.06);
  border-radius: 2px;
  overflow: hidden;
  margin-top: 0.3rem;
}
.strength-fill {
  height: 100%;
  border-radius: 2px;
  transition: width 0.3s, background 0.3s;
}
.strength-weak { background: #ef4444; }
.strength-medium { background: #f59e0b; }
.strength-strong { background: #10b981; }

/* Submit */
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
  box-shadow: 0 4px 20px rgba(99,102,241,0.35);
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 48px;
}
.submit-btn:hover:not(:disabled) {
  opacity: 0.92;
  transform: translateY(-1px);
  box-shadow: 0 8px 28px rgba(99,102,241,0.45);
}
.submit-btn:active:not(:disabled) { transform: translateY(0); }
.submit-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* Loading dots */
.loading-dots { display: flex; gap: 5px; align-items: center; }
.loading-dots span {
  width: 6px; height: 6px;
  background: white;
  border-radius: 50%;
  animation: bounce 1.2s ease-in-out infinite;
}
.loading-dots span:nth-child(2) { animation-delay: 0.2s; }
.loading-dots span:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounce {
  0%, 80%, 100% { transform: scale(0.6); opacity: 0.5; }
  40% { transform: scale(1); opacity: 1; }
}

/* Footer */
.card-footer {
  margin-top: 1.5rem;
  text-align: center;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
}
.footer-text { color: #475569; }
.footer-link {
  color: #818cf8;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.15s;
}
.footer-link:hover { color: #a5b4fc; }

/* Transition */
.shake-enter-active { animation: shake 0.4s ease; }
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-6px); }
  75% { transform: translateX(6px); }
}
</style>
