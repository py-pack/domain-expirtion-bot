<script setup lang="ts">
defineProps<{
  variant?: 'primary' | 'secondary' | 'text';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
}>();
</script>

<template>
  <button 
    class="btn" 
    :class="[
      `btn-${variant || 'primary'}`, 
      `btn-${size || 'md'}`
    ]"
    :disabled="disabled"
  >
    <slot></slot>
  </button>
</template>

<style lang="scss" scoped>
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-2);
  font-weight: 500;
  border-radius: var(--border-radius-md);
  transition: all var(--transition-normal) ease;
  cursor: pointer;
  white-space: nowrap;
  
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    pointer-events: none;
  }
  
  &-primary {
    background-color: var(--color-primary);
    color: white;
    
    &:hover {
      background-color: var(--color-secondary);
    }
  }
  
  &-secondary {
    background-color: rgba(255, 255, 255, 0.1);
    color: var(--color-text);
    
    &:hover {
      background-color: rgba(255, 255, 255, 0.15);
    }
  }
  
  &-text {
    background-color: transparent;
    color: var(--color-text);
    
    &:hover {
      background-color: rgba(255, 255, 255, 0.05);
    }
  }
  
  &-sm {
    padding: var(--spacing-1) var(--spacing-3);
    font-size: var(--font-size-sm);
    height: 32px;
  }
  
  &-md {
    padding: var(--spacing-2) var(--spacing-4);
    font-size: var(--font-size-md);
    height: 40px;
  }
  
  &-lg {
    padding: var(--spacing-3) var(--spacing-6);
    font-size: var(--font-size-lg);
    height: 48px;
  }
}
</style>