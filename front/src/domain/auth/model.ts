import {z} from 'zod'

export const loginPayloadSchema = z.object({
  email: z.string().email(),
  password: z.string().min(1),
})

export const googleCodePayloadSchema = z.object({
  code: z.string().min(1),
})

export const googleOneTapPayloadSchema = z.object({
  id_token: z.string().min(1),
})

export const refreshPayloadSchema = z.object({
  refresh_token: z.string().min(1),
})

export const tokenPairSchema = z.object({
  access_token: z.string().min(1),
  refresh_token: z.string().min(1),
  token_type: z.string().min(1).default('bearer'),
})

export type LoginPayload = z.infer<typeof loginPayloadSchema>
export type GoogleCodePayload = z.infer<typeof googleCodePayloadSchema>
export type GoogleOneTapPayload = z.infer<typeof googleOneTapPayloadSchema>
export type RefreshPayload = z.infer<typeof refreshPayloadSchema>
export type TokenPair = z.infer<typeof tokenPairSchema>
