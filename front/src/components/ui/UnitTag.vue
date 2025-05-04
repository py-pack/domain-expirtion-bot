<script setup lang="ts">
defineProps<{
  text: string;
}>();
</script>

<template>
  <span class="unit-tag">{{ text }}</span>
</template>

<style lang="scss" scoped>
.unit-tag {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-1) var(--spacing-2);
  border-radius: var(--border-radius-md);
  font-size: var(--font-size-xs);
  font-weight: 500;
  background-color: rgba(255, 255, 255, 0.1);
  color: var(--color-text);
  margin-right: var(--spacing-1);
}
</style>