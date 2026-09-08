<script setup lang="ts">
definePageMeta({ middleware: 'auth', layout: 'app' })
const steps = [{ title: 'Connect a channel', text: 'Add an Instagram, X, or YouTube identity.', to: '/connections' }, { title: 'Create your first post', text: 'Generate in English or Persian with the local provider.', to: '/create' }, { title: 'Plan your week', text: 'Place approved content on the publishing calendar.', to: '/calendar' }]
</script>
<template><div><PageHeader eyebrow="Welcome to OperAGI" title="Launch your creator workflow" description="Three quick steps take you from an idea to a measurable content calendar."/><div class="onboarding-list"><article v-for="(step, i) in steps" :key="step.title" class="panel onboarding-step"><span class="step-number">0{{ i + 1 }}</span><div class="grow"><h2>{{ step.title }}</h2><p>{{ step.text }}</p></div><NuxtLink class="button secondary" :to="step.to">Continue →</NuxtLink></article></div></div></template>
