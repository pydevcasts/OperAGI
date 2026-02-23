// server/api/auth/login.post.ts
import { readBody } from 'h3'

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const { email, password } = body

  if (!email || !password) {
    throw createError({ statusCode: 400, message: 'Email and password required' })
  }

  console.log('Sending credentials to Django:', { email, password: '***' })
try {
  const djangoRes = await $fetch('http://127.0.0.1:8000/api/v1/rest-auth/login/', {
    method: 'POST',
    body: { email, password },
    headers: { 'Content-Type': 'application/json' }
  })

  console.log('Raw Django response:', JSON.stringify(djangoRes, null, 2))

  if (!djangoRes.access) {
    console.log('No access token in djangoRes!')
    throw createError({ statusCode: 502, message: 'No access token from Django' })
  }

  console.log('Access token found:', djangoRes.access.substring(0, 20) + '...')

  await setUserSession(event, {
    user: { email, name: email.split('@')[0] },
    tokens: {
      access: djangoRes.access,
      refresh: djangoRes.refresh || null
    },
    authProvider: 'credentials',
    lastLogin: new Date().toISOString()
  })

  console.log('Session successfully set with tokens')
  return { success: true }
} catch (err) {
  console.error('Login route error:', err)
  throw createError({ statusCode: 401, message: 'Invalid credentials' })
}

})