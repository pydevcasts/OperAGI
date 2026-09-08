<script setup lang="ts">
import type { Platform, SocialConnection } from '~/types/phase1'
definePageMeta({ middleware: 'auth', layout: 'app' })
const { request } = usePhaseApi()
const { data: connections, refresh } = await useAsyncData('connections', () => request<SocialConnection[]>('social/user-social-accounts/'))
const form = reactive({ provider: 'instagram' as Platform, uid: '', display_name: '' })
const message = ref('')
const platforms: Array<{ id: Platform; text: string }> = [{ id: 'instagram', text: 'Captions, hashtags and optimal timing' }, { id: 'twitter', text: 'Tweets, threads and scheduling' }, { id: 'youtube', text: 'SEO titles and descriptions' }]
function connectionFor(platform: Platform) { return connections.value?.find(item => item.provider === platform) }
async function connect() { await request('social/user-social-accounts/', { method: 'POST', body: { social_account: { provider: form.provider, uid: form.uid, extra_data: { username: form.display_name } }, display_name: form.display_name } }); form.uid = ''; form.display_name = ''; message.value = 'Account connected.'; await refresh() }
async function disconnect(id: number) { await request(`social/user-social-accounts/${id}/`, { method: 'DELETE' }); await refresh() }
</script>
<template><div><PageHeader eyebrow="Channels" title="Social connections" description="OAuth-ready account records with a local connection flow for development and demos." />
  <div class="connection-grid"><article v-for="platform in platforms" :key="platform.id" class="panel connection-card"><PlatformBadge :platform="platform.id"/><h2>{{ platform.id === 'twitter' ? 'X / Twitter' : platform.id[0].toUpperCase() + platform.id.slice(1) }}</h2><p>{{ platform.text }}</p><template v-if="connectionFor(platform.id)"><div class="connected-state"><span class="live-dot"/>{{ connectionFor(platform.id)?.display_name || connectionFor(platform.id)?.social_account.uid }}</div><button class="button secondary" @click="disconnect(connectionFor(platform.id)!.id)">Disconnect</button></template><button v-else class="button primary" @click="form.provider = platform.id; (document.getElementById('connection-form') as HTMLElement)?.scrollIntoView({ behavior: 'smooth' })">Connect</button></article></div>
  <form id="connection-form" class="panel form-panel narrow" @submit.prevent="connect"><div class="panel-heading"><div><h2>Local / manual connection</h2><p>Useful without external OAuth keys. Never enter passwords or access tokens.</p></div></div><label>Platform<select v-model="form.provider"><option v-for="p in platforms" :key="p.id" :value="p.id">{{ p.id }}</option></select></label><label>Public account ID or handle<input v-model="form.uid" required placeholder="@creator or channel ID"></label><label>Display name<input v-model="form.display_name" placeholder="Creator Studio"></label><button class="button primary" :disabled="!form.uid">Save connection</button><p v-if="message" class="notice">{{ message }}</p></form>
</div></template>
