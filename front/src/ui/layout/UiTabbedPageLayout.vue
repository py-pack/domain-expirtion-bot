<script setup lang="ts">
import {useRoute, type RouteLocationRaw} from 'vue-router'
import type {BreadcrumbItem} from '@/ui/components/common/UiBreadcrumbs.vue'
import UiEntityPageLayout from '@/ui/layout/UiEntityPageLayout.vue'

export type TabbedPageTabItem = {
  label: string
  to: RouteLocationRaw
  matchPrefix?: string
}

const props = withDefaults(
  defineProps<{
    title: string
    description?: string
    tabs: TabbedPageTabItem[]
    breadcrumbs?: BreadcrumbItem[]
  }>(),
  {
    description: '',
    breadcrumbs: undefined,
  },
)

const route = useRoute()

function isTabMatchedByPrefix(tab: TabbedPageTabItem): boolean {
  return typeof tab.matchPrefix === 'string' && route.path.startsWith(tab.matchPrefix)
}
</script>

<template>
  <UiEntityPageLayout
    class="tabbed-page-layout"
    :title="props.title"
    :description="props.description"
    :breadcrumbs="props.breadcrumbs ?? [{label: props.title}]"
  >
    <template v-if="$slots.meta" #meta>
      <slot name="meta" />
    </template>

    <template v-if="$slots.actions" #actions>
      <slot name="actions" />
    </template>

    <nav class="tabbed-page-layout__tabs" aria-label="Page tabs">
      <RouterLink
        v-for="tab in props.tabs"
        :key="tab.label"
        :to="tab.to"
        class="tabbed-page-layout__tab"
        :class="{'tabbed-page-layout__tab--active': isTabMatchedByPrefix(tab)}"
        active-class="tabbed-page-layout__tab--active"
      >
        {{ tab.label }}
      </RouterLink>
    </nav>

    <div class="tabbed-page-layout__content">
      <slot />
    </div>
  </UiEntityPageLayout>
</template>

<style scoped lang="scss">
.tabbed-page-layout {
  display: grid;
  gap: var(--space-4);

  &__tabs {
    display: flex;
    gap: var(--space-2);
    flex-wrap: wrap;
    padding-bottom: var(--space-2);
    border-bottom: 1px solid var(--color-border);
  }

  &__tab {
    border: 1px solid var(--color-border);
    background: var(--color-surface);
    color: var(--color-text);
    border-radius: var(--radius-sm);
    min-height: 36px;
    padding: 0 var(--space-3);
    display: inline-flex;
    align-items: center;
    font-weight: 500;

    &:hover {
      background: var(--color-surface-soft);
    }

    &--active {
      border-color: var(--color-primary);
      color: var(--color-primary);
      background: var(--color-primary-soft);
    }
  }

  &__content {
    display: grid;
    gap: var(--space-4);
  }
}
</style>
