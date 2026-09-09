<script setup lang="ts">
import type { DashboardData } from '~/types/phase1'
definePageMeta({ middleware: 'auth', layout: 'app' })
const { request } = usePhaseApi()
const { data, pending, error, refresh } = await useAsyncData('phase-dashboard', () => request<DashboardData>('content_generator/dashboard/'))
const summary = computed(() => data.value?.summary || {})
</script>

<template><div>
  <PageHeader eyebrow="Phase 1 workspace" title="Your content command center" description="Generate, schedule, and measure content across every connected channel." />
  <div v-if="error" class="notice danger">Could not load dashboard. <button @click="refresh">Retry</button></div>
  <div class="metrics-grid" :class="{ skeleton: pending }">
    <MetricCard label="Connected accounts" :value="summary.connected_accounts || 0" detail="Instagram, X and YouTube" />
    <MetricCard label="Generated" :value="summary.posts_generated || 0" detail="Ready for review" tone="blue" />
    <MetricCard label="Scheduled" :value="summary.posts_scheduled || 0" detail="Queued to publish" tone="amber" />
    <MetricCard label="Total reach" :value="data?.analytics?.reach || 0" detail="Across analytics snapshots" tone="green" />
  </div>
  <div class="two-column">
    <section class="panel"><div class="panel-heading"><div><h2>Recent content</h2><p>Your latest drafts and generated posts.</p></div><NuxtLink to="/create">Create new</NuxtLink></div>
      <div v-if="!data?.recent_posts?.length" class="empty-state"><strong>Your content starts here</strong><span>Generate a platform-ready first draft without an API key.</span><NuxtLink class="button primary" to="/create">Generate content</NuxtLink></div>
      <div v-else class="stack-list"><article v-for="post in data.recent_posts" :key="post.id" class="list-row"><PlatformBadge :platform="post.platform"/><div class="grow"><strong>{{ post.generated_content?.title || post.content }}</strong><small>{{ new Date(post.created_at).toLocaleString() }}</small></div><span class="status-pill">{{ post.status.replaceAll('_', ' ') }}</span></article></div>
    </section>
    <section class="panel"><div class="panel-heading"><div><h2>Up next</h2><p>Your publishing queue.</p></div><NuxtLink to="/calendar">Calendar</NuxtLink></div>
      <div v-if="!data?.upcoming?.length" class="empty-state compact-empty"><strong>No scheduled posts</strong><span>Schedule approved content from the editor.</span></div>
      <div v-else class="stack-list"><article v-for="item in data.upcoming" :key="item.id" class="list-row"><div class="date-tile"><b>{{ new Date(item.scheduled_for).getDate() }}</b><span>{{ new Date(item.scheduled_for).toLocaleString('en', { month: 'short' }) }}</span></div><div class="grow"><PlatformBadge :platform="item.post.platform"/><small>{{ new Date(item.scheduled_for).toLocaleString() }}</small></div></article></div>
    </section>
  </div>
</div></template>
