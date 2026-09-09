<script setup lang="ts">
definePageMeta({ middleware: 'auth' })
await navigateTo('/dashboard', { replace: true })
</script>
<template><div /></template>
