// server/api/auth/register.post.ts
export default defineEventHandler(async (event) => {
  const body = await readBody(event)

  try {
    const res = await $fetch('http://127.0.0.1:8000/api/v1/rest-auth/registration/', {
      method: 'POST',
      body: {
      
        email: body.email,
        password1: body.password,
        password2: body.password
      },
      headers: { 'Content-Type': 'application/json' }
    })

    return { success: true, data: res }
  } catch (err: any) {
    // ← این رو اضافه کن تا ببینی Django چی میگه
    console.error('Django registration error:', JSON.stringify(err.data, null, 2))
    
    throw createError({
      statusCode: err.status || 400,
      data: err.data, // ← کل data رو برگردون
      message: err.data?.email?.[0] || err.data?.password1?.[0] || err.data?.non_field_errors?.[0] || 'خطا در ثبت‌نام'
    })
  }
})