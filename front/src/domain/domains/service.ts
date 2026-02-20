import type {DomainExpiration} from '@/domain/domains/model'
import {domainNameSchema} from '@/domain/domains/model'
import {domainsRepository} from '@/domain/domains/repository'

export const domainsService = {
  async getExpiration(domainName: string): Promise<DomainExpiration> {
    const normalizedDomainName = domainNameSchema.parse(domainName)

    return domainsRepository.getExpiration(normalizedDomainName)
  },
}
