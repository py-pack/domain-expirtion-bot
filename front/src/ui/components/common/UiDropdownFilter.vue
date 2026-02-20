<script setup lang="ts">
defineProps<{
  label: string
  modelValue: string
  options: Array<{value: string; label: string}>
}>()

const emit = defineEmits<{
  (event: 'update:modelValue', value: string): void
}>()

function onChange(event: Event): void {
  const target = event.target as HTMLSelectElement
  emit('update:modelValue', target.value)
}
</script>

<template>
  <label class="ui-dropdown-filter">
    <span class="ui-dropdown-filter__label">{{ label }}</span>
    <select class="ui-select" :value="modelValue" @change="onChange">
      <option v-for="option in options" :key="option.value" :value="option.value">
        {{ option.label }}
      </option>
    </select>
  </label>
</template>

<style scoped lang="scss">
.ui-dropdown-filter {
  display: grid;
  gap: var(--space-1);

  &__label {
    font-size: 0.875rem;
    color: var(--color-text-muted);
    font-weight: 600;
  }
}
</style>
