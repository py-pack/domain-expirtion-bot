import {z} from 'zod'

export const currentUserSchema = z.object({
  id: z.number().int().positive(),
  email: z.string().email(),
  full_name: z.string(),
})

export const systemUserSchema = z.object({
  id: z.number().int().positive(),
  email: z.string().email(),
  full_name: z.string(),
  is_active: z.boolean(),
  settings: z.record(z.string(), z.unknown()),
})

export const createSystemUserPayloadSchema = z.object({
  email: z.string().email(),
  full_name: z.string().trim().min(1).max(255),
  password: z.string().min(8),
  is_active: z.boolean().default(true),
  settings: z.record(z.string(), z.unknown()).default({}),
})

export const updateSystemUserPayloadSchema = z
  .object({
    email: z.string().email().optional(),
    full_name: z.string().trim().min(1).max(255).optional(),
    password: z.string().min(8).optional(),
    is_active: z.boolean().optional(),
    settings: z.record(z.string(), z.unknown()).optional(),
  })
  .refine((payload) => Object.keys(payload).length > 0, {
    message: 'At least one field must be provided',
  })

export const updateCurrentUserPayloadSchema = z
  .object({
    full_name: z.string().trim().min(1).max(255),
    current_password: z.string().min(1).optional(),
    new_password: z.string().min(8).optional(),
  })
  .refine(
    (payload) =>
      (Boolean(payload.current_password) && Boolean(payload.new_password)) ||
      (!payload.current_password && !payload.new_password),
    {
      message:
        'Both current_password and new_password must be provided to change password',
      path: ['new_password'],
    },
  )

export type CurrentUser = z.infer<typeof currentUserSchema>
export type UpdateCurrentUserPayload = z.infer<typeof updateCurrentUserPayloadSchema>
export type SystemUser = z.infer<typeof systemUserSchema>
export type CreateSystemUserPayload = z.infer<typeof createSystemUserPayloadSchema>
export type UpdateSystemUserPayload = z.infer<typeof updateSystemUserPayloadSchema>
