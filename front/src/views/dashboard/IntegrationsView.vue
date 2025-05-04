<script setup lang="ts">
import {ref, onMounted} from 'vue';
import SearchInput from '@/components/ui/SearchInput.vue';
import DropdownFilter from '@/components/ui/DropdownFilter.vue';
import Button from '@/components/ui/Button.vue';
import IntegrationsTable from '@/components/integrations/IntegrationsTable.vue';
import type {Integration} from '@/types';

// Mock data for the integrations
const integrations = ref<Integration[]>([
  {
    id: '1',
    type: 'hostingUkraine',
    name: 'HostingUkraine',
    login: 'user@example.com',
    status: 'active',
    units: ['marketing'],
    lastSync: '2 minutes ago',
    icon: 'https://i.imgur.com/fAsCgou.png'
  },
  {
    id: '2',
    type: 'namecheap',
    name: 'Namecheap',
    login: 'user@example.com',
    status: 'active',
    units: ['web', 'web'],
    lastSync: 'an hour ago',
    icon: 'https://i.imgur.com/J8pJCJD.png'
  },
  {
    id: '3',
    type: 'godaddy',
    name: 'GoDaddy',
    login: 'user123@example.com',
    status: 'active',
    units: ['web pt 42'],
    lastSync: '5 hours ago',
    icon: 'https://i.imgur.com/jduUiuL.png'
  },
  {
    id: '4',
    type: 'cloudflare',
    name: 'Cloudflare',
    login: 'cf_user@example.com',
    status: 'active',
    units: ['backend'],
    lastSync: '2 days ago',
    icon: 'https://i.imgur.com/txUzLWA.png'
  },
  {
    id: '5',
    type: 'hostingUkraine',
    name: 'HostingUkraine',
    login: 'user@example.com',
    status: 'active',
    units: ['6 days ago'],
    lastSync: '6 days ago',
    icon: 'https://i.imgur.com/fAsCgou.png'
  }
]);

// Search and filter states
const searchQuery = ref('');
const statusFilter = ref('all');
const typeFilter = ref('all');

// Filter options
const statusOptions = [
  {value: 'all', label: 'All Statuses'},
  {value: 'active', label: 'Active'},
  {value: 'inactive', label: 'Inactive'},
  {value: 'warning', label: 'Warning'},
  {value: 'error', label: 'Error'}
];

const typeOptions = [
  {value: 'all', label: 'All Types'},
  {value: 'hostingUkraine', label: 'HostingUkraine'},
  {value: 'namecheap', label: 'Namecheap'},
  {value: 'godaddy', label: 'GoDaddy'},
  {value: 'cloudflare', label: 'Cloudflare'}
];

const handleAddIntegration = () => {
  // This would open a modal or navigate to add integration form
  console.log('Add integration clicked');
};
</script>

<template>
  <div class="integrations-page">
    <div class="controls-container">
      <div class="search-section">
        <SearchInput
            placeholder="Search integrations"
            @update:search="searchQuery = $event"
        />
      </div>

      <div class="filters-section">
        <DropdownFilter
            label="Type"
            :options="typeOptions"
            v-model="typeFilter"
        />

        <DropdownFilter
            label="Status"
            :options="statusOptions"
            v-model="statusFilter"
        />

        <Button variant="primary">
          Add Integration
        </Button>
      </div>
    </div>

    <div class="integrations-table-container">
      <IntegrationsTable
          :integrations="integrations"
          :searchQuery="searchQuery"
          :statusFilter="statusFilter"
          :typeFilter="typeFilter"
      />
    </div>
  </div>
</template>
