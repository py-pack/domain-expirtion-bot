import 'axios'

export interface ApiEnvelope<T> {
  success: boolean
  data: T
}

declare module 'axios' {
  interface AxiosRequestConfig {
    skipAuthRefresh?: boolean
  }

  interface InternalAxiosRequestConfig {
    _retry?: boolean
    _networkRetry?: boolean
    skipAuthRefresh?: boolean
  }
}
