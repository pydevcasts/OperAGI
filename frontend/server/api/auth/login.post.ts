import { readBody } from 'h3'

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const { email, password } = body

  if (!email || !password) {
    throw createError({ statusCode: 400, message: 'Email and password required' })
  }

  console.log('Sending credentials to Django:', { email, password: '***' })

  let djangoRes: any

  try {
    djangoRes = await $fetch('http://127.0.0.1:8000/api/v1/rest-auth/login/', {
      method: 'POST',
      body: { email, password },
      headers: { 'Content-Type': 'application/json' }
    })
  } catch (err: any) {
    // ← اینجا پیام دقیق Django رو لاگ میکنیم
    console.error('Django login error:', JSON.stringify(err.data, null, 2))

    const djangoMessage = err.data?.non_field_errors?.[0] || err.data?.detail || ''

    const isUnverified =
      djangoMessage.toLowerCase().includes('e-mail') ||
      djangoMessage.toLowerCase().includes('verif') ||
      djangoMessage.toLowerCase().includes('confirm')

    if (isUnverified) {
      throw createError({ statusCode: 403, message: 'email_not_verified' })
    }

    throw createError({ statusCode: 401, message: djangoMessage || 'Invalid credentials' })
  }

  // ← اگه به اینجا رسیدیم یعنی لاگین موفق بود
  if (!djangoRes.access) {
    throw createError({ statusCode: 502, message: 'No access token from Django' })
  }

  await setUserSession(event, {
    user: {
      email,
      name: djangoRes.user?.first_name || email.split('@')[0],
      is_email_verified: true
    },
    tokens: {
      access: djangoRes.access,
      refresh: djangoRes.refresh || null
    },
    authProvider: 'credentials',
    lastLogin: new Date().toISOString()
  })

  console.log('Session successfully set')
  return { success: true }
})