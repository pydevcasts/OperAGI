<script setup lang="ts">
import type { Platform } from '~/types/phase1'
defineProps<{ platform: Platform }>()
const labels = { instagram: 'Instagram', twitter: 'X / Twitter', youtube: 'YouTube' }
</script>
<template><span :class="['platform-badge', platform]">{{ labels[platform] }}</span></template>
