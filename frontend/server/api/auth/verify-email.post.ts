export default defineEventHandler(async (event) => {
  const body = await readBody(event)

  try {
    await $fetch('http://127.0.0.1:8000/api/v1/rest-auth/registration/verify-email/', {
      method: 'POST',
      body: { key: body.key },
      headers: { 'Content-Type': 'application/json' }
    })
    return { success: true }
  } catch (err: any) {
    console.error('Verify email error:', err.data)
    throw createError({
      statusCode: 400,
      message: 'لینک تأیید نامعتبر یا منقضی شده است.'
    })
  }
})