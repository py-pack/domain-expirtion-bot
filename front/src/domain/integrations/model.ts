import {z} from 'zod'

export const integrationStatusSchema = z.enum([
  'active',
  'inactive',
  'warning',
  'error',
])

export const integrationSchema = z.object({
  id: z.string(),
  type: z.string(),
  name: z.string(),
  login: z.string(),
  status: integrationStatusSchema,
  units: z.array(z.string()),
  lastSync: z.string(),
  icon: z.string(),
})

export const integrationsSchema = z.array(integrationSchema)

export type IntegrationStatus = z.infer<typeof integrationStatusSchema>
export type Integration = z.infer<typeof integrationSchema>

export type IntegrationFilters = {
  searchQuery: string
  statusFilter: 'all' | IntegrationStatus
  typeFilter: 'all' | string
}
