// plugins/authFetch.client.ts
export default defineNuxtPlugin(() => {
  const accessToken = localStorage.getItem('accessToken')

  if (accessToken) {
    const originalFetch = globalThis.$fetch
    globalThis.$fetch = (url: string, options: any = {}) => {
      options.headers = {
        ...options.headers,
        Authorization: `Bearer ${accessToken}`  // ✅ Bearer + access
      }
      return originalFetch(url, options)
    }
  }
})