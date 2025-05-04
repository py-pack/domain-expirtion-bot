<script setup lang="ts">
import { ref, onUnmounted } from 'vue';
import IconChevronDown from '../icons/IconChevronDown.vue';

const props = defineProps<{
  label: string;
  options: { value: string; label: string }[];
  modelValue?: string;
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void;
}>();

const isOpen = ref(false);
const selectedValue = ref(props.modelValue || '');

const toggleDropdown = () => {
  isOpen.value = !isOpen.value;
};

const selectOption = (value: string) => {
  selectedValue.value = value;
  emit('update:modelValue', value);
  isOpen.value = false;
};

// Close dropdown when clicking outside
const dropdownRef = ref<HTMLDivElement | null>(null);
const handleClickOutside = (event: MouseEvent) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target as Node)) {
    isOpen.value = false;
  }
};

// Add click outside listener
const addOutsideClickListener = () => {
  document.addEventListener('click', handleClickOutside);
};

// Clean up
const removeOutsideClickListener = () => {
  document.removeEventListener('click', handleClickOutside);
};

// Watch for dropdown open/close to add/remove listener
const watchIsOpen = (val: boolean) => {
  if (val) {
    // Delay to avoid immediate trigger
    setTimeout(addOutsideClickListener, 0);
  } else {
    removeOutsideClickListener();
  }
}

// Clean up on component unmount
onUnmounted(() => {
  removeOutsideClickListener();
});
</script>

<template>
  <div class="dropdown" ref="dropdownRef">
    <button class="dropdown__toggle" @click="toggleDropdown">
      <span>{{ label }}</span>
      <IconChevronDown class="dropdown__icon" :class="{ 'dropdown__icon--open': isOpen }" />
    </button>
    
    <div v-if="isOpen" class="dropdown__menu">
      <div 
        v-for="option in options" 
        :key="option.value" 
        class="dropdown__item"
        :class="{ 'dropdown__item--active': selectedValue === option.value }"
        @click="selectOption(option.value)"
      >
        {{ option.label }}
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.dropdown {
  position: relative;
  
  &__toggle {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--spacing-3) var(--spacing-4);
    background-color: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--border-radius-md);
    min-width: 180px;
    cursor: pointer;
    
    &:hover {
      border-color: var(--color-text-secondary);
    }
  }
  
  &__icon {
    margin-left: var(--spacing-2);
    transition: transform var(--transition-fast) ease;
    
    &--open {
      transform: rotate(180deg);
    }
  }
  
  &__menu {
    position: absolute;
    top: calc(100% + var(--spacing-1));
    left: 0;
    right: 0;
    background-color: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--border-radius-md);
    box-shadow: var(--shadow-lg);
    z-index: 10;
    max-height: 250px;
    overflow-y: auto;
    animation: fadeIn var(--transition-fast) ease;
  }
  
  &__item {
    padding: var(--spacing-3) var(--spacing-4);
    cursor: pointer;
    transition: background-color var(--transition-fast) ease;
    
    &:hover {
      background-color: rgba(255, 255, 255, 0.05);
    }
    
    &--active {
      background-color: rgba(33, 150, 243, 0.1);
      color: var(--color-primary);
    }
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>