<!-- components/DocumentList.vue -->
<template>
  <div class="mb-6">
    <h3 class="text-lg font-bold mb-2">اسناد من</h3>
    <div v-if="documentStore.documents.length === 0" class="text-gray-500">
      هیچ سندی آپلود نشده است.
    </div>
    <div v-else class="space-y-2">
      <button
        v-for="doc in documentStore.documents"
        :key="doc.id"
        @click="chatStore.setDocument(doc.id)"
        :class="{
          'bg-indigo-700': chatStore.currentDocumentId === doc.id,
          'bg-gray-700 hover:bg-gray-600': chatStore.currentDocumentId !== doc.id
        }"
        class="w-full text-left p-3 rounded"
      >
        {{ doc.title }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useDocumentStore } from '../../stores/documentStore'
import { useChatStore } from '../../stores/chatStore'
const documentStore = useDocumentStore()
const chatStore = useChatStore()
</script>