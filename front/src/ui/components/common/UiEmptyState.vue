<script setup lang="ts">
withDefaults(
  defineProps<{
    title: string
    description: string
  }>(),
  {},
)
</script>

<template>
  <section class="ui-empty-state">
    <h3>{{ title }}</h3>
    <p>{{ description }}</p>
  </section>
</template>

<style scoped lang="scss">
.ui-empty-state {
  border: 1px dashed var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-5);
  text-align: center;
  background: var(--color-surface);

  h3 {
    margin-bottom: var(--space-2);
  }
}
</style>
