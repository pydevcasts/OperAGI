export default defineEventHandler(async (event) => {
  const body = await readBody(event)

  try {
    const res = await $fetch('http://127.0.0.1:8000/api/v1/rest-auth/password/reset/', {
      method: 'POST',
      body: { email: body.email },
      headers: { 'Content-Type': 'application/json' }
    })

    return { success: true, message: 'لینک بازیابی به ایمیل شما ارسال شد.' }
  } catch (err: any) {
    console.error('Forgot password error:', err.data)
    throw createError({
      statusCode: 400,
      message: err.data?.email?.[0] || 'خطا در ارسال ایمیل'
    })
  }
})