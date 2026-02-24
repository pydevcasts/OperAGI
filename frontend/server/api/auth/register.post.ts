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
    console.error('Full Django error response:', {
      status: err.status,
      statusText: err.statusText,
      data: err.data,                // ← مهم: کل data رو ببین
      message: err.message
    });

    // اگر err.data وجود داشت، پیام‌های خطا رو استخراج کن
    let errorMessage = 'خطا در ثبت‌نام';
    if (err.data) {
      if (err.data.email) errorMessage = err.data.email[0];
      else if (err.data.password1) errorMessage = err.data.password1[0];
      else if (err.data.non_field_errors) errorMessage = err.data.non_field_errors[0];
      else if (err.data.detail) errorMessage = err.data.detail;
    }

    throw createError({
      statusCode: err.status || 400,
      message: errorMessage
    });
  }
})