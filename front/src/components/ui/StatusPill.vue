<script setup lang="ts">
defineProps<{
  status: 'active' | 'inactive' | 'warning' | 'error';
}>();
</script>

<template>
  <div class="status-pill" :class="status">
    {{ status.charAt(0).toUpperCase() + status.slice(1) }}
  </div>
</template>

<style lang="scss" scoped>
.status-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-1) var(--spacing-3);
  border-radius: var(--border-radius-full);
  font-size: var(--font-size-sm);
  font-weight: 500;
  
  &.active {
    background-color: rgba(76, 175, 80, 0.15);
    color: var(--color-success);
  }
  
  &.inactive {
    background-color: rgba(158, 158, 158, 0.15);
    color: var(--color-text-secondary);
  }
  
  &.warning {
    background-color: rgba(255, 152, 0, 0.15);
    color: var(--color-warning);
  }
  
  &.error {
    background-color: rgba(244, 67, 54, 0.15);
    color: var(--color-error);
  }
}
</style>