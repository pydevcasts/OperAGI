// server/api/auth/login.post.ts
import { readBody } from 'h3'
import { hashPassword, verifyPassword } from 'nuxt-auth-utils/server/utils/crypto' // اگر نیاز به hash داری

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const { email, password } = body

  if (!email || !password) {
    throw createError({ statusCode: 400, message: 'ایمیل و رمز عبور الزامی است' })
  }

  // اینجا منطق ورود با Django یا DB خودت رو پیاده کن
  // مثال ساده (در واقعیت به Django API کال کن):
  try {
    // فرض کنیم یک user در DB داری (یا به Django POST کن)
    // const user = await $fetch('http://127.0.0.1:8000/api/v1/login', {
    //   method: 'POST',
    //   body: { email, password }
    // })

    // اگر موفق بود:
    await setUserSession(event, {
      user: {
        email,
        // name, id, ... از Django بگیر
      },
      authProvider: 'credentials'
    })

    return { success: true, message: 'ورود موفق' }
  } catch (err) {
    throw createError({ statusCode: 401, message: 'ایمیل یا رمز عبور اشتباه است' })
  }
})