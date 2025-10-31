<!-- components/ChatInterface.vue -->
<template>
  <div v-if="chatStore.currentDocumentId" class="flex-1 flex flex-col bg-gray-900 rounded">
    <!-- Messages -->
    <div class="flex-1 overflow-y-auto p-4 space-y-4">
      <div v-for="msg in chatStore.messages" :key="msg.id" class="flex" :class="{
        'justify-end': msg.role === 'user',
        'justify-start': msg.role === 'assistant'
      }">
        <div
          :class="{
            'bg-indigo-600': msg.role === 'user',
            'bg-gray-700': msg.role === 'assistant'
          }"
          class="max-w-[80%] p-3 rounded"
        >
          {{ msg.content }}
        </div>
      </div>
      <div v-if="chatStore.loading" class="flex justify-start">
        <div class="bg-gray-700 p-3 rounded">در حال پاسخ‌دهی...</div>
      </div>
    </div>

    <!-- Input -->
    <form @submit.prevent="handleSubmit" class="p-4 border-t border-gray-700">
      <input
        v-model="question"
        placeholder="سوال خود را بپرسید..."
        class="w-full p-2 mb-2 rounded bg-gray-800 text-white"
        :disabled="chatStore.loading"
        required
      />
      <ProfileLanguageSelector />
      <button
        type="submit"
        :disabled="!question.trim() || chatStore.loading"
        class="mt-2 px-4 py-2 bg-green-600 hover:bg-green-700 rounded disabled:opacity-50"
      >
        ارسال
      </button>
    </form>
  </div>
  <div v-else class="flex-1 flex items-center justify-center text-gray-500">
    لطفاً یک سند انتخاب کنید
  </div>
</template>

<script setup lang="ts">
import { useChatStore } from '../../stores/chatStore'

const question = ref('')
const chatStore = useChatStore()

const handleSubmit = async () => {
  if (!question.value.trim()) return
  await chatStore.ask(question.value)
  question.value = ''
}
</script>