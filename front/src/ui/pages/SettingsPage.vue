<script setup lang="ts">
import {computed} from 'vue'
import {CornerUpLeft, Plus} from 'lucide-vue-next'
import {useRoute, useRouter} from 'vue-router'
import {useUnitQuery} from '@/domain/units/queries'
import UiButton from '@/ui/components/common/UiButton.vue'
import UiTabbedPageLayout, {
  type TabbedPageTabItem,
} from '@/ui/layout/UiTabbedPageLayout.vue'

const route = useRoute()
const router = useRouter()

const tabs: TabbedPageTabItem[] = [
  {label: 'General', to: {name: 'settings-general'}, matchPrefix: '/settings/general'},
  {label: 'Units', to: {name: 'settings-units'}, matchPrefix: '/settings/units'},
  {
    label: 'Notifications',
    to: {name: 'settings-notifications'},
    matchPrefix: '/settings/notifications',
  },
]

const showCreateUnitAction = computed(() => route.name === 'settings-units')

const settingsUnitEditId = computed<number | null>(() => {
  if (route.name !== 'settings-units-edit') {
    return null
  }

  const rawId = route.params.id
  const value = Array.isArray(rawId) ? rawId[0] : rawId
  if (!value) {
    return null
  }

  const parsed = Number.parseInt(value, 10)
  return Number.isInteger(parsed) && parsed > 0 ? parsed : null
})

const settingsUnitEditQuery = useUnitQuery(settingsUnitEditId)

const pageTitle = computed(() => {
  if (
    route.name === 'settings-units' ||
    route.name === 'settings-units-create' ||
    route.name === 'settings-units-edit'
  ) {
    return route.name === 'settings-units' ? 'Units (Setting)' : 'Unit (Setting)'
  }

  if (route.name === 'settings-general') {
    return 'General (Setting)'
  }

  if (route.name === 'settings-notifications') {
    return 'Notifications (Setting)'
  }

  return 'Setting'
})

const pageBreadcrumbs = computed(() => {
  if (route.name === 'settings-general') {
    return [{label: 'Setting'}, {label: 'General'}]
  }

  if (route.name === 'settings-notifications') {
    return [{label: 'Setting'}, {label: 'Notifications'}]
  }

  if (route.name === 'settings-units') {
    return [{label: 'Setting'}, {label: 'Unit'}]
  }

  if (route.name === 'settings-units-create') {
    return [{label: 'Setting'}, {label: 'Unit', to: {name: 'settings-units'}}, {label: 'Create'}]
  }

  if (route.name === 'settings-units-edit') {
    const unitId = settingsUnitEditId.value
    const unitName = settingsUnitEditQuery.data.value?.name
    const editLabel =
      unitId === null
        ? 'Edit'
        : `Edit ${unitName ?? ''}${unitName ? ' ' : ''}(ID: ${unitId})`

    return [
      {label: 'Setting'},
      {label: 'Unit', to: {name: 'settings-units'}},
      {label: editLabel},
    ]
  }

  return [{label: 'Setting'}]
})

function openCreateUnitPage(): void {
  void router.push({name: 'settings-units-create'})
}

function goBackToUnits(): void {
  void router.push({name: 'settings-units'})
}
</script>

<template>
  <UiTabbedPageLayout
    :title="pageTitle"
    description="System-level settings grouped by sections."
    :tabs="tabs"
    :breadcrumbs="pageBreadcrumbs"
  >
    <template v-if="showCreateUnitAction" #actions>
      <UiButton tone="success" @click="openCreateUnitPage">
        <template #icon>
          <Plus :size="16" />
        </template>
        Create unit
      </UiButton>
    </template>
    <template
      v-else-if="route.name === 'settings-units-create' || route.name === 'settings-units-edit'"
      #actions
    >
      <UiButton variant="ghost" @click="goBackToUnits">
        <template #icon>
          <CornerUpLeft :size="16" />
        </template>
        Back to units
      </UiButton>
    </template>

    <RouterView />
  </UiTabbedPageLayout>
</template>
