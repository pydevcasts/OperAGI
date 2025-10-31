<template>
  <div id="g_id_onload"
       :data-client_id="clientId"
       data-callback="handleCredentialResponse"
       data-auto_prompt="false">
  </div>
  <div class="g_id_signin"
       data-type="standard"
       data-size="large"
       data-theme="outline"
       data-text="sign_in_with"
       data-shape="rectangular"
       data-logo_alignment="left">
  </div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
// import axios from 'axios'; // دیگر نیازی نیست
import axiosInstance from '@/utils/axiosInstance'; // یا مسیر دقیق شما

const router = useRouter();
const clientId = import.meta.env.VITE_GOOGLE_OAUTH_CLIENT_ID;

function handleCredentialResponse(response) {
  console.log("ID Token Received:", response.credential);

  // استفاده از axiosInstance با baseURL
  axiosInstance.post('/auth/google/login/', { // فقط مسیر نسبی
    id_token: response.credential
  })
  .then(response => {
    console.log("JWT Received:", response.data);
    localStorage.setItem('auth', response.data.access_token);
    localStorage.setItem('refresh', response.data.refresh_token);
    router.push('/');
  })
  .catch(error => {
    if (error.response) {
      console.error("Login Error (Response):", error.response.status, error.response.data);
    } else if (error.request) {
      console.error("Login Error (Request):", error.request);
    } else {
      console.error("Login Error (Setup):", error.message);
    }
  });
}

onMounted(() => {
  window.handleCredentialResponse = handleCredentialResponse;
});

onUnmounted(() => {
  delete window.handleCredentialResponse;
});
</script>