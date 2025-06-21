import axios from 'axios'
import {env} from "@/env.ts"
import {refreshToken} from "@/api/auth.ts"
import {clearAuth} from "@/utils/storage/modules/auth.ts"
import storage from "@/utils/storage"
import {router} from "@/router"

const api = axios.create({
    baseURL: `${env.api.baseUrl}/api/v1`,
    withCredentials: false, // змінити на true, якщо будеш використовувати httpOnly cookies
})

// 👉 Глобальні стани для контролю оновлення токена
let isRefreshing = false // Чи зараз триває refresh
let failedQueue: {
    resolve: (token: string) => void,
    reject: (err: any) => void
}[] = []

// 🔁 Обробка всіх запитів, що чекали на новий токен
const processQueue = (error: any, token: string | null = null) => {
    failedQueue.forEach(prom => {
        if (error) {
            prom.reject(error)
        } else {
            prom.resolve(token)
        }
    })
    failedQueue = []
}

// 📤 Додаємо access токен до кожного запиту
api.interceptors.request.use((config) => {
    const token: string = storage.auth.getToken()
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
})

// 🔄 Перехоплення помилок, зокрема 401 (Unauthorized)
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config

        const is401 = error.response?.status === 401
        const hasNotRetried = !originalRequest._retry

        if (is401 && hasNotRetried) {
            if (isRefreshing) {
                // 🕒 Якщо refresh вже триває — ставимо запит у чергу
                return new Promise((resolve, reject) => {
                    failedQueue.push({
                        resolve: (token: string) => {
                            originalRequest.headers.Authorization = `Bearer ${token}`
                            resolve(axios(originalRequest))
                        },
                        reject
                    })
                })
            }

            // 🟡 Починаємо новий refresh
            originalRequest._retry = true
            isRefreshing = true

            try {
                await refreshToken() // ⬅️ Оновлюємо токен

                const newAccess = storage.auth.getToken()

                processQueue(null, newAccess) // ✅ Повідомляємо всіх, хто чекав

                originalRequest.headers.Authorization = `Bearer ${newAccess}`
                return axios(originalRequest) // 🔁 Повторюємо оригінальний запит

            } catch (err) {
                processQueue(err, null) // ❌ Всі запити з черги падають

                clearAuth()
                router.push("/login")
                return Promise.reject(err)
            } finally {
                isRefreshing = false
            }
        }

        // 💬 Обробка кастомного повідомлення від FastAPI (з detail)
        const detail = error?.response?.data?.detail
        if (typeof detail === 'string') {
            error.message = detail
        }
        return Promise.reject(error) // 🔻 Інші помилки просто прокидуємо далі
    }
)

export default api
