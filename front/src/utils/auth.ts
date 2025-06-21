import {jwtDecode} from "jwt-decode"
import storage from "@/utils/storage";

interface JWTPayload {
    exp: number

    [key: string]: any
}

// Пример функции проверки авторизации
export const checkIfUserIsAuthenticated = (): boolean => {
    const token = storage.auth.getToken()
    if (!token) return false

    try {
        const decoded = jwtDecode<JWTPayload>(token)
        const now = Date.now() / 1000 // секунди
        return decoded.exp > now
    } catch (e) {
        return false // токен пошкоджено або невалідний
    }
}
