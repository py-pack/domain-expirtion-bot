import axios from 'axios'
import {env} from "@/env.ts";

const api = axios.create({
    baseURL: `${env.api.baseUrl}/api/v1`,
    withCredentials: false, // змінити на true, якщо будеш юзати httpOnly cookies
})

// ⛔ Отримуємо токен із localStorage або з Pinia store (залежно від реалізації)
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
})

// 🔁 Обробляємо 401 помилки — можна редіректити або оновлювати токен
api.interceptors.response.use(
    (response) => response,
    (error) => {

        // 👇 обробка кастомної помилки від FastAPI
        const detail = error?.response?.data?.detail
        if (typeof detail === 'string') {
            error.message = detail
        }

        if (error.response?.status === 401) {
            window.location.href = '/login'
            console.warn('⛔ Unauthorized. Redirect to login')
        }
        return Promise.reject(error)
    }
)

export default api
