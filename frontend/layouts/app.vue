<script setup lang="ts">
const mobileOpen = ref(false)
</script>

<template>
  <div class="phase-shell">
    <AppSidebar :open="mobileOpen" @close="mobileOpen = false" />
    <div class="phase-main">
      <header class="phase-topbar">
        <button class="icon-button mobile-menu" aria-label="Open navigation" @click="mobileOpen = true">☰</button>
        <div class="topbar-context"><span class="topbar-kicker">WORKSPACE</span><strong>Creator workspace</strong></div>
        <div class="topbar-actions"><span class="topbar-help">Need inspiration? <NuxtLink to="/create">Start with an idea</NuxtLink></span><NuxtLink class="button primary compact" to="/create">+ Create content</NuxtLink></div>
      </header>
      <main class="phase-content"><slot /></main>
    </div>
  </div>
</template>
