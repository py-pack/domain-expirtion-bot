<script setup lang="ts">
import UiEmptyState from '@/ui/components/common/UiEmptyState.vue'
</script>

<template>
  <section class="page-card">
    <h1 class="page-title">Logs</h1>
    <p class="page-subtitle">Security and activity timeline for integrations and auth actions.</p>

    <UiEmptyState
      title="Logs feed is not connected yet"
      description="Add the backend log endpoint and bind it through domain repository/query files."
    />
  </section>
</template>
