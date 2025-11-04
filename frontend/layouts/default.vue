<!-- layouts/default.vue -->
<script setup lang="ts">
onMounted(() => {
  if (!document.getElementById('google-gsi')) {
    const script = document.createElement('script')
    script.id = 'google-gsi'
    script.src = 'https://accounts.google.com/gsi/client'
    script.async = true
    script.defer = true

    script.onload = () => {
      console.log('Google GIS loaded')
      // بعد از لود، event بفرست
      window.dispatchEvent(new Event('google-gsi-loaded'))
    }

    document.head.appendChild(script)
  }
})
</script>

<template>
  <slot />
</template>