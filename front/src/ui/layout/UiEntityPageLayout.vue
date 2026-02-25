<script setup lang="ts">
import {CircleHelp} from 'lucide-vue-next'
import UiBreadcrumbs, {
  type BreadcrumbItem,
} from '@/ui/components/common/UiBreadcrumbs.vue'
import UiTooltip from '@/ui/components/common/UiTooltip.vue'

withDefaults(
  defineProps<{
    title: string
    description?: string
    breadcrumbs?: BreadcrumbItem[]
  }>(),
  {
    description: '',
    breadcrumbs: () => [],
  },
)
</script>

<template>
  <section class="page-card entity-page-layout">
    <header class="entity-page-layout__header">
      <div class="entity-page-layout__header-main">
        <div class="entity-page-layout__title-row">
          <h1 class="page-title">{{ title }}</h1>

          <UiTooltip v-if="description" :text="description">
            <button
              type="button"
              class="entity-page-layout__help"
              :aria-label="`About ${title}`"
            >
              <CircleHelp :size="16" />
            </button>
          </UiTooltip>
        </div>

        <UiBreadcrumbs
          v-if="breadcrumbs.length > 0"
          :items="breadcrumbs"
        />

        <div v-if="$slots.meta" class="entity-page-layout__meta">
          <slot name="meta" />
        </div>
      </div>

      <div v-if="$slots.actions" class="entity-page-layout__actions">
        <slot name="actions" />
      </div>
    </header>

    <div class="entity-page-layout__content">
      <slot />
    </div>
  </section>
</template>

<style scoped lang="scss">
.entity-page-layout {
  display: grid;
  gap: var(--space-4);

  &__header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: var(--space-3);
  }

  &__header-main {
    min-width: 0;
    display: grid;
    gap: var(--space-2);
  }

  &__title-row {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
  }

  &__help {
    width: 28px;
    height: 28px;
    border-radius: 999px;
    border: 1px solid var(--color-border);
    background: var(--color-surface);
    color: var(--color-text-muted);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    cursor: help;
    flex-shrink: 0;

    &:hover {
      color: var(--color-text);
      background: var(--color-surface-soft);
    }
  }

  &__meta {
    color: var(--color-text-muted);
    font-size: 0.9375rem;
  }

  &__actions {
    display: inline-flex;
    gap: var(--space-2);
    align-items: center;
    flex-wrap: wrap;
    justify-content: flex-end;
  }

  &__content {
    display: grid;
    gap: var(--space-4);
  }
}

@media (max-width: 768px) {
  .entity-page-layout {
    &__header {
      flex-direction: column;
      align-items: stretch;
    }

    &__actions {
      justify-content: flex-start;
    }
  }
}
</style>
