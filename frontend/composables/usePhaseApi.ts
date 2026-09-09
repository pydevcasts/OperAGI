export function usePhaseApi() {
  const config = useRuntimeConfig()
  const request = <T>(path: string, options: Record<string, any> = {}) => {
    const normalizedPath = path.replace(/^\/+/, '')
    const base = String(config.public.API_BASE_URL || '').replace(/\/$/, '')
    const url = base ? `${base}/${normalizedPath}` : `/api/v1/${normalizedPath}`
    return $fetch<T>(url, options)
  }

  return { request }
}
