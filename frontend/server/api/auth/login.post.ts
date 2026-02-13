// server/api/auth/login.post.ts
import { readBody } from 'h3'

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const { email, password } = body

  if (!email || !password) {
    throw createError({
      statusCode: 400,
      message: 'Email and password are required'
    })
  }

  try {
    // درخواست به Django
  const djangoRes = await $fetch('http://127.0.0.1:8000/api/v1/rest-auth/login/', {
  method: 'POST',
  body: {
    login: email,
    password
  },
  headers: { 'Content-Type': 'application/json' }
})

    if (!djangoRes.key) {
      throw new Error('No token received from backend')
    }

    // ذخیره session در cookie (server-side)
    await setUserSession(event, {
      user: {
        email,
        name: email.split('@')[0]
      },
      tokens: {
        access: djangoRes.key
        // اگر refresh هم داری: refresh: djangoRes.refresh_token
      },
      authProvider: 'credentials',
      lastLogin: new Date().toISOString()
    })

    return { success: true }
  } catch (err: any) {
    console.error('Backend login error:', err)
    throw createError({
      statusCode: 401,
      message: err.data?.non_field_errors?.[0] || 'Invalid credentials'
    })
  }
})