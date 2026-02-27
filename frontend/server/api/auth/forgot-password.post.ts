export default defineEventHandler(async (event) => {
  const body = await readBody(event)

  try {
    const res = await $fetch('http://127.0.0.1:8000/api/v1/rest-auth/password/reset/', {
      method: 'POST',
      body: { email: body.email },
      headers: { 'Content-Type': 'application/json' }
    })

    return { 
      success: true, 
      message: 'Recovery link has been sent to your email.' 
    }
  } catch (err: any) {
    console.error('Forgot password error:', err.data)
    
    // استخراج پیام خطا از پاسخ سرور (معمولاً Django REST Framework ساختار { field: [messages] } دارد)
    let errorMessage = 'Error sending email. Please try again.'
    
    if (err.data) {
      // اگر خطا روی فیلد email باشد
      if (err.data.email && Array.isArray(err.data.email)) {
        errorMessage = err.data.email[0]
      } 
      // یا پیام کلی
      else if (err.data.detail) {
        errorMessage = err.data.detail
      } 
      // یا پیام‌های دیگر
      else if (err.data.non_field_errors && Array.isArray(err.data.non_field_errors)) {
        errorMessage = err.data.non_field_errors[0]
      }
    }

    throw createError({
      statusCode: 400,
      message: errorMessage
    })
  }
})