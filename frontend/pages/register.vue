<!-- pages/register.vue -->
<script setup lang="ts">
import {ref, computed} from 'vue'

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
    errorMsg.value = err?.data?.message || 'An error occurred. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="register-page">
    <div class="bg-orb bg-orb-1" />
    <div class="bg-orb bg-orb-2" />
    <div class="bg-grid" />

    <div class="register-container">
      <!-- Brand -->
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
          <h1 class="card-title">Create Account</h1>
          <p class="card-subtitle">Join our community</p>
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
            <label class="field-label">Email</label>
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
            <label class="field-label">Password</label>
            <div class="field-input-wrap">
              <svg class="field-icon" width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                <path d="M8 1a4 4 0 00-4 4v1H3a1 1 0 00-1 1v7a1 1 0 001 1h10a1 1 0 001-1V7a1 1 0 00-1-1h-1V5a4 4 0 00-4-4zm0 1.5A2.5 2.5 0 0110.5 5v1h-5V5A2.5 2.5 0 018 2.5zm0 7a1.5 1.5 0 110-3 1.5 1.5 0 010 3z"/>
              </svg>
              <input
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="At least 8 characters"
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
            <label class="field-label">Confirm Password</label>
            <div class="field-input-wrap" :class="{ 'field-error': confirmPassword && !passwordMatch }">
              <svg class="field-icon" width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                <path d="M8 1a4 4 0 00-4 4v1H3a1 1 0 00-1 1v7a1 1 0 001 1h10a1 1 0 001-1V7a1 1 0 00-1-1h-1V5a4 4 0 00-4-4zm0 1.5A2.5 2.5 0 0110.5 5v1h-5V5A2.5 2.5 0 018 2.5zm0 7a1.5 1.5 0 110-3 1.5 1.5 0 010 3z"/>
              </svg>
              <input
                v-model="confirmPassword"
                :type="showConfirmPassword ? 'text' : 'password'"
                placeholder="Confirm your password"
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
            <p v-if="confirmPassword && !passwordMatch" class="field-hint-error">Passwords do not match</p>
          </div>

          <!-- Submit -->
          <button type="submit" class="submit-btn" :disabled="!isFormValid || loading">
            <span v-if="!loading">Create Account</span>
            <span v-else class="loading-dots">
              <span /><span /><span />
            </span>
          </button>
        </form>

        <div class="card-footer">
          <span class="footer-text">Already have an account?</span>
          <NuxtLink to="/login" class="footer-link">Sign In</NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>