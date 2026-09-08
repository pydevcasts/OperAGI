<script setup lang="ts">
import type { ContentPost, Language, Platform, SocialConnection } from '~/types/phase1'
definePageMeta({ middleware: 'auth', layout: 'app' })
const { request } = usePhaseApi()
const form = reactive({ platform: 'instagram' as Platform, language: 'en' as Language, tone: 'professional', content: '', visual_idea: '', social_account_id: undefined as number | undefined })
const result = ref<ContentPost | null>(null)
const loading = ref(false)
const saving = ref(false)
const message = ref('')
const editorText = computed({
  get: () => result.value?.generated_content?.generated_text || result.value?.generated_content?.description || '',
  set: (value: string) => {
    if (!result.value?.generated_content) return
    if (form.platform === 'youtube') result.value.generated_content.description = value
    else result.value.generated_content.generated_text = value
  }
})
const { data: connections } = await useAsyncData('creator-connections', () => request<SocialConnection[]>('social/user-social-accounts/'))
const matchingConnections = computed(() => (connections.value || []).filter(item => item.provider === form.platform))
watch(() => form.platform, () => { form.social_account_id = matchingConnections.value[0]?.id })
async function generate() {
  if (!form.content.trim()) return
  loading.value = true; message.value = ''
  try {
    const post = await request<ContentPost>('content_generator/posts/', { method: 'POST', body: form })
    const response = await request<{ post: ContentPost }>(`content_generator/posts/${post.id}/generate/`, { method: 'POST' })
    result.value = response.post
  } catch (error: any) { message.value = error?.data?.statusMessage || 'Generation failed.' }
  finally { loading.value = false }
}
async function saveEdits() {
  const generated = result.value?.generated_content
  if (!generated) return
  saving.value = true
  try {
    await request(`content_generator/generated-content/${generated.id}/`, { method: 'PATCH', body: generated })
    message.value = 'Draft saved.'
  } finally { saving.value = false }
}
async function schedule() {
  if (!result.value) return
  const when = result.value.generated_content?.suggested_publish_time || new Date(Date.now() + 86400000).toISOString()
  await request('content_generator/schedules/', { method: 'POST', body: { post_id: result.value.id, scheduled_for: when, timezone: Intl.DateTimeFormat().resolvedOptions().timeZone } })
  message.value = 'Added to your publishing calendar.'
}
</script>

<template><div>
  <PageHeader eyebrow="AI studio" title="Create platform-ready content" description="Local generation works out of the box in English and Persian. Add an API provider later without changing your workflow." />
  <div class="editor-grid">
    <form class="panel form-panel" @submit.prevent="generate">
      <div class="segmented"><button v-for="platform in (['instagram','twitter','youtube'] as Platform[])" :key="platform" type="button" :class="{ active: form.platform === platform }" @click="form.platform = platform"><PlatformBadge :platform="platform" /></button></div>
      <label>Content idea<textarea v-model="form.content" rows="6" required placeholder="Describe the topic, offer, or story you want to share…" /></label>
      <div class="form-row"><label>Language<select v-model="form.language"><option value="en">English</option><option value="fa">فارسی</option></select></label><label>Tone<select v-model="form.tone"><option>professional</option><option>friendly</option><option>bold</option><option>educational</option></select></label></div>
      <label>Visual direction <input v-model="form.visual_idea" placeholder="Optional shot, thumbnail, or visual concept" /></label>
      <label>Publish from<select v-model="form.social_account_id"><option :value="undefined">No account (draft only)</option><option v-for="account in matchingConnections" :key="account.id" :value="account.id">{{ account.display_name || account.social_account.uid }}</option></select></label>
      <button class="button primary full" :disabled="loading || !form.content.trim()">{{ loading ? 'Creating draft…' : 'Generate content' }}</button>
      <p v-if="message" class="notice">{{ message }}</p>
    </form>
    <section class="panel preview-panel" :dir="form.language === 'fa' ? 'rtl' : 'ltr'">
      <div class="panel-heading"><div><h2>Live preview</h2><p>{{ result ? `Generated with ${result.generated_content?.provider}` : 'Your result will appear here.' }}</p></div><PlatformBadge :platform="form.platform" /></div>
      <div v-if="!result" class="phone-preview empty-state"><strong>Ready when you are</strong><span>Choose a platform, add your idea, and generate.</span></div>
      <div v-else class="generated-editor">
        <label v-if="form.platform === 'youtube'">Title<input v-model="result.generated_content.title" /></label>
        <label>{{ form.platform === 'youtube' ? 'Description' : 'Caption' }}<textarea v-model="editorText" rows="10" /></label>
        <label>Hashtags<input v-model="result.generated_content.suggested_hashtags" /></label>
        <div class="actions"><button class="button secondary" :disabled="saving" @click="saveEdits">Save edits</button><button class="button primary" @click="schedule">Schedule</button></div>
      </div>
    </section>
  </div>
</div></template>
