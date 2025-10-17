<!-- app.vue -->
<template>
  <div class="min-h-screen bg-gray-900 text-gray-100 p-6 font-sans">
    <header class="mb-6">
      <h1 class="text-2xl font-bold">🚀 Operagi — دستیار هوش مصنوعی محلی</h1>
      <p class="text-gray-400">همه چیز روی دستگاه شما — بدون اینترنت، بدون ردیابی</p>
    </header>

    <div class="flex gap-6 max-w-6xl mx-auto">
      <!-- Sidebar -->
      <div class="w-80 flex flex-col">
        <DocumentUploader />
        <DocumentList />
      </div>

      <!-- Chat Area -->
      <div class="flex-1 flex flex-col">
        <ChatInterface />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// ✅ این خطوط حیاتی هستند — کامپوننت‌ها را import می‌کنند
import DocumentUploader from '../components/DocumentUploader.vue'
import DocumentList from '../components/DocumentList.vue'
import ChatInterface from '../components/ChatInterface.vue'

// ✅ برای بارگذاری اسناد در ابتدا
import { useDocumentStore } from '../stores/documentStore'
import { onMounted } from 'vue'

const documentStore = useDocumentStore()
onMounted(() => {
  documentStore.fetchDocuments()
})
</script>