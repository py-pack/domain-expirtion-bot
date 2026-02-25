<template>
  <UiEntityPageLayout
    title="Dashboard"
    description="Overview of active integrations and domain health."
    :breadcrumbs="[{label: 'Dashboard'}]"
  >
    <UiEmptyState
      title="Dashboard metrics are coming next"
      description="Wire analytics endpoints in domain modules and render charts from prepared DTOs."
    />
  </UiEntityPageLayout>
</template>

<script setup lang="ts">
import UiEntityPageLayout from '@/ui/layout/UiEntityPageLayout.vue'
import UiEmptyState from '@/ui/components/common/UiEmptyState.vue'
</script>
