<script setup lang="ts">
import { ref } from 'vue';
import IconSearch from '../icons/IconSearch.vue';

const props = defineProps<{
  placeholder?: string;
}>();

const emit = defineEmits<{
  (e: 'update:search', value: string): void;
}>();

const searchValue = ref('');

const updateSearch = (event: Event) => {
  const input = event.target as HTMLInputElement;
  searchValue.value = input.value;
  emit('update:search', searchValue.value);
}
</script>

<template>
  <div class="search-bar">
    <IconSearch class="search-bar__icon" />
    <input 
      type="text" 
      class="search-bar__input" 
      :placeholder="placeholder || 'Search...'" 
      v-model="searchValue"
      @input="updateSearch"
    />
  </div>
</template>

<style lang="scss" scoped>
.search-bar {
  position: relative;
  width: 100%;
  
  &__icon {
    position: absolute;
    left: var(--spacing-3);
    top: 50%;
    transform: translateY(-50%);
    color: var(--color-text-secondary);
  }
  
  &__input {
    width: 100%;
    padding: var(--spacing-3) var(--spacing-3) var(--spacing-3) var(--spacing-8);
    background-color: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--border-radius-md);
    color: var(--color-text);
    
    &::placeholder {
      color: var(--color-text-secondary);
    }
    
    &:focus {
      border-color: var(--color-primary);
    }
  }
}
</style>