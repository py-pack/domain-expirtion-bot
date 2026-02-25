import {z} from 'zod'

export const unitSchema = z.object({
  id: z.number().int().positive(),
  name: z.string(),
  responsibles_count: z.number().int().nonnegative().default(0),
})

export const unitDetailsSchema = z.object({
  id: z.number().int().positive(),
  name: z.string(),
})

export const unitResponsibleLevelSchema = z.enum(['View', 'Edit', 'Full'])

export const unitResponsibleSchema = z.object({
  id: z.number().int().positive(),
  email: z.string().email(),
  full_name: z.string(),
  level: unitResponsibleLevelSchema,
})

export const createUnitPayloadSchema = z.object({
  name: z.string().trim().min(1).max(255),
})

export const updateUnitPayloadSchema = z
  .object({
    name: z.string().trim().min(1).max(255).optional(),
  })
  .refine((payload) => Object.keys(payload).length > 0, {
    message: 'At least one field must be provided',
  })

export const replaceUnitResponsiblesPayloadSchema = z.object({
  assignments: z
    .array(
      z.object({
        user_id: z.number().int().positive(),
        level: unitResponsibleLevelSchema,
      }),
    )
    .refine(
      (assignments) =>
        new Set(assignments.map((assignment) => assignment.user_id)).size ===
        assignments.length,
      {
        message: 'assignments.user_id must be unique',
      },
    ),
})

export type Unit = z.infer<typeof unitSchema>
export type UnitDetails = z.infer<typeof unitDetailsSchema>
export type UnitResponsible = z.infer<typeof unitResponsibleSchema>
export type UnitResponsibleLevel = z.infer<typeof unitResponsibleLevelSchema>
export type CreateUnitPayload = z.infer<typeof createUnitPayloadSchema>
export type UpdateUnitPayload = z.infer<typeof updateUnitPayloadSchema>
export type ReplaceUnitResponsiblesPayload = z.infer<
  typeof replaceUnitResponsiblesPayloadSchema
>
