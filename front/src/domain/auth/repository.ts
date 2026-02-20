import {httpClient} from '@/shared/http/client'
import {
  type GoogleCodePayload,
  type GoogleOneTapPayload,
  type LoginPayload,
  type RefreshPayload,
  type TokenPair,
  googleCodePayloadSchema,
  googleOneTapPayloadSchema,
  loginPayloadSchema,
  refreshPayloadSchema,
  tokenPairSchema,
} from '@/domain/auth/model'

export interface AuthRepository {
  login(payload: LoginPayload): Promise<TokenPair>
  loginWithGoogleCode(payload: GoogleCodePayload): Promise<TokenPair>
  loginWithGoogleOneTap(payload: GoogleOneTapPayload): Promise<TokenPair>
  refresh(payload: RefreshPayload): Promise<TokenPair>
  logout(payload: RefreshPayload): Promise<void>
}

async function parseTokenPair(data: unknown): Promise<TokenPair> {
  return tokenPairSchema.parseAsync(data)
}

export const authRepository: AuthRepository = {
  async login(payload: LoginPayload): Promise<TokenPair> {
    const requestPayload = loginPayloadSchema.parse(payload)
    const {data} = await httpClient.post('/auth/login', requestPayload, {
      skipAuthRefresh: true,
    })

    return parseTokenPair(data)
  },

  async loginWithGoogleCode(payload: GoogleCodePayload): Promise<TokenPair> {
    const requestPayload = googleCodePayloadSchema.parse(payload)
    const {data} = await httpClient.post('/auth/login-google', requestPayload, {
      skipAuthRefresh: true,
    })

    return parseTokenPair(data)
  },

  async loginWithGoogleOneTap(payload: GoogleOneTapPayload): Promise<TokenPair> {
    const requestPayload = googleOneTapPayloadSchema.parse(payload)
    const {data} = await httpClient.post(
      '/auth/login-google-one-tap',
      requestPayload,
      {
        skipAuthRefresh: true,
      },
    )

    return parseTokenPair(data)
  },

  async refresh(payload: RefreshPayload): Promise<TokenPair> {
    const requestPayload = refreshPayloadSchema.parse(payload)
    const {data} = await httpClient.post('/auth/refresh', requestPayload, {
      skipAuthRefresh: true,
    })

    return parseTokenPair(data)
  },

  async logout(payload: RefreshPayload): Promise<void> {
    const requestPayload = refreshPayloadSchema.parse(payload)
    await httpClient.post('/auth/logout', requestPayload, {
      skipAuthRefresh: true,
    })
  },
}
