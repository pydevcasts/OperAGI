export function usePhaseApi() {
  const request = <T>(path: string, options: Record<string, any> = {}) =>
    $fetch<T>(`/api/phase1/${path.replace(/^\//, '')}`, options)
  return { request }
}
