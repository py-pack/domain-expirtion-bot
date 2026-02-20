import axios from 'axios'

export type ApiErrorCode =
  | 'bad_request'
  | 'unauthorized'
  | 'forbidden'
  | 'not_found'
  | 'validation'
  | 'rate_limited'
  | 'network'
  | 'server_error'
  | 'unknown'

export class ApiError extends Error {
  readonly code: ApiErrorCode
  readonly status?: number
  readonly details?: unknown
  readonly cause?: unknown

  constructor(params: {
    message: string
    code: ApiErrorCode
    status?: number
    details?: unknown
    cause?: unknown
  }) {
    super(params.message)

    this.name = 'ApiError'
    this.code = params.code
    this.status = params.status
    this.details = params.details

    if (params.cause) {
      this.cause = params.cause
    }
  }
}

function mapStatusToCode(status?: number): ApiErrorCode {
  if (!status) {
    return 'network'
  }

  if (status === 400) {
    return 'bad_request'
  }

  if (status === 401) {
    return 'unauthorized'
  }

  if (status === 403) {
    return 'forbidden'
  }

  if (status === 404) {
    return 'not_found'
  }

  if (status === 422) {
    return 'validation'
  }

  if (status === 429) {
    return 'rate_limited'
  }

  if (status >= 500) {
    return 'server_error'
  }

  return 'unknown'
}

export function toApiError(error: unknown): ApiError {
  if (error instanceof ApiError) {
    return error
  }

  if (axios.isAxiosError(error)) {
    const status = error.response?.status
    const payload = error.response?.data
    const payloadDetail =
      payload && typeof payload === 'object'
        ? (payload as Record<string, unknown>).detail
        : undefined

    const message =
      typeof payloadDetail === 'string'
        ? payloadDetail
        : error.message || 'Request failed'

    return new ApiError({
      message,
      status,
      details: payload,
      code: mapStatusToCode(status),
      cause: error,
    })
  }

  if (error instanceof Error) {
    return new ApiError({
      message: error.message,
      code: 'unknown',
      cause: error,
    })
  }

  return new ApiError({
    message: 'Unexpected error',
    code: 'unknown',
    details: error,
  })
}

export function getApiErrorMessage(error: unknown): string {
  return toApiError(error).message
}
