<script setup lang="ts">
defineProps<{ open: boolean }>()
defineEmits<{ close: [] }>()
const route = useRoute()
const { user } = useUserSession()
const auth = useAuthStore()
const nav = [
  ['/dashboard', 'Overview', '⌂'], ['/create', 'Create content', '✦'], ['/calendar', 'Calendar', '□'],
  ['/connections', 'Connections', '◎'], ['/analytics', 'Analytics', '↗'], ['/pricing', 'Plans', '◇'],
]
</script>

<template>
  <div v-if="open" class="sidebar-scrim" @click="$emit('close')" />
  <aside :class="['phase-sidebar', { open }]">
    <NuxtLink to="/dashboard" class="phase-brand"><span class="brand-glyph">O</span><span>OperAGI<small>Influencer Copilot</small></span></NuxtLink>
    <div class="sidebar-section-label">WORKSPACE</div>
    <nav>
      <NuxtLink v-for="item in nav" :key="item[0]" :to="item[0]" :class="{ active: route.path === item[0] }" @click="$emit('close')">
        <span>{{ item[2] }}</span>{{ item[1] }}
      </NuxtLink>
    </nav>
    <div class="sidebar-account">
      <div class="avatar">{{ String((user as any)?.email || 'U')[0].toUpperCase() }}</div>
      <div><strong>{{ (user as any)?.name || 'Creator' }}</strong><small>{{ (user as any)?.email }}</small></div>
      <button class="icon-button" title="Sign out" @click="auth.logout">↪</button>
    </div>
  </aside>
</template>
