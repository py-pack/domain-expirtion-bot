import {httpClient} from '@/shared/http/client'
import {
  type GoogleCodePayload,
  type GoogleOneTapPayload,
  type LoginPayload,
  type TokenPair,
  googleCodePayloadSchema,
  googleOneTapPayloadSchema,
  loginPayloadSchema,
  tokenPairSchema,
} from '@/domain/auth/model'

export interface AuthRepository {
  login(payload: LoginPayload): Promise<TokenPair>
  loginWithGoogleCode(payload: GoogleCodePayload): Promise<TokenPair>
  loginWithGoogleOneTap(payload: GoogleOneTapPayload): Promise<TokenPair>
  refresh(): Promise<TokenPair>
  logout(): Promise<void>
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

  async refresh(): Promise<TokenPair> {
    const {data} = await httpClient.post('/auth/refresh', {}, {
      skipAuthRefresh: true,
    })

    return parseTokenPair(data)
  },

  async logout(): Promise<void> {
    await httpClient.post('/auth/logout', {}, {
      skipAuthRefresh: true,
    })
  },
}
