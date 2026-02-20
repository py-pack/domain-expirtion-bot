export type AuthTokens = {
  accessToken: string
}

let accessToken: string | null = null

export const tokenStore = {
  setTokens(tokens: AuthTokens): void {
    accessToken = tokens.accessToken
  },

  setAccessToken(token: string | null): void {
    accessToken = token
  },

  setRefreshToken(token: string | null): void {
    void token
  },

  getAccessToken(): string | null {
    return accessToken
  },

  getRefreshToken(): string | null {
    return null
  },

  clear(): void {
    accessToken = null
  },
}
