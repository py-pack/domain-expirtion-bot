import {z} from 'zod'

export const domainNameSchema = z
  .string()
  .trim()
  .toLowerCase()
  .min(3)
  .regex(/^[a-z0-9.-]+$/)

const expirationDataSchema = z.object({
  domain: z.string(),
  expiration_date: z.string(),
})

export const expirationResponseSchema = z.object({
  success: z.boolean(),
  data: expirationDataSchema,
})

export type DomainExpiration = {
  domain: string
  expirationDate: string
}

export function mapDomainExpiration(data: unknown): DomainExpiration {
  const parsed = expirationResponseSchema.parse(data)

  return {
    domain: parsed.data.domain,
    expirationDate: parsed.data.expiration_date,
  }
}
