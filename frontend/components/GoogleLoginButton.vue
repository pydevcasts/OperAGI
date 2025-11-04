<!-- components/GoogleLoginButton.vue -->
<script setup lang="ts">
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import { nextTick, onMounted, onUnmounted } from 'vue'

const authStore = useAuthStore()
const router = useRouter()

const clientId = import.meta.env.VITE_GOOGLE_OAUTH_CLIENT_ID

if (!clientId) {
  console.error('VITE_GOOGLE_OAUTH_CLIENT_ID is missing in .env!')
}

// تابع callback
const handleCredentialResponse = (response: any) => {
  const idToken = response.credential
  console.log('Google ID Token:', idToken)

  authStore.loginWithGoogle(idToken)
    .then(() => router.push('/'))
    .catch(err => console.error('Google login failed:', err))
}

// لود اسکریپت GIS
onMounted(() => {
  if (document.getElementById('google-gsi-script')) return

  const script = document.createElement('script')
  script.id = 'google-gsi-script'
  script.src = 'https://accounts.google.com/gsi/client'
  script.async = true
  script.defer = true

  script.onload = () => {
    console.log('Google GIS loaded')
    initButton()
  }

  document.head.appendChild(script)
})

const initButton = () => {
  nextTick(() => {
    ;(window as any).handleCredentialResponse = handleCredentialResponse

    if ((window as any).google?.accounts?.id) {
      ;(window as any).google.accounts.id.initialize({
        client_id: clientId,
        callback: handleCredentialResponse
      })

      const el = document.getElementById('google-signin-btn')
      if (el) {
        ;(window as any).google.accounts.id.renderButton(el, {
          theme: 'outline',
          size: 'large',
          text: 'signin_with',
          width: '100%'
        })
      }
    }
  })
}

onUnmounted(() => {
  delete (window as any).handleCredentialResponse
})
</script>

<template>
  <div id="google-signin-btn" class="w-full"></div>
</template>