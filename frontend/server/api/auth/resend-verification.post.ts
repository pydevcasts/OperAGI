export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  console.log('Resend verification for:', body.email)

  try {
    const res = await $fetch('http://127.0.0.1:8000/api/v1/rest-auth/registration/resend-email/', {
      method: 'POST',
      body: { email: body.email },
      headers: { 'Content-Type': 'application/json' }
    })
    console.log('Resend response:', res)
    return { success: true }
  } catch (err: any) {
    console.error('Resend error:', JSON.stringify(err.data, null, 2))
    throw createError({
      statusCode: err.status || 400,
      message: err.data?.detail || err.data?.email?.[0] || 'خطا در ارسال ایمیل'
    })
  }
})