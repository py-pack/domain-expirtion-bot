<script setup lang="ts">
withDefaults(
  defineProps<{
    id: string
    label: string
    modelValue: string
    type?: 'text' | 'email' | 'password'
    autocomplete?: string
    required?: boolean
    readonly?: boolean
  }>(),
  {
    type: 'text',
    autocomplete: 'off',
    required: false,
    readonly: false,
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
  <label class="ui-form-field" :for="id">
    <span class="ui-form-label">{{ label }}</span>
    <input
      :id="id"
      class="ui-input"
      :type="type"
      :autocomplete="autocomplete"
      :required="required"
      :readonly="readonly"
      :value="modelValue"
      @input="onInput"
    />
  </label>
</template>
