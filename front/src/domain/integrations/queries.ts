import {computed, type MaybeRefOrGetter, toValue} from 'vue'
import {useQuery} from '@tanstack/vue-query'
import type {IntegrationFilters} from '@/domain/integrations/model'
import {integrationsService} from '@/domain/integrations/service'

export const integrationsQueryKeys = {
  all: ['integrations'] as const,
  list: (filters: IntegrationFilters) =>
    [
      'integrations',
      'list',
      filters.searchQuery.trim(),
      filters.statusFilter,
      filters.typeFilter,
    ] as const,
}

export function useIntegrationsQuery(filters: MaybeRefOrGetter<IntegrationFilters>) {
  return useQuery({
    queryKey: computed(() => integrationsQueryKeys.list(toValue(filters))),
    queryFn: async () => integrationsService.list(toValue(filters)),
    staleTime: 60_000,
  })
}
