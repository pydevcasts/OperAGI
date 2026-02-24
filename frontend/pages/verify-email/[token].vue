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
    error.value = 'لینک تأیید نامعتبر یا منقضی شده است.'
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
          <p class="state-text">در حال تأیید ایمیل...</p>
        </div>

        <!-- Success -->
        <div v-else-if="success" class="state-box">
          <div class="success-icon">
            <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
              <circle cx="16" cy="16" r="15" stroke="#34d399" stroke-width="1.5"/>
              <path d="M9 16l5 5 9-9" stroke="#34d399" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <h2 class="state-title">ایمیل تأیید شد!</h2>
          <p class="state-desc">حساب شما با موفقیت فعال شد.</p>
          <NuxtLink to="/login" class="submit-btn">ورود به حساب</NuxtLink>
        </div>

        <!-- Error -->
        <div v-else class="state-box">
          <div class="error-icon">
            <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
              <circle cx="16" cy="16" r="15" stroke="#f87171" stroke-width="1.5"/>
              <path d="M10 10l12 12M22 10L10 22" stroke="#f87171" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </div>
          <h2 class="state-title">لینک نامعتبر است</h2>
          <p class="state-desc">{{ error }}</p>
          <NuxtLink to="/login" class="submit-btn">برگشت به ورود</NuxtLink>
        </div>

      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700&display=swap');
*, *::before, *::after { box-sizing: border-box; }
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
.bg-orb { position: absolute; border-radius: 50%; filter: blur(80px); pointer-events: none; }
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
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-30px); }
}
.container {
  width: 100%; max-width: 420px;
  display: flex; flex-direction: column;
  align-items: center; gap: 1.5rem;
  position: relative; z-index: 1;
  animation: fadeUp 0.5s ease forwards;
}
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.brand { display: flex; align-items: center; gap: 0.6rem; }
.brand-icon {
  width: 44px; height: 44px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  color: white;
  box-shadow: 0 8px 24px rgba(99,102,241,0.35);
}
.brand-name {
  font-size: 1.4rem; font-weight: 700;
  background: linear-gradient(135deg, #e2e8f0, #94a3b8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.card {
  width: 100%;
  background: rgba(15,20,35,0.85);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 20px;
  padding: 2.5rem 2rem;
  backdrop-filter: blur(20px);
  box-shadow: 0 25px 60px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.06);
}
.state-box {
  display: flex; flex-direction: column;
  align-items: center; text-align: center;
  gap: 0.75rem;
}
.spinner {
  width: 48px; height: 48px;
  border: 3px solid rgba(99,102,241,0.2);
  border-top-color: #6366f1;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 0.5rem;
}
@keyframes spin { to { transform: rotate(360deg); } }
.success-icon, .error-icon {
  width: 64px; height: 64px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  margin-bottom: 0.5rem;
  animation: popIn 0.4s cubic-bezier(0.175,0.885,0.32,1.275) forwards;
}
.success-icon { background: rgba(16,185,129,0.1); }
.error-icon { background: rgba(239,68,68,0.1); }
@keyframes popIn {
  from { transform: scale(0.5); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}
.state-title { font-size: 1.3rem; font-weight: 700; color: #f1f5f9; margin: 0; }
.state-text { font-size: 0.9rem; color: #64748b; margin: 0; }
.state-desc { font-size: 0.875rem; color: #64748b; margin: 0; }
.submit-btn {
  margin-top: 0.75rem;
  display: inline-flex; align-items: center; justify-content: center;
  padding: 0.75rem 2rem;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border: none; border-radius: 10px;
  color: white; text-decoration: none;
  font-family: 'Vazirmatn', sans-serif;
  font-size: 0.9rem; font-weight: 600;
  box-shadow: 0 4px 20px rgba(99,102,241,0.35);
  transition: opacity 0.2s, transform 0.15s;
}
.submit-btn:hover { opacity: 0.9; transform: translateY(-1px); }
</style>