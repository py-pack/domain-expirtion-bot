import type {
  AccountDomainApi,
  Integration,
  IntegrationFilters,
} from '@/domain/integrations/model'
import {integrationsRepository} from '@/domain/integrations/repository'
import {integrationProviderOptions} from '@/domain/integrations/model'
import {formatIsoDate} from '@/shared/utils/time'

const PROVIDER_ICON_URLS: Record<AccountDomainApi['name'], string> = {
  ukraine_host: 'https://i.imgur.com/fAsCgou.png',
  name_cheap: 'https://i.imgur.com/J8pJCJD.png',
  go_daddy: 'https://i.imgur.com/jduUiuL.png',
  whois: 'https://i.imgur.com/J8pJCJD.png',
  cloud_flare: 'https://i.imgur.com/txUzLWA.png',
}

function providerLabel(provider: AccountDomainApi['name']): string {
  return (
    integrationProviderOptions.find((option) => option.value === provider)?.label ?? provider
  )
}

export const integrationsService = {
  async list(filters: IntegrationFilters): Promise<Integration[]> {
    const rows = await integrationsRepository.list(filters)
    return rows.map((row) => integrationsService.mapFromApi(row))
  },

  mapFromApi(account: AccountDomainApi): Integration {
    return {
      id: account.id,
      type: account.name,
      name: providerLabel(account.name),
      login: account.login,
      status: account.status,
      units: account.unit_name ? [account.unit_name] : [],
      lastSync: formatIsoDate(account.last_update_at),
      icon: PROVIDER_ICON_URLS[account.name],
    }
  },
}
