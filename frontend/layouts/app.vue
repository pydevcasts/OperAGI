<script setup lang="ts">
const mobileOpen = ref(false)
</script>

<template>
  <div class="phase-shell">
    <AppSidebar :open="mobileOpen" @close="mobileOpen = false" />
    <div class="phase-main">
      <header class="phase-topbar">
        <button class="icon-button mobile-menu" aria-label="Open navigation" @click="mobileOpen = true">☰</button>
        <div><strong>OperAGI</strong><span class="muted topbar-sub"> Creator workspace</span></div>
        <NuxtLink class="button primary compact" to="/create">+ Create content</NuxtLink>
      </header>
      <main class="phase-content"><slot /></main>
    </div>
  </div>
</template>
