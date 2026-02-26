<script setup lang="ts">
import type {IntegrationStatus} from '@/domain/integrations/model'

defineProps<{
  status: IntegrationStatus
}>()

function toLabel(status: IntegrationStatus): string {
  return status.charAt(0).toUpperCase() + status.slice(1)
}
</script>

<template>
  <span class="ui-status-pill" :class="`ui-status-pill--${status}`">
    {{ toLabel(status) }}
  </span>
</template>

<style scoped lang="scss">
.ui-status-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 2px var(--space-2);
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 600;

  &--active {
    color: var(--color-success);
    background: color-mix(in srgb, var(--color-success), transparent 86%);
  }

  &--inactive {
    color: var(--color-text-muted);
    background: color-mix(in srgb, var(--color-text-muted), transparent 86%);
  }

  &--warning {
    color: var(--color-warning);
    background: color-mix(in srgb, var(--color-warning), transparent 86%);
  }

  &--ban {
    color: var(--color-danger);
    background: color-mix(in srgb, var(--color-danger), transparent 86%);
  }
}
</style>
