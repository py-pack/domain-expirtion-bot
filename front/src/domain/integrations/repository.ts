import {httpClient} from '@/shared/http/client'
import {
  accountDomainsApiSchema,
  type AccountDomainApi,
  type IntegrationFilters,
} from '@/domain/integrations/model'

export interface IntegrationsRepository {
  list(filters?: Partial<IntegrationFilters>): Promise<AccountDomainApi[]>
}

export const integrationsRepository: IntegrationsRepository = {
  async list(filters = {}): Promise<AccountDomainApi[]> {
    const params: Record<string, string> = {}

    const searchQuery = filters.searchQuery?.trim()
    if (searchQuery) {
      params.search = searchQuery
    }

    if (filters.statusFilter && filters.statusFilter !== 'all') {
      params.status = filters.statusFilter
    }

    if (filters.typeFilter && filters.typeFilter !== 'all') {
      params.name = filters.typeFilter
    }

    const {data} = await httpClient.get('/account-domains/', {params})
    return accountDomainsApiSchema.parseAsync(data)
  },
}
