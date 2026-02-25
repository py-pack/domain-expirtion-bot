<script setup lang="ts">
import {computed} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import UiEntityPageLayout from '@/ui/layout/UiEntityPageLayout.vue'

type SettingsTab = 'general' | 'units' | 'notifications'

type SettingsTabItem = {
  id: SettingsTab
  label: string
  description: string
}

const tabs: SettingsTabItem[] = [
  {
    id: 'general',
    label: 'General',
    description: 'Global application preferences and defaults.',
  },
  {
    id: 'units',
    label: 'Units',
    description: 'Configure units and formatting used across the admin panel.',
  },
  {
    id: 'notifications',
    label: 'Notifications',
    description: 'Notification-related defaults and delivery preferences.',
  },
]

const route = useRoute()
const router = useRouter()

function isSettingsTab(value: unknown): value is SettingsTab {
  return value === 'general' || value === 'units' || value === 'notifications'
}

const activeTab = computed<SettingsTab>(() => {
  const tab = route.query.tab
  if (typeof tab === 'string' && isSettingsTab(tab)) {
    return tab
  }

  return 'general'
})

async function selectTab(tab: SettingsTab): Promise<void> {
  await router.replace({
    path: '/settings',
    query: tab === 'general' ? {} : {tab},
  })
}
</script>

<template>
  <UiEntityPageLayout
    class="settings-page"
    title="Settings"
    description="System-level settings grouped by sections."
    :breadcrumbs="[{label: 'Settings'}]"
  >
    <div class="settings-page__tabs" role="tablist" aria-label="Settings sections">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        type="button"
        class="settings-page__tab"
        :class="{'settings-page__tab--active': activeTab === tab.id}"
        role="tab"
        :aria-selected="activeTab === tab.id"
        @click="selectTab(tab.id)"
      >
        {{ tab.label }}
      </button>
    </div>

    <section class="settings-page__panel" role="tabpanel" :aria-label="activeTab">
      <template v-if="activeTab === 'general'">
        <h2 class="settings-page__panel-title">General</h2>
        <p class="settings-page__text">
          General system settings will be configured here.
        </p>
      </template>

      <template v-else-if="activeTab === 'units'">
        <h2 class="settings-page__panel-title">Units</h2>
        <p class="settings-page__text">
          Manage measurement units and formatting rules used in reports and forms.
        </p>
        <div class="settings-page__card">
          <p class="settings-page__text-muted">
            Unit management UI placeholder. Add unit list/table and actions here.
          </p>
        </div>
      </template>

      <template v-else>
        <h2 class="settings-page__panel-title">Notifications</h2>
        <p class="settings-page__text">
          Notification defaults and alert settings will be available here.
        </p>
      </template>
    </section>
  </UiEntityPageLayout>
</template>

<style scoped lang="scss">
.settings-page {
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
    font: inherit;
    cursor: pointer;

    &:hover {
      background: var(--color-surface-soft);
    }

    &--active {
      border-color: var(--color-primary);
      color: var(--color-primary);
      background: var(--color-primary-soft);
    }
  }

  &__panel {
    display: grid;
    gap: var(--space-3);
    max-width: 720px;
  }

  &__panel-title {
    margin: 0;
    font-size: 1.125rem;
  }

  &__text {
    margin: 0;
    color: var(--color-text);
  }

  &__text-muted {
    margin: 0;
    color: var(--color-text-muted);
  }

  &__card {
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    background: var(--color-surface);
    padding: var(--space-3);
    box-shadow: var(--card-shadow);
  }
}
</style>
