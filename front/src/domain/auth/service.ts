import {jwtDecode} from 'jwt-decode'
import {authEvents} from '@/shared/auth/auth-events'
import {tokenStore} from '@/shared/auth/token-store'
import {registerAuthRefreshHandlers} from '@/shared/http/auth-refresh'
import type {
  GoogleCodePayload,
  GoogleOneTapPayload,
  LoginPayload,
  TokenPair,
} from '@/domain/auth/model'
import {authRepository} from '@/domain/auth/repository'

type JwtPayload = {
  exp?: number
}

function isTokenExpired(token: string): boolean {
  try {
    const payload = jwtDecode<JwtPayload>(token)

    if (!payload.exp) {
      return true
    }

    return payload.exp <= Date.now() / 1000
  } catch {
    return true
  }
}

function saveTokenPair(tokens: TokenPair): void {
  tokenStore.setTokens({
    accessToken: tokens.access_token,
  })
}

export const authService = {
  async login(payload: LoginPayload): Promise<void> {
    const tokens = await authRepository.login(payload)
    saveTokenPair(tokens)
  },

  async loginWithGoogleCode(payload: GoogleCodePayload): Promise<void> {
    const tokens = await authRepository.loginWithGoogleCode(payload)
    saveTokenPair(tokens)
  },

  async loginWithGoogleOneTap(payload: GoogleOneTapPayload): Promise<void> {
    const tokens = await authRepository.loginWithGoogleOneTap(payload)
    saveTokenPair(tokens)
  },

  async refreshSession(): Promise<string> {
    const tokens = await authRepository.refresh()

    saveTokenPair(tokens)

    return tokens.access_token
  },

  async logout(): Promise<void> {
    try {
      await authRepository.logout()
    } finally {
      this.clearSession()
      authEvents.emit('signed-out')
    }
  },

  clearSession(): void {
    tokenStore.clear()
  },

  isAuthenticated(): boolean {
    const accessToken = tokenStore.getAccessToken()

    if (!accessToken) {
      return false
    }

    return !isTokenExpired(accessToken)
  },
}

registerAuthRefreshHandlers({
  refreshAccessToken: async (): Promise<string> => authService.refreshSession(),
  onRefreshFailure: (): void => {
    authService.clearSession()
    authEvents.emit('session-expired')
  },
})
