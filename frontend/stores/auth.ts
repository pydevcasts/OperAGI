// stores/auth.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

// استفاده از یک متغیر محیطی یا ثابت برای آدرس API
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/v1'; // پایه API

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref<string | null>(null)
  const refreshToken = ref<string | null>(null)
  const isAuthenticated = computed(() => !!accessToken.value)

  const login = async (email: string, password: string) => {
    console.log("در حال ارسال درخواست ورود به:", `${API_BASE_URL}/auth/login/`); // لاگ ارسال
    console.log("داده ارسالی:", { email, password }); // لاگ داده

    try {
      const res = await $fetch(`${API_BASE_URL}/auth/login/`, {
        method: 'POST',
        body: { email, password }
      });

      console.log("پاسخ دریافت شده از سرور:", res); // لاگ پاسخ

      // تغییر نام فیلدها اگر dj-rest-auth به این شکل برگرداند
      // بررسی اینکه آیا فیلدها وجود دارند یا خیر
      if (res.access_token) {
        accessToken.value = res.access_token;
        console.log("Access Token ذخیره شد:", res.access_token);
      } else {
        console.error("پاسخ سرور فیلد 'access_token' ندارد:", res);
        throw new Error("Invalid response from server: access_token missing");
      }

      if (res.refresh_token) {
        refreshToken.value = res.refresh_token;
        console.log("Refresh Token ذخیره شد:", res.refresh_token);
      } else {
        console.error("پاسخ سرور فیلد 'refresh_token' ندارد:", res);
        // اگر refresh نیاز نیست، می‌توان اینجا فقط اخطار داد یا ادامه داد
        refreshToken.value = null; // یا مقدار دیگری
      }

      localStorage.setItem('accessToken', res.access_token);
      localStorage.setItem('refreshToken', res.refresh_token);

    } catch (error) {
      console.error("خطا در فرآیند ورود:", error); // لاگ خطا
      // می‌توانید خطای خاصی را نیز پرتاب کنید تا در جای دیگر گرفته شود
      throw error;
    }
  }

  const logout = () => {
    accessToken.value = null
    refreshToken.value = null
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
  }

  if (typeof window !== 'undefined') {
    accessToken.value = localStorage.getItem('accessToken');
    refreshToken.value = localStorage.getItem('refreshToken');
  }

  return { accessToken, refreshToken, isAuthenticated, login, logout }
})