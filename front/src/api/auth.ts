import api from './axios'
import storage from "@/utils/storage";
import {isAxiosError} from "@/utils/axios";

export interface LoginPayload {
    email: string
    password: string
}

export interface LoginResponse {
    access_token: string
    refresh_token: string
    token_type: string
}

export async function loginUser(payload: LoginPayload): Promise<true> {
    try {
        const response = await api.post<LoginResponse>('/auth/login', {
            ...payload,
            session_id: storage.session.getSessionId()
        })
        if (response.status === 200) {
            storage.auth.setToken(response.data.access_token)
            storage.auth.setRefreshToken(response.data.refresh_token)
        } else {
            return Promise.reject(new Error('Login failed'))
        }
        return true
    } catch (error: unknown) {
        let message = 'Unknown error'

        if (isAxiosError(error)) {
            message = error.response?.data?.detail || 'Login failed'
        }

        return Promise.reject(new Error(message))
    }
}

export async function loginWithGoogleOneTap(idToken: string): Promise<true> {
    try {
        const response = await api.post('/auth/login-google-one-tap', {
            id_token: idToken,
            session_id: storage.session.getSessionId()
        })
        if (response.status === 200) {
            storage.auth.setToken(response.data.access_token)
            storage.auth.setRefreshToken(response.data.refresh_token)
        } else {
            return Promise.reject(new Error('Login failed'))
        }
        return Promise.resolve()
    } catch (err) {
        return Promise.reject(err)
    }
}

export async function loginWithGoogle(code: string): Promise<true> {
    try {
        const response = await api.post('/auth/login-google', {
            code,
            session_id: storage.session.getSessionId()
        })
        if (response.status === 200) {
            storage.auth.setToken(response.data.access_token)
            storage.auth.setRefreshToken(response.data.refresh_token)
        } else {
            return Promise.reject(new Error('Login failed'))
        }
        return Promise.resolve()
    } catch (err) {
        return Promise.reject(err)
    }
}

export async function refreshToken(refreshToken: string): Promise<true> {
    try {
        const response = await api.post("/auth/refresh", {
            refresh_token: refreshToken,
            session_id: storage.session.getSessionId()
        })
        if (response.status === 200) {
            storage.auth.setToken(response.data.access_token)
            storage.auth.setRefreshToken(response.data.refresh_token)
        } else {
            return Promise.reject(new Error('Login failed'))
        }
        return Promise.resolve()
    } catch (err) {
        return Promise.reject(err)
    }
}

export function logout() {
    storage.auth.clearAuth()
    storage.session.clearSessionId()
    router.push("/login")
}