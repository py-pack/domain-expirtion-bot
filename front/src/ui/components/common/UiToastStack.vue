<script setup lang="ts">
import {AlertCircle, CheckCircle2, X} from 'lucide-vue-next'
import {useToastState} from '@/shared/ui/toast'

const {toasts, removeToast} = useToastState()
</script>

<template>
  <Teleport to="body">
    <div v-if="toasts.length > 0" class="toast-stack" aria-live="polite" aria-atomic="false">
      <TransitionGroup name="toast">
        <div
          v-for="toast in toasts"
          :key="toast.id"
          class="toast-stack__item"
          :class="`toast-stack__item--${toast.variant}`"
          :role="toast.variant === 'error' ? 'alert' : 'status'"
        >
          <component
            :is="toast.variant === 'success' ? CheckCircle2 : AlertCircle"
            class="toast-stack__icon"
            aria-hidden="true"
          />
          <p class="toast-stack__message">{{ toast.message }}</p>
          <button
            type="button"
            class="toast-stack__close"
            aria-label="Close notification"
            @click="removeToast(toast.id)"
          >
            <X :size="16" aria-hidden="true" />
          </button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<style scoped lang="scss">
.toast-stack {
  position: fixed;
  right: var(--space-4);
  bottom: var(--space-4);
  z-index: 1200;
  display: grid;
  gap: var(--space-2);
  width: min(380px, calc(100vw - (var(--space-4) * 2)));
  pointer-events: none;

  &__item {
    pointer-events: auto;
    display: grid;
    grid-template-columns: auto 1fr auto;
    align-items: start;
    gap: var(--space-2);
    margin: 0;
    padding: var(--space-3);
    border-radius: var(--radius-md);
    border: 1px solid var(--color-border);
    background: var(--color-surface);
    box-shadow: var(--card-shadow);
  }

  &__item--success {
    border-color: color-mix(in srgb, var(--color-success), var(--color-border) 60%);
  }

  &__item--error {
    border-color: color-mix(in srgb, var(--color-danger), var(--color-border) 60%);
  }

  &__icon {
    margin-top: 2px;
    width: 16px;
    height: 16px;
    flex-shrink: 0;
  }

  &__item--success &__icon {
    color: var(--color-success);
  }

  &__item--error &__icon {
    color: var(--color-danger);
  }

  &__message {
    margin: 0;
    color: var(--color-text);
    font-size: 0.875rem;
    line-height: 1.4;
  }

  &__close {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    margin: -2px -2px 0 0;
    border: 0;
    border-radius: var(--radius-sm);
    background: transparent;
    color: var(--color-text-muted);
    cursor: pointer;
  }

  &__close:hover {
    background: color-mix(in srgb, var(--color-primary-soft), transparent 40%);
    color: var(--color-text);
  }
}

.toast-enter-active,
.toast-leave-active {
  transition:
    opacity 160ms ease,
    transform 160ms ease;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateY(8px);
}

@media (prefers-reduced-motion: reduce) {
  .toast-enter-active,
  .toast-leave-active {
    transition: none;
  }
}
</style>
