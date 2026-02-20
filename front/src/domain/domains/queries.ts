import {computed, unref, type MaybeRef} from 'vue'
import {useQuery} from '@tanstack/vue-query'
import {domainsService} from '@/domain/domains/service'

export const domainsQueryKeys = {
  all: ['domains'] as const,
  expiration: (domainName: string) => ['domains', {domainName}] as const,
}

export function useDomainExpirationQuery(domainName: MaybeRef<string>) {
  const normalizedDomainName = computed(() => unref(domainName).trim().toLowerCase())

  return useQuery({
    queryKey: computed(() => domainsQueryKeys.expiration(normalizedDomainName.value)),
    queryFn: async () => domainsService.getExpiration(normalizedDomainName.value),
    enabled: computed(() => normalizedDomainName.value.length > 0),
    staleTime: 30_000,
    retry: 1,
  })
}
