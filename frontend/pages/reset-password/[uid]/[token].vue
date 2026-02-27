<!-- pages/reset-password/[uid]/[token].vue -->
<script setup lang="ts">
definePageMeta({ middleware: 'guest' })

const route = useRoute()
const uid = route.params.uid as string
const token = route.params.token as string

const password1 = ref('')
const password2 = ref('')
const loading = ref(false)
const error = ref('')
const success = ref(false)
const showPass1 = ref(false)
const showPass2 = ref(false)

const passwordMatch = computed(() =>
  password2.value === '' || password1.value === password2.value
)

const isValid = computed(() =>
  password1.value.length >= 8 && passwordMatch.value && password2.value !== ''
)

const submit = async () => {
  if (!isValid.value) return
  loading.value = true
  error.value = ''

  try {
    await $fetch('/api/auth/reset-password-confirm', {
      method: 'POST',
      body: {
        uid,
        token,
        new_password1: password1.value,
        new_password2: password2.value
      }
    })
    success.value = true
  } catch (err: any) {
    error.value =
      err?.data?.token?.[0] ||
      err?.data?.new_password2?.[0] ||
      err?.data?.message ||
      'The link has expired or is invalid. Please request a new one.'
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
            <path d="M14 2L26 8V20L14 26L2 20V8L14 2Z" stroke="currentColor" stroke-width="1.5" fill="none"/>
            <path d="M14 8L20 11V17L14 20L8 17V11L14 8Z" fill="currentColor" opacity="0.4"/>
            <circle cx="14" cy="14" r="2.5" fill="currentColor"/>
          </svg>
        </div>
        <span class="brand-name">OperAGI</span>
      </div>

      <!-- Card -->
      <div class="card">

        <!-- Success state -->
        <Transition name="fade">
          <div v-if="success" class="success-state">
            <div class="success-icon">
              <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                <circle cx="16" cy="16" r="15" stroke="#34d399" stroke-width="1.5"/>
                <path d="M9 16l5 5 9-9" stroke="#34d399" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <h2 class="success-title">Password Changed</h2>
            <p class="success-desc">Your password has been successfully updated.</p>
            <NuxtLink to="/login" class="back-btn">
              <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor">
                <path d="M1 8a.5.5 0 01.5-.5h12.293l-3.147-3.146a.5.5 0 01.708-.708l4 4a.5.5 0 010 .708l-4 4a.5.5 0 01-.708-.708L2.707 8.5H1.5A.5.5 0 011 8z"/>
              </svg>
              Sign In
            </NuxtLink>
          </div>
        </Transition>

        <!-- Form state -->
        <Transition name="fade">
          <div v-if="!success">
            <div class="card-header">
              <div class="shield-icon">
                <svg width="22" height="22" viewBox="0 0 16 16" fill="currentColor">
                  <path d="M5.338 1.59a61.44 61.44 0 00-2.837.856.481.481 0 00-.328.39c-.554 4.157.726 7.19 2.959 9.19a11.75 11.75 0 002.876 1.934c.17.078.345.145.52.205.323-.06.65-.162.972-.314a11.75 11.75 0 002.878-1.926c2.234-2 3.514-5.032 2.96-9.189a.48.48 0 00-.326-.39 60.637 60.637 0 00-2.837-.855C9.552 1.29 8.531 1.067 8 1.067c-.53 0-1.552.223-2.662.524zM5.072.56C6.157.265 7.31 0 8 0s1.843.265 2.928.56c1.11.3 2.229.655 2.887.87a1.54 1.54 0 011.044 1.262c.596 4.477-.787 7.795-2.465 9.99a13.193 13.193 0 01-3.268 2.352 6.37 6.37 0 01-.556.25 1 1 0 01-.77 0 6.37 6.37 0 01-.556-.25 13.192 13.192 0 01-3.27-2.351C1.219 10.642-.164 7.324.432 2.847A1.54 1.54 0 011.476 1.59C2.134.844 3.253.49 4.364.19L5.072.56z"/>
                  <path d="M10.854 5.146a.5.5 0 010 .708l-3 3a.5.5 0 01-.708 0l-1.5-1.5a.5.5 0 11.708-.708L7.5 7.793l2.646-2.647a.5.5 0 01.708 0z"/>
                </svg>
              </div>
              <h1 class="card-title">Set New Password</h1>
              <p class="card-subtitle">Enter your new password below.</p>
            </div>

            <form @submit.prevent="submit" class="form" novalidate>

              <!-- Error -->
              <Transition name="shake">
                <div v-if="error" class="error-banner">
                  <svg width="15" height="15" viewBox="0 0 16 16" fill="currentColor">
                    <path d="M8 1a7 7 0 100 14A7 7 0 008 1zm.75 4a.75.75 0 00-1.5 0v3.5a.75.75 0 001.5 0V5zm-.75 6.5a1 1 0 110-2 1 1 0 010 2z"/>
                  </svg>
                  {{ error }}
                </div>
              </Transition>

              <!-- Password 1 -->
              <div class="field">
                <label class="field-label">New Password</label>
                <div class="field-input-wrap">
                  <svg class="field-icon" width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                    <path d="M8 1a4 4 0 00-4 4v1H3a1 1 0 00-1 1v7a1 1 0 001 1h10a1 1 0 001-1V7a1 1 0 00-1-1h-1V5a4 4 0 00-4-4zm0 1.5A2.5 2.5 0 0110.5 5v1h-5V5A2.5 2.5 0 018 2.5zm0 7a1.5 1.5 0 110-3 1.5 1.5 0 010 3z"/>
                  </svg>
                  <input
                    v-model="password1"
                    :type="showPass1 ? 'text' : 'password'"
                    placeholder="At least 8 characters"
                    class="field-input"
                    autocomplete="new-password"
                    dir="ltr"
                    required
                  />
                  <button type="button" class="eye-btn" @click="showPass1 = !showPass1">
                    <svg v-if="!showPass1" width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                      <path d="M8 3C4.5 3 1.5 5.5 1 8c.5 2.5 3.5 5 7 5s6.5-2.5 7-5c-.5-2.5-3.5-5-7-5zm0 8a3 3 0 110-6 3 3 0 010 6zm0-4.5a1.5 1.5 0 100 3 1.5 1.5 0 000-3z"/>
                    </svg>
                    <svg v-else width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                      <path d="M2 2l12 12M8 3C4.5 3 1.5 5.5 1 8c.3 1.3 1 2.5 2 3.4M6.1 6.1A3 3 0 0111 11M8 13c3.5 0 6.5-2.5 7-5-.3-1.3-1-2.5-2-3.4"/>
                    </svg>
                  </button>
                </div>
                <!-- Strength bar -->
                <div class="strength-bar" v-if="password1">
                  <div
                    class="strength-fill"
                    :class="{
                      'strength-weak': password1.length < 6,
                      'strength-medium': password1.length >= 6 && password1.length < 10,
                      'strength-strong': password1.length >= 10
                    }"
                    :style="{ width: Math.min(password1.length * 10, 100) + '%' }"
                  />
                </div>
              </div>

              <!-- Password 2 -->
              <div class="field">
                <label class="field-label">Confirm New Password</label>
                <div class="field-input-wrap" :class="{ 'field-error': !passwordMatch && password2 }">
                  <svg class="field-icon" width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                    <path d="M8 1a4 4 0 00-4 4v1H3a1 1 0 00-1 1v7a1 1 0 001 1h10a1 1 0 001-1V7a1 1 0 00-1-1h-1V5a4 4 0 00-4-4zm0 1.5A2.5 2.5 0 0110.5 5v1h-5V5A2.5 2.5 0 018 2.5zm0 7a1.5 1.5 0 110-3 1.5 1.5 0 010 3z"/>
                  </svg>
                  <input
                    v-model="password2"
                    :type="showPass2 ? 'text' : 'password'"
                    placeholder="Confirm your new password"
                    class="field-input"
                    autocomplete="new-password"
                    dir="ltr"
                    required
                  />
                  <button type="button" class="eye-btn" @click="showPass2 = !showPass2">
                    <svg v-if="!showPass2" width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                      <path d="M8 3C4.5 3 1.5 5.5 1 8c.5 2.5 3.5 5 7 5s6.5-2.5 7-5c-.5-2.5-3.5-5-7-5zm0 8a3 3 0 110-6 3 3 0 010 6zm0-4.5a1.5 1.5 0 100 3 1.5 1.5 0 000-3z"/>
                    </svg>
                    <svg v-else width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                      <path d="M2 2l12 12M8 3C4.5 3 1.5 5.5 1 8c.3 1.3 1 2.5 2 3.4M6.1 6.1A3 3 0 0111 11M8 13c3.5 0 6.5-2.5 7-5-.3-1.3-1-2.5-2-3.4"/>
                    </svg>
                  </button>
                </div>
                <p v-if="!passwordMatch && password2" class="field-hint-error">Passwords do not match</p>
              </div>

              <!-- Submit -->
              <button type="submit" class="submit-btn" :disabled="!isValid || loading">
                <span v-if="!loading">Change Password</span>
                <span v-else class="loading-dots">
                  <span /><span /><span />
                </span>
              </button>
            </form>

            <div class="card-footer">
              <NuxtLink to="/login" class="footer-link">
                <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor">
                  <path d="M1 8a.5.5 0 01.5-.5h12.293l-3.147-3.146a.5.5 0 01.708-.708l4 4a.5.5 0 010 .708l-4 4a.5.5 0 01-.708-.708L2.707 8.5H1.5A.5.5 0 011 8z"/>
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