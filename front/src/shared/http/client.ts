import axios, {
  AxiosHeaders,
  type AxiosError,
  type InternalAxiosRequestConfig,
} from 'axios'
import {env} from '@/env'
import {tokenStore} from '@/shared/auth/token-store'
import {retryRequestWithFreshToken} from '@/shared/http/auth-refresh'
import {toApiError} from '@/shared/http/errors'

const baseConfig = {
  baseURL: `${env.api.baseUrl}/api/v1`,
  withCredentials: true,
  timeout: 15_000,
}

export const httpClient = axios.create(baseConfig)

function injectBearerToken(
  config: InternalAxiosRequestConfig,
): InternalAxiosRequestConfig {
  const accessToken = tokenStore.getAccessToken()

  if (!accessToken) {
    return config
  }

  if (!config.headers) {
    config.headers = new AxiosHeaders()
  }

  ;(config.headers as Record<string, string>).Authorization = `Bearer ${accessToken}`

  return config
}

httpClient.interceptors.request.use(injectBearerToken)

function canRetryNetworkError(error: AxiosError): boolean {
  const config = error.config

  if (!config || config._networkRetry || config.skipAuthRefresh) {
    return false
  }

  if (error.response) {
    return false
  }

  const method = (config.method ?? 'get').toLowerCase()

  return method === 'get' || method === 'head' || method === 'options'
}

function canRefreshAuth(error: AxiosError): boolean {
  const config = error.config

  if (!config || config._retry || config.skipAuthRefresh) {
    return false
  }

  return error.response?.status === 401
}

httpClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    if (canRetryNetworkError(error)) {
      const requestConfig = error.config as InternalAxiosRequestConfig
      requestConfig._networkRetry = true

      return httpClient.request(requestConfig)
    }

    if (canRefreshAuth(error)) {
      try {
        return await retryRequestWithFreshToken(httpClient, error)
      } catch (refreshError) {
        return Promise.reject(toApiError(refreshError))
      }
    }

    return Promise.reject(toApiError(error))
  },
)
