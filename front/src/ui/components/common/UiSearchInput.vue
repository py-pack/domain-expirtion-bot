<script setup lang="ts">
import {Search} from 'lucide-vue-next'

withDefaults(
  defineProps<{
    modelValue: string
    placeholder?: string
  }>(),
  {
    placeholder: 'Search',
  },
)

const emit = defineEmits<{
  (event: 'update:modelValue', value: string): void
}>()

function onInput(event: Event): void {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', target.value)
}
</script>

<template>
  <label class="ui-search-input">
    <Search :size="16" class="ui-search-input__icon" />
    <input
      class="ui-input ui-search-input__field"
      type="text"
      :value="modelValue"
      :placeholder="placeholder"
      @input="onInput"
    />
  </label>
</template>

<style scoped lang="scss">
.ui-search-input {
  position: relative;
  display: block;

  &__icon {
    position: absolute;
    top: 50%;
    left: var(--space-3);
    transform: translateY(-50%);
    color: var(--color-text-muted);
    pointer-events: none;
  }

  &__field {
    padding-left: 34px;
  }
}
</style>
