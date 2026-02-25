<script setup lang="ts">
import UiEntityPageLayout from '@/ui/layout/UiEntityPageLayout.vue'
import UiEmptyState from '@/ui/components/common/UiEmptyState.vue'
</script>

<template>
  <UiEntityPageLayout
    title="Logs"
    description="Security and activity timeline for integrations and authentication events."
    :breadcrumbs="[{label: 'Logs'}]"
  >
    <UiEmptyState
      title="Logs feed is not connected yet"
      description="Add the backend log endpoint and bind it through domain repository/query files."
    />
  </UiEntityPageLayout>
</template>
