// stores/chatStore.ts
import { defineStore } from 'pinia'
import type { Message, Profile, Language } from '~/types'

export const useChatStore = defineStore('chat', () => {
  const messages = ref<Message[]>([])
  const loading = ref(false)
  const currentDocumentId = ref<number | null>(null)
  const profile = ref<Profile>('balanced')
  const language = ref<Language>('fa')

  const ask = async (question: string) => {
    if (!currentDocumentId.value) return

    messages.value.push({
      id: Date.now().toString(),
      role: 'user',
      content: question,
      timestamp: new Date()
    })
    loading.value = true

    try {
      const res = await $fetch<{ answer: string }>('/api/v1/qa/ask/', {
        method: 'POST',
        body: {
          document_id: currentDocumentId.value,
          question,
          profile: profile.value,
          language: language.value
        }
      })

      messages.value.push({
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: res.answer,
        timestamp: new Date()
      })
    } catch (err) {
      console.error('Error:', err)
    } finally {
      loading.value = false
    }
  }

  const setDocument = (id: number) => {
    currentDocumentId.value = id
    messages.value = []
  }

  return {
    messages,
    loading,
    currentDocumentId,
    profile,
    language,
    ask,
    setDocument
  }
})