<script setup lang="ts">
import type {RouteLocationRaw} from 'vue-router'

export interface BreadcrumbItem {
  label: string
  to?: RouteLocationRaw
}

defineProps<{
  items: BreadcrumbItem[]
}>()
</script>

<template>
  <nav class="ui-breadcrumbs" aria-label="Breadcrumb">
    <ol class="ui-breadcrumbs__list">
      <li
        v-for="(item, index) in items"
        :key="`${item.label}-${index}`"
        class="ui-breadcrumbs__item"
      >
        <RouterLink
          v-if="item.to"
          :to="item.to"
          class="ui-breadcrumbs__link"
        >
          {{ item.label }}
        </RouterLink>
        <span v-else class="ui-breadcrumbs__current" aria-current="page">
          {{ item.label }}
        </span>
      </li>
    </ol>
  </nav>
</template>

<style scoped lang="scss">
.ui-breadcrumbs {
  &__list {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-1) var(--space-2);
    align-items: center;
    margin: 0;
    padding: 0;
    list-style: none;
  }

  &__item {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
    color: var(--color-text-muted);
    font-size: 0.875rem;

    &:not(:last-child)::after {
      content: '/';
      color: var(--color-border);
    }
  }

  &__link {
    color: inherit;
    text-decoration: none;

    &:hover {
      color: var(--color-text);
    }
  }

  &__current {
    color: var(--color-text);
    font-weight: 600;
  }
}
</style>
