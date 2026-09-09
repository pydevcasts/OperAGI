export function usePhaseApi() {
  const request = <T>(path: string, options: Record<string, any> = {}) => {
    const normalizedPath = path.replace(/^\/+/, '')
    // Keep requests same-origin so Nuxt can read the secure session cookie,
    // attach the Django access token, and proxy the request server-side.
    return $fetch<T>(`/api/phase1/${normalizedPath}`, options)
  }

  return { request }
}
