// stores/documentStore.ts
import { defineStore } from 'pinia'
import type { Document } from '~/types'

export const useDocumentStore = defineStore('document', () => {
  const documents = ref<Document[]>([])
  const loading = ref(false)

  const fetchDocuments = async () => {
    try {
      const data = await $fetch<Document[]>('/api/v1/documents/')
      documents.value = data
    } catch (err) {
      console.error('Failed to fetch documents', err)
    }
  }

  const uploadDocument = async (file: File, title: string) => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('title', title)

    const doc = await $fetch<Document>('/api/v1/documents/upload/', {
      method: 'POST',
      body: formData
    })
    documents.value.push(doc)
    return doc
  }

  return { documents, loading, fetchDocuments, uploadDocument }
})