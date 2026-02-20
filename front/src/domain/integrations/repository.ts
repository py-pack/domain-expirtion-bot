import {type Integration, integrationsSchema} from '@/domain/integrations/model'

export interface IntegrationsRepository {
  list(): Promise<Integration[]>
}

const INTEGRATIONS: Integration[] = [
  {
    id: '1',
    type: 'hostingUkraine',
    name: 'HostingUkraine',
    login: 'user@example.com',
    status: 'active',
    units: ['marketing'],
    lastSync: '2 minutes ago',
    icon: 'https://i.imgur.com/fAsCgou.png',
  },
  {
    id: '2',
    type: 'namecheap',
    name: 'Namecheap',
    login: 'user@example.com',
    status: 'active',
    units: ['web', 'web'],
    lastSync: 'an hour ago',
    icon: 'https://i.imgur.com/J8pJCJD.png',
  },
  {
    id: '3',
    type: 'godaddy',
    name: 'GoDaddy',
    login: 'user123@example.com',
    status: 'active',
    units: ['web pt 42'],
    lastSync: '5 hours ago',
    icon: 'https://i.imgur.com/jduUiuL.png',
  },
  {
    id: '4',
    type: 'cloudflare',
    name: 'Cloudflare',
    login: 'cf_user@example.com',
    status: 'active',
    units: ['backend'],
    lastSync: '2 days ago',
    icon: 'https://i.imgur.com/txUzLWA.png',
  },
  {
    id: '5',
    type: 'hostingUkraine',
    name: 'HostingUkraine',
    login: 'user@example.com',
    status: 'warning',
    units: ['billing'],
    lastSync: '6 days ago',
    icon: 'https://i.imgur.com/fAsCgou.png',
  },
]

export const integrationsRepository: IntegrationsRepository = {
  async list(): Promise<Integration[]> {
    return integrationsSchema.parse(INTEGRATIONS)
  },
}
