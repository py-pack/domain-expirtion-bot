<script setup lang="ts">
import {computed, ref, watch} from 'vue'
import {Plus, Save} from 'lucide-vue-next'
import {useRoute} from 'vue-router'
import type {UnitResponsibleLevel} from '@/domain/units/model'
import {
  useReplaceUnitResponsiblesMutation,
  useUnitQuery,
  useUnitResponsiblesQuery,
  useUpdateUnitMutation,
} from '@/domain/units/queries'
import {useSystemUsersQuery} from '@/domain/users/queries'
import {getApiErrorMessage} from '@/shared/http/errors'
import {showErrorToast, showSuccessToast} from '@/shared/ui/toast'
import UiButton from '@/ui/components/common/UiButton.vue'
import UiFormField from '@/ui/components/common/UiFormField.vue'
import UnitResponsiblesRepeater, {
  type UnitResponsibleDraftRow,
} from '@/ui/components/units/UnitResponsiblesRepeater.vue'

const route = useRoute()

const usersQuery = useSystemUsersQuery()
const updateUnitMutation = useUpdateUnitMutation()
const replaceUnitResponsiblesMutation = useReplaceUnitResponsiblesMutation()

const unitId = computed<number | null>(() => {
  const rawId = route.params.id
  const value = Array.isArray(rawId) ? rawId[0] : rawId

  if (!value) {
    return null
  }

  const parsed = Number.parseInt(value, 10)
  return Number.isInteger(parsed) && parsed > 0 ? parsed : null
})

const unitQuery = useUnitQuery(unitId)
const unitResponsiblesQuery = useUnitResponsiblesQuery(unitId)

const unitName = ref('')
const responsibleRows = ref<UnitResponsibleDraftRow[]>([])

const responsiblesError = ref<string | null>(null)

let nextResponsibleRowId = 1

const systemUsers = computed(() => usersQuery.data.value ?? [])
const responsiblesRepeaterError = computed(
  () =>
    responsiblesError.value ??
    (usersQuery.error.value
      ? getApiErrorMessage(usersQuery.error.value)
      : unitResponsiblesQuery.error.value
        ? getApiErrorMessage(unitResponsiblesQuery.error.value)
        : null),
)

function createResponsibleRow(params?: {
  userId?: number | null
  level?: UnitResponsibleLevel
}): UnitResponsibleDraftRow {
  return {
    key: `unit-responsible-${Date.now()}-${nextResponsibleRowId++}`,
    userId: params?.userId ?? null,
    level: params?.level ?? 'View',
  }
}

watch(
  () => unitQuery.data.value,
  (unit) => {
    if (!unit) {
      return
    }

    unitName.value = unit.name
  },
  {immediate: true},
)

watch(
  () => unitResponsiblesQuery.data.value,
  (responsibles) => {
    const items = responsibles ?? []
    responsibleRows.value = items.map((user) =>
      createResponsibleRow({
        userId: user.id,
        level: user.level,
      }),
    )
  },
  {immediate: true},
)

async function saveUnit(): Promise<void> {
  if (unitId.value === null) {
    showErrorToast('Invalid unit ID.')
    return
  }

  try {
    await updateUnitMutation.mutateAsync({
      id: unitId.value,
      payload: {name: unitName.value.trim()},
    })
    showSuccessToast('Unit updated successfully.')
  } catch (error: unknown) {
    showErrorToast(getApiErrorMessage(error))
  }
}

function normalizeResponsibles():
  | Array<{user_id: number; level: UnitResponsibleLevel}>
  | null {
  const seenUserIds = new Set<number>()
  const assignments: Array<{user_id: number; level: UnitResponsibleLevel}> = []

  for (const row of responsibleRows.value) {
    if (row.userId === null) {
      responsiblesError.value =
        'Select a user in each responsible row or remove the empty row.'
      return null
    }

    if (seenUserIds.has(row.userId)) {
      responsiblesError.value = 'Each user can be assigned only once.'
      return null
    }

    seenUserIds.add(row.userId)
    assignments.push({
      user_id: row.userId,
      level: row.level,
    })
  }

  return assignments
}

async function saveResponsibles(): Promise<void> {
  responsiblesError.value = null

  if (unitId.value === null) {
    showErrorToast('Invalid unit ID.')
    return
  }

  const assignments = normalizeResponsibles()
  if (assignments === null) {
    return
  }

  try {
    await replaceUnitResponsiblesMutation.mutateAsync({
      unitId: unitId.value,
      payload: {
        assignments,
      },
    })

    showSuccessToast('Unit responsibles updated successfully.')
  } catch (error: unknown) {
    showErrorToast(getApiErrorMessage(error))
  }
}
</script>

<template>
  <section class="settings-unit-edit-page">
    <p class="settings-unit-edit-page__text-muted">
      Update unit name and manage responsible users.
    </p>

    <p v-if="unitId === null" class="settings-unit-edit-page__error">Invalid unit ID.</p>
    <p v-else-if="unitQuery.error.value" class="settings-unit-edit-page__error">
      {{ getApiErrorMessage(unitQuery.error.value) }}
    </p>
    <p v-else-if="unitQuery.isLoading.value" class="settings-unit-edit-page__text-muted">
      Loading unit...
    </p>

    <template v-else-if="unitQuery.data.value">
      <div class="settings-unit-edit-page__grid">
        <div class="settings-unit-edit-page__card settings-unit-edit-page__card--left">
          <form class="settings-unit-edit-page__form" @submit.prevent="saveUnit">
            <UiFormField
              id="settings-unit-edit-name"
              label="Unit name"
              :model-value="unitName"
              required
              @update:model-value="unitName = $event"
            />

            <UiButton
              type="submit"
              tone="success"
              :disabled="updateUnitMutation.isPending.value"
            >
              <template #icon>
                <Save :size="16" />
              </template>
              {{ updateUnitMutation.isPending.value ? 'Saving...' : 'Save unit' }}
            </UiButton>
          </form>
        </div>

        <div class="settings-unit-edit-page__card settings-unit-edit-page__card--right">
          <UnitResponsiblesRepeater
            v-model="responsibleRows"
            :users="systemUsers"
            :loading="usersQuery.isLoading.value || unitResponsiblesQuery.isLoading.value"
            :disabled="
              replaceUnitResponsiblesMutation.isPending.value ||
              usersQuery.isLoading.value ||
              unitResponsiblesQuery.isLoading.value
            "
            :error-message="responsiblesRepeaterError"
            description="Saved via separate endpoint for user-unit bindings."
          />

          <UiButton
            v-if="responsibleRows.length === 0"
            type="button"
            size="sm"
            variant="ghost"
            tone="success"
            :disabled="usersQuery.isLoading.value || unitResponsiblesQuery.isLoading.value"
            @click="responsibleRows = [createResponsibleRow()]"
          >
            <template #icon>
              <Plus :size="16" />
            </template>
            Add first responsible
          </UiButton>

          <UiButton
            type="button"
            tone="success"
            :disabled="
              replaceUnitResponsiblesMutation.isPending.value ||
              usersQuery.isLoading.value ||
              unitResponsiblesQuery.isLoading.value
            "
            @click="saveResponsibles"
          >
            <template #icon>
              <Save :size="16" />
            </template>
            {{
              replaceUnitResponsiblesMutation.isPending.value
                ? 'Saving responsibles...'
                : 'Save responsibles'
            }}
          </UiButton>
        </div>
      </div>
    </template>
  </section>
</template>

<style scoped lang="scss">
.settings-unit-edit-page {
  display: grid;
  gap: var(--space-4);

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
    display: grid;
    gap: var(--space-3);
  }

  &__grid {
    display: grid;
    grid-template-columns: minmax(0, 0.95fr) minmax(0, 1.25fr);
    gap: var(--space-4);
    align-items: start;
  }

  &__card--left {
    align-self: start;
  }

  &__card--right {
    align-self: start;
  }

  &__form {
    display: grid;
    gap: var(--space-3);
    max-width: 520px;
  }

  &__error {
    margin: 0;
    color: var(--color-danger);
    font-size: 0.875rem;
  }

}

@media (max-width: 900px) {
  .settings-unit-edit-page {
    &__grid {
      grid-template-columns: 1fr;
    }
  }
}
</style>
