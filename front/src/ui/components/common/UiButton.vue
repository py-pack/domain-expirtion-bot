<script setup lang="ts">
withDefaults(
  defineProps<{
    variant?: 'primary' | 'secondary' | 'ghost'
    tone?: 'default' | 'success' | 'danger' | 'warning'
    size?: 'sm' | 'md' | 'lg'
    type?: 'button' | 'submit' | 'reset'
    disabled?: boolean
    iconOnly?: boolean
    ariaLabel?: string
  }>(),
  {
    variant: 'primary',
    tone: 'default',
    size: 'md',
    type: 'button',
    disabled: false,
    iconOnly: false,
    ariaLabel: undefined,
  },
)
</script>

<template>
  <button
    :type="type"
    class="ui-button"
    :class="[
      `ui-button--${variant}`,
      `ui-button--${tone}`,
      `ui-button--${size}`,
      {'ui-button--icon-only': iconOnly},
    ]"
    :disabled="disabled"
    :aria-label="ariaLabel"
  >
    <span v-if="$slots.icon" class="ui-button__icon">
      <slot name="icon" />
    </span>
    <span v-if="$slots.default" class="ui-button__label">
      <slot />
    </span>
  </button>
</template>
