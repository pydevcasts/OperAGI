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

    // Extract error messages from Django response (DRF format)
    let errorMessage = 'Registration failed. Please try again.'

    if (err.data) {
      // Priority: field-specific errors
      if (err.data.email && Array.isArray(err.data.email)) {
        errorMessage = err.data.email[0]
      } else if (err.data.password1 && Array.isArray(err.data.password1)) {
        errorMessage = err.data.password1[0]
      } else if (err.data.password2 && Array.isArray(err.data.password2)) {
        errorMessage = err.data.password2[0]
      } 
      // Non-field errors (common for password mismatch, etc.)
      else if (err.data.non_field_errors && Array.isArray(err.data.non_field_errors)) {
        errorMessage = err.data.non_field_errors[0]
      } 
      // Generic detail
      else if (err.data.detail) {
        errorMessage = err.data.detail
      }
    }

    throw createError({
      statusCode: err.status || 400,
      message: errorMessage
    })
  }
})