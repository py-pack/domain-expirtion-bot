<script setup lang="ts">
import {computed, ref} from 'vue'
import {Plus} from 'lucide-vue-next'
import {
  integrationProviderOptions,
  type IntegrationStatus,
} from '@/domain/integrations/model'
import {useIntegrationsQuery} from '@/domain/integrations/queries'
import {getApiErrorMessage} from '@/shared/http/errors'
import UiButton from '@/ui/components/common/UiButton.vue'
import UiDropdownFilter from '@/ui/components/common/UiDropdownFilter.vue'
import UiEmptyState from '@/ui/components/common/UiEmptyState.vue'
import UiEntityPageLayout from '@/ui/layout/UiEntityPageLayout.vue'
import UiSearchInput from '@/ui/components/common/UiSearchInput.vue'
import IntegrationsTable from '@/ui/components/integrations/IntegrationsTable.vue'

const searchQuery = ref('')
const statusFilter = ref<'all' | IntegrationStatus>('all')
const typeFilter = ref<'all' | (typeof integrationProviderOptions)[number]['value']>('all')

const queryFilters = computed(() => ({
  searchQuery: searchQuery.value,
  statusFilter: statusFilter.value,
  typeFilter: typeFilter.value,
}))

const integrationsQuery = useIntegrationsQuery(queryFilters)
const filteredIntegrations = computed(() => integrationsQuery.data.value ?? [])

const statusOptions = [
  {value: 'all', label: 'All Statuses'},
  {value: 'active', label: 'Active'},
  {value: 'inactive', label: 'Inactive'},
  {value: 'warning', label: 'Warning'},
  {value: 'ban', label: 'Banned'},
]

const typeOptions = [
  {value: 'all', label: 'All Types'},
  ...integrationProviderOptions,
]

const errorMessage = computed(() => {
  if (!integrationsQuery.error.value) {
    return null
  }

  return getApiErrorMessage(integrationsQuery.error.value)
})
</script>

<template>
  <UiEntityPageLayout
    class="integrations-page"
    title="Integrations"
    description="Manage provider connections, filtering, and sync status."
    :breadcrumbs="[{label: 'Integrations'}]"
  >
    <template #actions>
      <UiButton tone="success">
        <template #icon>
          <Plus :size="16" />
        </template>
        Add integration
      </UiButton>
    </template>

    <div class="integrations-page__controls">
      <UiSearchInput v-model="searchQuery" placeholder="Search integrations" />

      <UiDropdownFilter v-model="typeFilter" label="Type" :options="typeOptions" />
      <UiDropdownFilter v-model="statusFilter" label="Status" :options="statusOptions" />
    </div>

    <p v-if="errorMessage" class="integrations-page__error">{{ errorMessage }}</p>

    <UiEmptyState
      v-else-if="!integrationsQuery.isLoading.value && filteredIntegrations.length === 0"
      title="No integrations found"
      description="Adjust filters or add a new integration."
    />

    <IntegrationsTable v-else :integrations="filteredIntegrations" />
  </UiEntityPageLayout>
</template>

<style scoped lang="scss">
.integrations-page {
  display: grid;
  gap: var(--space-4);

  &__controls {
    display: grid;
    grid-template-columns: 1fr repeat(2, minmax(160px, 220px));
    gap: var(--space-3);
    align-items: end;
  }

  &__error {
    color: var(--color-danger);
    font-size: 0.875rem;
  }
}

@media (max-width: 860px) {
  .integrations-page {
    &__controls {
      grid-template-columns: 1fr;
    }
  }
}
</style>
