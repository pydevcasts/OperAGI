<script setup lang="ts">
const authStore = useAuthStore()
const router = useRouter()

onMounted(() => {
  if (!authStore.token) {
    router.push('/login')
  }
})
definePageMeta({
  middleware: 'auth'
})
</script>