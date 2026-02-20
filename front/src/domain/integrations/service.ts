import type {
  Integration,
  IntegrationFilters,
} from '@/domain/integrations/model'
import {integrationsRepository} from '@/domain/integrations/repository'

export const integrationsService = {
  async list(): Promise<Integration[]> {
    return integrationsRepository.list()
  },

  filter(
    integrations: Integration[],
    filters: IntegrationFilters,
  ): Integration[] {
    const query = filters.searchQuery.trim().toLowerCase()

    return integrations.filter((integration) => {
      const matchesSearch =
        query.length === 0 ||
        integration.name.toLowerCase().includes(query) ||
        integration.login.toLowerCase().includes(query)

      const matchesStatus =
        filters.statusFilter === 'all' || integration.status === filters.statusFilter

      const matchesType =
        filters.typeFilter === 'all' || integration.type === filters.typeFilter

      return matchesSearch && matchesStatus && matchesType
    })
  },
}
