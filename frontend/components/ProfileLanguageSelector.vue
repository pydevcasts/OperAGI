<!-- components/ProfileLanguageSelector.vue -->
<template>
  <div class="flex gap-2 mb-2">
    <select v-model="chatStore.profile" class="bg-gray-800 text-white p-1 rounded">
      <option value="quick">سریع</option>
      <option value="balanced">متعادل</option>
      <option value="detailed">مفصل</option>
      <option value="creative">خلاقانه</option>
    </select>
    <select v-model="chatStore.language" class="bg-gray-800 text-white p-1 rounded">
      <option value="fa">فارسی</option>
      <option value="en">English</option>
    </select>
  </div>
</template>

<script setup lang="ts">
import { useChatStore } from '../stores/chatStore'
const chatStore = useChatStore()
</script>