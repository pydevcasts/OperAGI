import { getMethod, getQuery, getRouterParam, readBody } from 'h3'

export default defineEventHandler(async (event) => {
  const session = await requireUserSession(event) as any
  const access = session?.tokens?.access
  if (!access) throw createError({ statusCode: 401, message: 'Authentication required' })

  const path = getRouterParam(event, 'path') || ''
  const method = getMethod(event)
  const base = process.env.NUXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000/api/v1'
  try {
    return await $fetch(`${base.replace(/\/$/, '')}/${path}`, {
      method: method as any,
      query: getQuery(event),
      body: ['GET', 'HEAD'].includes(method) ? undefined : await readBody(event),
      headers: { Authorization: `Bearer ${access}` },
    })
  } catch (error: any) {
    throw createError({
      statusCode: error?.response?.status || error?.statusCode || 502,
      statusMessage: error?.data?.detail || error?.data?.message || 'Backend request failed',
      data: error?.data,
    })
  }
})
