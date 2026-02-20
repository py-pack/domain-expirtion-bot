import {useQuery} from '@tanstack/vue-query'
import {integrationsService} from '@/domain/integrations/service'

export const integrationsQueryKeys = {
  all: ['integrations'] as const,
}

export function useIntegrationsQuery() {
  return useQuery({
    queryKey: integrationsQueryKeys.all,
    queryFn: async () => integrationsService.list(),
    staleTime: 60_000,
  })
}
