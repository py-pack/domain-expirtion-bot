import type {
  AxiosError,
  AxiosInstance,
  AxiosResponse,
  InternalAxiosRequestConfig,
} from 'axios'
import {AxiosHeaders} from 'axios'
import {toApiError} from '@/shared/http/errors'

type RefreshAccessTokenHandler = () => Promise<string>
type RefreshFailureHandler = (error: unknown) => void

type PendingRequest = {
  resolve: (accessToken: string) => void
  reject: (error: unknown) => void
}

let refreshAccessTokenHandler: RefreshAccessTokenHandler | null = null
let refreshFailureHandler: RefreshFailureHandler | null = null

let isRefreshing = false
const pendingRequests: PendingRequest[] = []

export function registerAuthRefreshHandlers(params: {
  refreshAccessToken: RefreshAccessTokenHandler
  onRefreshFailure?: RefreshFailureHandler
}): void {
  refreshAccessTokenHandler = params.refreshAccessToken
  refreshFailureHandler = params.onRefreshFailure ?? null
}

function enqueuePendingRequest(): Promise<string> {
  return new Promise<string>((resolve, reject) => {
    pendingRequests.push({resolve, reject})
  })
}

function resolvePendingRequests(error: unknown | null, accessToken?: string): void {
  pendingRequests.splice(0, pendingRequests.length).forEach((request) => {
    if (error) {
      request.reject(error)
      return
    }

    request.resolve(accessToken ?? '')
  })
}

function setAuthorizationHeader(
  config: InternalAxiosRequestConfig,
  accessToken: string,
): void {
  if (!config.headers) {
    config.headers = new AxiosHeaders()
  }

  ;(config.headers as Record<string, string>).Authorization = `Bearer ${accessToken}`
}

async function getFreshAccessToken(): Promise<string> {
  if (!refreshAccessTokenHandler) {
    throw new Error('Auth refresh handler is not registered')
  }

  if (isRefreshing) {
    return enqueuePendingRequest()
  }

  isRefreshing = true

  try {
    const accessToken = await refreshAccessTokenHandler()
    resolvePendingRequests(null, accessToken)

    return accessToken
  } catch (error) {
    resolvePendingRequests(error)
    refreshFailureHandler?.(error)

    throw error
  } finally {
    isRefreshing = false
  }
}

export async function retryRequestWithFreshToken(
  client: AxiosInstance,
  error: AxiosError,
): Promise<AxiosResponse> {
  const originalRequest = error.config

  if (!originalRequest || originalRequest._retry) {
    throw toApiError(error)
  }

  originalRequest._retry = true

  try {
    const freshToken = await getFreshAccessToken()
    setAuthorizationHeader(originalRequest, freshToken)

    return await client.request(originalRequest)
  } catch (refreshError) {
    throw toApiError(refreshError)
  }
}
