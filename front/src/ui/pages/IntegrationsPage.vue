<script setup lang="ts">
import {computed, ref} from 'vue'
import type {IntegrationStatus} from '@/domain/integrations/model'
import {useIntegrationsQuery} from '@/domain/integrations/queries'
import {integrationsService} from '@/domain/integrations/service'
import {getApiErrorMessage} from '@/shared/http/errors'
import UiButton from '@/ui/components/common/UiButton.vue'
import UiDropdownFilter from '@/ui/components/common/UiDropdownFilter.vue'
import UiEmptyState from '@/ui/components/common/UiEmptyState.vue'
import UiSearchInput from '@/ui/components/common/UiSearchInput.vue'
import IntegrationsTable from '@/ui/components/integrations/IntegrationsTable.vue'

const searchQuery = ref('')
const statusFilter = ref<'all' | IntegrationStatus>('all')
const typeFilter = ref<'all' | string>('all')

const integrationsQuery = useIntegrationsQuery()

const integrations = computed(() => integrationsQuery.data.value ?? [])

const filteredIntegrations = computed(() =>
  integrationsService.filter(integrations.value, {
    searchQuery: searchQuery.value,
    statusFilter: statusFilter.value,
    typeFilter: typeFilter.value,
  }),
)

const statusOptions = [
  {value: 'all', label: 'All Statuses'},
  {value: 'active', label: 'Active'},
  {value: 'inactive', label: 'Inactive'},
  {value: 'warning', label: 'Warning'},
  {value: 'error', label: 'Error'},
]

const typeOptions = computed(() => {
  const uniqueTypes = [...new Set(integrations.value.map((integration) => integration.type))]

  return [
    {value: 'all', label: 'All Types'},
    ...uniqueTypes.map((type) => ({
      value: type,
      label: type.charAt(0).toUpperCase() + type.slice(1),
    })),
  ]
})

const errorMessage = computed(() => {
  if (!integrationsQuery.error.value) {
    return null
  }

  return getApiErrorMessage(integrationsQuery.error.value)
})
</script>

<template>
  <section class="page-card integrations-page">
    <header class="integrations-page__header">
      <div>
        <h1 class="page-title">Integrations</h1>
        <p class="page-subtitle">Manage provider connections and sync status.</p>
      </div>

      <UiButton> Add integration </UiButton>
    </header>

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
  </section>
</template>

<style scoped lang="scss">
.integrations-page {
  display: grid;
  gap: var(--space-4);

  &__header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: var(--space-3);
  }

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

    &__header {
      flex-direction: column;
    }
  }
}
</style>
