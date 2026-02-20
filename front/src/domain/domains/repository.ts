import {httpClient} from '@/shared/http/client'
import {
  type DomainExpiration,
  domainNameSchema,
  mapDomainExpiration,
} from '@/domain/domains/model'

export interface DomainsRepository {
  getExpiration(domainName: string): Promise<DomainExpiration>
}

export const domainsRepository: DomainsRepository = {
  async getExpiration(domainName: string): Promise<DomainExpiration> {
    const normalizedDomainName = domainNameSchema.parse(domainName)
    const {data} = await httpClient.get('/domain/expiration', {
      params: {
        domain_name: normalizedDomainName,
      },
    })

    return mapDomainExpiration(data)
  },
}
