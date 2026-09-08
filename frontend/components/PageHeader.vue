<script setup lang="ts">
defineProps<{ eyebrow?: string; title: string; description: string }>()
</script>
<template><header class="page-header"><p v-if="eyebrow" class="eyebrow">{{ eyebrow }}</p><h1>{{ title }}</h1><p>{{ description }}</p><slot /></header></template>
