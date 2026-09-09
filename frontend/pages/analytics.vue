<script setup lang="ts">
import type { AnalyticsSnapshot, Platform } from '~/types/phase1'
definePageMeta({ middleware: 'auth', layout: 'app' })
const { request } = usePhaseApi()
const { data } = await useAsyncData('analytics', () => request<AnalyticsSnapshot[]>('content_generator/analytics/'))
const totals = computed(() => (data.value || []).reduce((a, row) => ({ reach: a.reach + row.reach, impressions: a.impressions + row.impressions, engagement: a.engagement + row.likes + row.comments + row.shares + row.clicks }), { reach: 0, impressions: 0, engagement: 0 }))
const byPlatform = computed(() => (['instagram','twitter','youtube'] as Platform[]).map(platform => ({ platform, rows: (data.value || []).filter(row => row.platform === platform) })).map(item => ({ platform: item.platform, reach: item.rows.reduce((n, r) => n + r.reach, 0), engagement: item.rows.reduce((n, r) => n + r.likes + r.comments + r.shares + r.clicks, 0) })))
</script>
<template><div><PageHeader eyebrow="Performance" title="Analytics" description="Compare reach and engagement from imported or API-synced snapshots." />
  <div class="metrics-grid"><MetricCard label="Reach" :value="totals.reach.toLocaleString()" detail="Unique audience"/><MetricCard label="Impressions" :value="totals.impressions.toLocaleString()" detail="Content views" tone="blue"/><MetricCard label="Engagements" :value="totals.engagement.toLocaleString()" detail="Likes, comments, shares and clicks" tone="green"/></div>
  <section class="panel"><div class="panel-heading"><div><h2>Channel comparison</h2><p>Performance by platform.</p></div></div><div class="chart-list"><div v-for="item in byPlatform" :key="item.platform" class="chart-row"><PlatformBadge :platform="item.platform"/><div class="bar-track"><div class="bar-fill" :style="{ width: `${Math.min(100, totals.reach ? item.reach / totals.reach * 100 : 0)}%` }"/></div><b>{{ item.reach.toLocaleString() }}</b><small>{{ item.engagement }} engagements</small></div></div><div v-if="!data?.length" class="empty-state compact-empty"><strong>No analytics yet</strong><span>Snapshots appear after publishing or can be added through the REST API.</span></div></section>
</div></template>
