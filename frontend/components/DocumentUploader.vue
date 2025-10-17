<!-- components/DocumentUploader.vue -->
<template>
  <form @submit.prevent="handleSubmit" class="mb-6 p-4 bg-gray-800 rounded">
    <input
      v-model="title"
      placeholder="عنوان سند (مثلاً: راهنمای هوش مصنوعی)"
      class="w-full p-2 mb-2 rounded bg-gray-700 text-white placeholder-gray-400"
      required
    />
    <input
      type="file"
      @change="onFileChange"
      accept=".pdf"
      class="mb-2 w-full text-white"
      required
    />
    <button
      type="submit"
      :disabled="!file || loading"
      class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 rounded disabled:opacity-50"
    >
      {{ loading ? 'در حال آپلود...' : 'آپلود PDF' }}
    </button>
  </form>
</template>

<script setup lang="ts">
import { useDocumentStore } from '../stores/documentStore'
import { useChatStore } from '../stores/chatStore'

const title = ref('')
const file = ref<File | null>(null)
const loading = ref(false)

const documentStore = useDocumentStore()
const chatStore = useChatStore()

const onFileChange = (e: Event) => {
  const target = e.target as HTMLInputElement
  file.value = target.files?.[0] || null
}

const handleSubmit = async () => {
  if (!file.value || !title.value) return
  loading.value = true
  try {
    const doc = await documentStore.uploadDocument(file.value, title.value)
    chatStore.setDocument(doc.id)
    title.value = ''
    file.value = null
  } finally {
    loading.value = false
  }
}
</script>