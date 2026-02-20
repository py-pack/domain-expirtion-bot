<template>
  <section class="page-card">
    <h1 class="page-title">Dashboard</h1>
    <p class="page-subtitle">Overview of active integrations and domain health.</p>

    <UiEmptyState
      title="Dashboard metrics are coming next"
      description="Wire analytics endpoints in domain modules and render charts from prepared DTOs."
    />
  </section>
</template>

<script setup lang="ts">
import UiEmptyState from '@/ui/components/common/UiEmptyState.vue'
</script>
