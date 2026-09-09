<script setup lang="ts">
defineProps<{ label: string; value: string | number; detail?: string; tone?: string }>()
</script>
<template><article :class="['metric-card', tone || 'violet']"><span>{{ label }}</span><strong>{{ value }}</strong><small>{{ detail }}</small></article></template>
