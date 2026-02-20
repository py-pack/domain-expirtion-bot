export type AuthTokens = {
  accessToken: string
  refreshToken: string
}

let accessToken: string | null = null
let refreshToken: string | null = null

export const tokenStore = {
  setTokens(tokens: AuthTokens): void {
    accessToken = tokens.accessToken
    refreshToken = tokens.refreshToken
  },

  setAccessToken(token: string | null): void {
    accessToken = token
  },

  setRefreshToken(token: string | null): void {
    refreshToken = token
  },

  getAccessToken(): string | null {
    return accessToken
  },

  getRefreshToken(): string | null {
    return refreshToken
  },

  clear(): void {
    accessToken = null
    refreshToken = null
  },
}
