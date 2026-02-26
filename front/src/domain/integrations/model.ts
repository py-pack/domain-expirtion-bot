import {z} from 'zod'

export const integrationProviderSchema = z.enum([
  'ukraine_host',
  'name_cheap',
  'go_daddy',
  'whois',
  'cloud_flare',
])

export const integrationStatusSchema = z.enum([
  'active',
  'inactive',
  'warning',
  'ban',
])

export const accountDomainApiSchema = z.object({
  id: z.number().int().positive(),
  name: integrationProviderSchema,
  login: z.string(),
  unit_id: z.number().int().positive().nullable(),
  unit_name: z.string().nullable(),
  status: integrationStatusSchema,
  accesses: z.record(z.string(), z.unknown()).default({}),
  ns_accounts: z.array(z.string()).default([]),
  created_at: z.string(),
  last_update_at: z.string(),
})

export const accountDomainsApiSchema = z.array(accountDomainApiSchema)

export const integrationSchema = z.object({
  id: z.number().int().positive(),
  type: integrationProviderSchema,
  name: z.string(),
  login: z.string(),
  status: integrationStatusSchema,
  units: z.array(z.string()),
  lastSync: z.string(),
  icon: z.string(),
})

export const integrationsSchema = z.array(integrationSchema)

export type IntegrationStatus = z.infer<typeof integrationStatusSchema>
export type IntegrationProvider = z.infer<typeof integrationProviderSchema>
export type Integration = z.infer<typeof integrationSchema>
export type AccountDomainApi = z.infer<typeof accountDomainApiSchema>

export type IntegrationFilters = {
  searchQuery: string
  statusFilter: 'all' | IntegrationStatus
  typeFilter: 'all' | IntegrationProvider
}

export const integrationProviderOptions: ReadonlyArray<{
  value: IntegrationProvider
  label: string
}> = [
  {value: 'ukraine_host', label: 'Ukraine Host'},
  {value: 'name_cheap', label: 'Namecheap'},
  {value: 'go_daddy', label: 'GoDaddy'},
  {value: 'whois', label: 'Whois'},
  {value: 'cloud_flare', label: 'Cloudflare'},
]
