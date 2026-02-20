<script setup lang="ts">
defineProps<{
  text: string
}>()
</script>

<template>
  <span class="ui-unit-tag">{{ text }}</span>
</template>

<style scoped lang="scss">
.ui-unit-tag {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 2px var(--space-2);
  border-radius: var(--radius-sm);
  background: var(--color-surface-soft);
  color: var(--color-text);
  font-size: 0.75rem;
  font-weight: 600;
}
</style>
