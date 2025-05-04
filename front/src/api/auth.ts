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
    const response = await api.post<LoginResponse>('/auth/login', payload)
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
