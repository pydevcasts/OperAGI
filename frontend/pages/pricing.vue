<script setup lang="ts">
import type { Plan } from '~/types/phase1'
definePageMeta({ middleware: 'auth', layout: 'app' })
const { request } = usePhaseApi()
const { data: plans } = await useAsyncData('plans', () => request<Plan[]>('plans/'))
const selected = ref('')
async function choose(slug: string) { const result = await request<any>('subscription/', { method: 'POST', body: { plan: slug } }); selected.value = result.subscription.plan.name }
</script>
<template><div><PageHeader eyebrow="Simple pricing" title="Choose a plan that grows with you" description="Start with a 14-day local trial. Payment collection is intentionally not enabled until Stripe credentials are configured." />
  <p v-if="selected" class="notice success">{{ selected }} trial activated.</p><div class="pricing-grid"><article v-for="plan in plans" :key="plan.id" :class="['panel', 'price-card', { featured: plan.slug === 'pro' }]"><span v-if="plan.slug === 'pro'" class="recommended">Most popular</span><h2>{{ plan.name }}</h2><p class="price"><b>${{ Number(plan.price).toFixed(0) }}</b><span>/ month</span></p><ul><li v-for="feature in plan.features" :key="feature">✓ {{ feature }}</li></ul><button class="button primary full" @click="choose(plan.slug)">Start 14-day trial</button></article></div>
</div></template>
