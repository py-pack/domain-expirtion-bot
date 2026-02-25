<script setup lang="ts">
import {computed, ref, watch} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import type {UnitResponsibleLevel} from '@/domain/units/model'
import {
  useCreateUnitMutation,
  useDeleteUnitMutation,
  useReplaceUnitResponsiblesMutation,
  useUnitQuery,
  useUnitResponsiblesQuery,
  useUnitsQuery,
  useUpdateUnitMutation,
} from '@/domain/units/queries'
import {useSystemUsersQuery} from '@/domain/users/queries'
import {getApiErrorMessage} from '@/shared/http/errors'
import UiButton from '@/ui/components/common/UiButton.vue'
import UiFormField from '@/ui/components/common/UiFormField.vue'
import UiTable from '@/ui/components/common/UiTable.vue'
import UiEntityPageLayout from '@/ui/layout/UiEntityPageLayout.vue'

type SettingsTab = 'general' | 'units' | 'notifications'

type SettingsTabItem = {
  id: SettingsTab
  label: string
}

const tabs: SettingsTabItem[] = [
  {id: 'general', label: 'General'},
  {id: 'units', label: 'Units'},
  {id: 'notifications', label: 'Notifications'},
]

const route = useRoute()
const router = useRouter()

const unitsQuery = useUnitsQuery()
const usersQuery = useSystemUsersQuery()
const createUnitMutation = useCreateUnitMutation()
const updateUnitMutation = useUpdateUnitMutation()
const deleteUnitMutation = useDeleteUnitMutation()
const replaceUnitResponsiblesMutation = useReplaceUnitResponsiblesMutation()

const createUnitName = ref('')
const editUnitName = ref('')
const selectedResponsibleUserIds = ref<number[]>([])
const responsibleLevels = ref<Record<number, UnitResponsibleLevel>>({})
const responsibleLevelOptions: readonly UnitResponsibleLevel[] = ['View', 'Edit', 'Full']

const unitsActionError = ref<string | null>(null)
const unitEditError = ref<string | null>(null)
const unitResponsiblesError = ref<string | null>(null)
const unitsActionSuccess = ref<string | null>(null)

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

const activeUnitId = computed<number | null>(() => {
  if (activeTab.value !== 'units') {
    return null
  }

  const rawValue = route.query.unitId
  const value = Array.isArray(rawValue) ? rawValue[0] : rawValue

  if (!value) {
    return null
  }

  const parsed = Number.parseInt(value, 10)
  return Number.isInteger(parsed) && parsed > 0 ? parsed : null
})

const unitQuery = useUnitQuery(activeUnitId)
const unitResponsiblesQuery = useUnitResponsiblesQuery(activeUnitId)

const units = computed(() => unitsQuery.data.value ?? [])
const systemUsers = computed(() => usersQuery.data.value ?? [])
const selectedUnitListItem = computed(
  () => units.value.find((unit) => unit.id === activeUnitId.value) ?? null,
)

watch(
  () => unitQuery.data.value,
  (unit) => {
    if (!unit) {
      return
    }

    editUnitName.value = unit.name
  },
  {immediate: true},
)

watch(
  () => unitResponsiblesQuery.data.value,
  (responsibles) => {
    const items = responsibles ?? []
    selectedResponsibleUserIds.value = items.map((user) => user.id)
    responsibleLevels.value = Object.fromEntries(
      items.map((user) => [user.id, user.level]),
    ) as Record<number, UnitResponsibleLevel>
  },
  {immediate: true},
)

async function selectTab(tab: SettingsTab): Promise<void> {
  const query: Record<string, string> = {}

  if (tab !== 'general') {
    query.tab = tab
  }

  if (tab === 'units' && activeUnitId.value !== null) {
    query.unitId = String(activeUnitId.value)
  }

  await router.replace({
    path: '/settings',
    query,
  })
}

async function openUnitEditor(unitId: number): Promise<void> {
  unitsActionError.value = null
  unitEditError.value = null
  unitResponsiblesError.value = null
  unitsActionSuccess.value = null

  await router.replace({
    path: '/settings',
    query: {
      tab: 'units',
      unitId: String(unitId),
    },
  })
}

async function closeUnitEditor(): Promise<void> {
  unitEditError.value = null
  unitResponsiblesError.value = null
  unitsActionSuccess.value = null

  await router.replace({
    path: '/settings',
    query: {
      tab: 'units',
    },
  })
}

async function createUnit(): Promise<void> {
  unitsActionError.value = null
  unitsActionSuccess.value = null

  try {
    const createdUnit = await createUnitMutation.mutateAsync({
      name: createUnitName.value.trim(),
    })

    createUnitName.value = ''
    unitsActionSuccess.value = 'Unit created successfully.'
    await openUnitEditor(createdUnit.id)
  } catch (error: unknown) {
    unitsActionError.value = getApiErrorMessage(error)
  }
}

async function saveUnit(): Promise<void> {
  unitEditError.value = null
  unitsActionSuccess.value = null

  if (activeUnitId.value === null) {
    unitEditError.value = 'Select a unit to edit.'
    return
  }

  try {
    await updateUnitMutation.mutateAsync({
      id: activeUnitId.value,
      payload: {
        name: editUnitName.value.trim(),
      },
    })

    unitsActionSuccess.value = 'Unit updated successfully.'
  } catch (error: unknown) {
    unitEditError.value = getApiErrorMessage(error)
  }
}

async function removeUnit(unitId: number): Promise<void> {
  unitsActionError.value = null
  unitsActionSuccess.value = null

  if (!window.confirm(`Delete unit #${unitId}?`)) {
    return
  }

  try {
    await deleteUnitMutation.mutateAsync(unitId)
    unitsActionSuccess.value = 'Unit deleted successfully.'

    if (activeUnitId.value === unitId) {
      await closeUnitEditor()
    }
  } catch (error: unknown) {
    unitsActionError.value = getApiErrorMessage(error)
  }
}

function toggleResponsible(userId: number, checked: boolean): void {
  if (checked) {
    if (!selectedResponsibleUserIds.value.includes(userId)) {
      selectedResponsibleUserIds.value = [...selectedResponsibleUserIds.value, userId]
    }
    if (!responsibleLevels.value[userId]) {
      responsibleLevels.value = {
        ...responsibleLevels.value,
        [userId]: 'View',
      }
    }
    return
  }

  selectedResponsibleUserIds.value = selectedResponsibleUserIds.value.filter(
    (currentUserId) => currentUserId !== userId,
  )
}

function isResponsibleSelected(userId: number): boolean {
  return selectedResponsibleUserIds.value.includes(userId)
}

function getResponsibleLevel(userId: number): UnitResponsibleLevel {
  return responsibleLevels.value[userId] ?? 'View'
}

function setResponsibleLevel(userId: number, level: UnitResponsibleLevel): void {
  responsibleLevels.value = {
    ...responsibleLevels.value,
    [userId]: level,
  }
}

function isUnitResponsibleLevel(value: string): value is UnitResponsibleLevel {
  return (
    value === 'View' ||
    value === 'Edit' ||
    value === 'Full'
  )
}

function onResponsibleLevelChange(userId: number, event: Event): void {
  const target = event.target
  if (!(target instanceof HTMLSelectElement)) {
    return
  }

  if (!isUnitResponsibleLevel(target.value)) {
    return
  }

  setResponsibleLevel(userId, target.value)
}

function onResponsibleChange(userId: number, event: Event): void {
  const target = event.target
  if (!(target instanceof HTMLInputElement)) {
    return
  }

  toggleResponsible(userId, target.checked)
}

async function saveResponsibles(): Promise<void> {
  unitResponsiblesError.value = null
  unitsActionSuccess.value = null

  if (activeUnitId.value === null) {
    unitResponsiblesError.value = 'Select a unit to manage responsibles.'
    return
  }

  try {
    await replaceUnitResponsiblesMutation.mutateAsync({
      unitId: activeUnitId.value,
      payload: {
        assignments: [...selectedResponsibleUserIds.value]
          .sort((a, b) => a - b)
          .map((userId) => ({
            user_id: userId,
            level: getResponsibleLevel(userId),
          })),
      },
    })

    unitsActionSuccess.value = 'Unit responsibles updated successfully.'
  } catch (error: unknown) {
    unitResponsiblesError.value = getApiErrorMessage(error)
  }
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
        <div class="settings-page__units-header">
          <div>
            <h2 class="settings-page__panel-title">Units</h2>
            <p class="settings-page__text">
              CRUD for units and separate management of unit responsible users.
            </p>
          </div>
        </div>

        <p v-if="unitsActionError" class="settings-page__error">{{ unitsActionError }}</p>
        <p v-if="unitsActionSuccess" class="settings-page__success">{{ unitsActionSuccess }}</p>

        <div class="settings-page__card">
          <form class="settings-page__inline-form" @submit.prevent="createUnit">
            <UiFormField
              id="settings-units-create-name"
              label="New unit name"
              :model-value="createUnitName"
              required
              @update:model-value="createUnitName = $event"
            />

            <UiButton type="submit" :disabled="createUnitMutation.isPending.value">
              {{ createUnitMutation.isPending.value ? 'Creating...' : 'Create unit' }}
            </UiButton>
          </form>
        </div>

        <p v-if="unitsQuery.error.value" class="settings-page__error">
          {{ getApiErrorMessage(unitsQuery.error.value) }}
        </p>
        <p v-else-if="unitsQuery.isLoading.value" class="settings-page__text-muted">
          Loading units...
        </p>
        <p v-else-if="units.length === 0" class="settings-page__text-muted">
          No units yet.
        </p>

        <UiTable v-else>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Responsibles</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="unit in units" :key="unit.id">
              <td>{{ unit.id }}</td>
              <td>{{ unit.name }}</td>
              <td>{{ unit.responsibles_count }}</td>
              <td class="settings-page__table-actions">
                <UiButton size="sm" variant="ghost" @click="openUnitEditor(unit.id)">
                  Edit
                </UiButton>
                <UiButton
                  size="sm"
                  variant="ghost"
                  :disabled="deleteUnitMutation.isPending.value"
                  @click="removeUnit(unit.id)"
                >
                  Delete
                </UiButton>
              </td>
            </tr>
          </tbody>
        </UiTable>

        <div class="settings-page__card settings-page__editor">
          <div class="settings-page__editor-head">
            <div>
              <h3 class="settings-page__section-title">Edit unit</h3>
              <p class="settings-page__text-muted">
                <template v-if="selectedUnitListItem">
                  Editing `{{ selectedUnitListItem.name }}` (ID: {{ selectedUnitListItem.id }})
                </template>
                <template v-else>
                  Select a unit from the table to edit.
                </template>
              </p>
            </div>

            <UiButton
              v-if="activeUnitId !== null"
              size="sm"
              variant="ghost"
              @click="closeUnitEditor"
            >
              Close editor
            </UiButton>
          </div>

          <p v-if="activeUnitId === null" class="settings-page__text-muted">
            Unit editor is inactive.
          </p>

          <template v-else>
            <p v-if="unitQuery.error.value" class="settings-page__error">
              {{ getApiErrorMessage(unitQuery.error.value) }}
            </p>
            <p v-else-if="unitQuery.isLoading.value" class="settings-page__text-muted">
              Loading unit...
            </p>

            <template v-else-if="unitQuery.data.value">
              <p v-if="unitEditError" class="settings-page__error">{{ unitEditError }}</p>

              <form class="settings-page__edit-form" @submit.prevent="saveUnit">
                <UiFormField
                  id="settings-units-edit-name"
                  label="Unit name"
                  :model-value="editUnitName"
                  required
                  @update:model-value="editUnitName = $event"
                />

                <UiButton type="submit" :disabled="updateUnitMutation.isPending.value">
                  {{ updateUnitMutation.isPending.value ? 'Saving...' : 'Save unit' }}
                </UiButton>
              </form>

              <div class="settings-page__responsibles">
                <div class="settings-page__responsibles-head">
                  <div>
                    <h4 class="settings-page__section-title">Unit responsibles</h4>
                    <p class="settings-page__text-muted">
                      Saved via separate endpoint for user-unit bindings.
                    </p>
                  </div>
                </div>

                <p v-if="unitResponsiblesError" class="settings-page__error">
                  {{ unitResponsiblesError }}
                </p>
                <p v-else-if="unitResponsiblesQuery.error.value" class="settings-page__error">
                  {{ getApiErrorMessage(unitResponsiblesQuery.error.value) }}
                </p>

                <p
                  v-if="usersQuery.error.value"
                  class="settings-page__error"
                >
                  {{ getApiErrorMessage(usersQuery.error.value) }}
                </p>
                <p v-else-if="usersQuery.isLoading.value" class="settings-page__text-muted">
                  Loading users...
                </p>
                <p
                  v-else-if="unitResponsiblesQuery.isLoading.value"
                  class="settings-page__text-muted"
                >
                  Loading current responsibles...
                </p>
                <p v-else-if="systemUsers.length === 0" class="settings-page__text-muted">
                  No users available for assignment.
                </p>

                <div v-else class="settings-page__checkbox-list">
                  <label
                    v-for="user in systemUsers"
                    :key="user.id"
                    class="settings-page__checkbox"
                  >
                    <div class="settings-page__checkbox-main">
                      <input
                        type="checkbox"
                        :checked="isResponsibleSelected(user.id)"
                        @change="onResponsibleChange(user.id, $event)"
                      />
                      <span>{{ user.full_name }} ({{ user.email }})</span>
                    </div>
                    <select
                      class="settings-page__level-select"
                      :disabled="!isResponsibleSelected(user.id)"
                      :value="getResponsibleLevel(user.id)"
                      @change="onResponsibleLevelChange(user.id, $event)"
                    >
                      <option
                        v-for="level in responsibleLevelOptions"
                        :key="level"
                        :value="level"
                      >
                        {{ level }}
                      </option>
                    </select>
                  </label>
                </div>

                <UiButton
                  type="button"
                  :disabled="
                    replaceUnitResponsiblesMutation.isPending.value ||
                    usersQuery.isLoading.value ||
                    unitResponsiblesQuery.isLoading.value
                  "
                  @click="saveResponsibles"
                >
                  {{
                    replaceUnitResponsiblesMutation.isPending.value
                      ? 'Saving responsibles...'
                      : 'Save responsibles'
                  }}
                </UiButton>
              </div>
            </template>
          </template>
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
    gap: var(--space-4);
  }

  &__units-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: var(--space-3);
  }

  &__panel-title {
    margin: 0;
    font-size: 1.125rem;
  }

  &__section-title {
    margin: 0;
    font-size: 1rem;
  }

  &__text {
    margin: 0;
    color: var(--color-text);
  }

  &__text-muted {
    margin: 0;
    color: var(--color-text-muted);
  }

  &__error {
    margin: 0;
    color: var(--color-danger);
    font-size: 0.875rem;
  }

  &__success {
    margin: 0;
    color: var(--color-success);
    font-size: 0.875rem;
  }

  &__card {
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    background: var(--color-surface);
    padding: var(--space-3);
    box-shadow: var(--card-shadow);
  }

  &__inline-form {
    display: grid;
    gap: var(--space-3);
    align-items: end;
    grid-template-columns: minmax(220px, 420px) auto;
  }

  &__table-actions {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
  }

  &__editor {
    display: grid;
    gap: var(--space-4);
  }

  &__editor-head {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: var(--space-3);
  }

  &__edit-form {
    display: grid;
    gap: var(--space-3);
    max-width: 520px;
  }

  &__responsibles {
    display: grid;
    gap: var(--space-3);
    padding-top: var(--space-3);
    border-top: 1px solid var(--color-border);
  }

  &__responsibles-head {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: var(--space-3);
  }

  &__checkbox-list {
    display: grid;
    gap: var(--space-2);
    max-height: 320px;
    overflow: auto;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    padding: var(--space-3);
    background: var(--color-surface-soft);
  }

  &__checkbox {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--space-3);
    color: var(--color-text);
  }

  &__checkbox-main {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
    min-width: 0;
  }

  &__level-select {
    min-width: 120px;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    background: var(--color-surface);
    color: var(--color-text);
    min-height: 32px;
    padding: 0 var(--space-2);
  }
}

@media (max-width: 900px) {
  .settings-page {
    &__inline-form {
      grid-template-columns: 1fr;
      align-items: stretch;
    }

    &__editor-head {
      flex-direction: column;
      align-items: stretch;
    }
  }
}
</style>
