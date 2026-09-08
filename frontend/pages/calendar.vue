<script setup lang="ts">
import type { ContentPost, Schedule } from '~/types/phase1'
definePageMeta({ middleware: 'auth', layout: 'app' })
const { request } = usePhaseApi()
const { data: schedules, refresh } = await useAsyncData('schedules', () => request<Schedule[]>('content_generator/schedules/'))
const { data: posts } = await useAsyncData('schedulable-posts', () => request<ContentPost[]>('content_generator/posts/'))
const form = reactive({ post_id: undefined as number | undefined, scheduled_for: '', timezone: Intl.DateTimeFormat().resolvedOptions().timeZone })
const grouped = computed(() => {
  const groups: Record<string, Schedule[]> = {}
  for (const item of schedules.value || []) (groups[item.scheduled_for.slice(0, 10)] ||= []).push(item)
  return groups
})
async function addSchedule() { if (!form.post_id || !form.scheduled_for) return; await request('content_generator/schedules/', { method: 'POST', body: { ...form, scheduled_for: new Date(form.scheduled_for).toISOString() } }); form.post_id = undefined; form.scheduled_for = ''; await refresh() }
async function cancel(id: number) { await request(`content_generator/schedules/${id}/cancel/`, { method: 'POST' }); await refresh() }
</script>
<template><div><PageHeader eyebrow="Publishing" title="Content calendar" description="Review your queue and schedule approved drafts in your local timezone." />
  <section class="panel inline-form"><select v-model="form.post_id"><option :value="undefined">Select a post</option><option v-for="post in posts" :key="post.id" :value="post.id">{{ post.platform }} — {{ post.content.slice(0, 52) }}</option></select><input v-model="form.scheduled_for" type="datetime-local"><button class="button primary" @click="addSchedule">Add to calendar</button></section>
  <div v-if="!Object.keys(grouped).length" class="panel empty-state"><strong>Your calendar is clear</strong><span>Generate content first, then choose a publishing time.</span><NuxtLink class="button primary" to="/create">Create a post</NuxtLink></div>
  <section v-for="(items, date) in grouped" :key="date" class="calendar-day"><div class="calendar-date"><b>{{ new Date(date).toLocaleDateString('en', { weekday: 'short' }) }}</b><span>{{ new Date(date).toLocaleDateString('en', { month: 'short', day: 'numeric' }) }}</span></div><div class="calendar-items"><article v-for="item in items" :key="item.id" class="panel schedule-card"><span class="time">{{ new Date(item.scheduled_for).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }}</span><PlatformBadge :platform="item.post.platform"/><div class="grow"><strong>{{ item.post.generated_content?.title || item.post.content }}</strong><small>{{ item.status }} · {{ item.timezone }}</small></div><button v-if="item.status === 'queued'" class="text-button danger-text" @click="cancel(item.id)">Cancel</button></article></div></section>
</div></template>
