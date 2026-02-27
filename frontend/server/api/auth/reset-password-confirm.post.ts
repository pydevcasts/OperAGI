export default defineEventHandler(async (event) => {
  const body = await readBody(event)

  try {
    const res = await $fetch('http://127.0.0.1:8000/api/v1/rest-auth/password/reset/confirm/', {
      method: 'POST',
      body: {
        uid: body.uid,
        token: body.token,
        new_password1: body.new_password1,
        new_password2: body.new_password2
      }
    })
    return { success: true }
  } catch (err: any) {
    console.error('Reset confirm error:', err.data)
    throw createError({
      statusCode: 400,
      data: err.data,
      message: err.data?.token?.[0] || 'Faile to change password'
    })
  }
})