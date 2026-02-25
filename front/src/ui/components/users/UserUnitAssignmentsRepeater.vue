<script setup lang="ts">
import {computed} from 'vue'
import {Plus, Trash2} from 'lucide-vue-next'
import type {UnitResponsibleLevel} from '@/domain/units/model'
import UiButton from '@/ui/components/common/UiButton.vue'

type UnitOption = {
  id: number
  name: string
}

type AssignmentRow = {
  key: string
  unitId: number | null
  level: UnitResponsibleLevel
}

const props = withDefaults(
  defineProps<{
    modelValue: AssignmentRow[]
    units: UnitOption[]
    disabled?: boolean
    loading?: boolean
    errorMessage?: string | null
    title?: string
    description?: string
  }>(),
  {
    disabled: false,
    loading: false,
    errorMessage: null,
    title: 'Unit assignments',
    description: 'Bind user to units and set access level for each binding.',
  },
)

const emit = defineEmits<{
  (event: 'update:modelValue', value: AssignmentRow[]): void
}>()

const levelOptions: readonly UnitResponsibleLevel[] = ['View', 'Edit', 'Full']
const selectedUnitIds = computed(() =>
  props.modelValue
    .map((row) => row.unitId)
    .filter((unitId): unitId is number => unitId !== null),
)
const canAddRow = computed(
  () => selectedUnitIds.value.length < props.units.length,
)

let nextRowId = 1

function updateRows(nextRows: AssignmentRow[]): void {
  emit('update:modelValue', nextRows)
}

function addRow(): void {
  if (!canAddRow.value) {
    return
  }

  updateRows([
    ...props.modelValue,
    {
      key: `row-${Date.now()}-${nextRowId++}`,
      unitId: null,
      level: 'View',
    },
  ])
}

function removeRow(key: string): void {
  updateRows(props.modelValue.filter((row) => row.key !== key))
}

function updateRowUnit(key: string, unitId: number | null): void {
  if (unitId !== null && isUnitSelectedInAnotherRow(key, unitId)) {
    return
  }

  updateRows(
    props.modelValue.map((row) =>
      row.key === key
        ? {
            ...row,
            unitId,
          }
        : row,
    ),
  )
}

function isUnitSelectedInAnotherRow(key: string, unitId: number): boolean {
  return props.modelValue.some((row) => row.key !== key && row.unitId === unitId)
}

function updateRowLevel(key: string, level: UnitResponsibleLevel): void {
  updateRows(
    props.modelValue.map((row) =>
      row.key === key
        ? {
            ...row,
            level,
          }
        : row,
    ),
  )
}

function onUnitChange(key: string, event: Event): void {
  const target = event.target
  if (!(target instanceof HTMLSelectElement)) {
    return
  }

  const value = target.value.trim()
  if (!value) {
    updateRowUnit(key, null)
    return
  }

  const parsed = Number.parseInt(value, 10)
  if (!Number.isInteger(parsed) || parsed <= 0) {
    return
  }

  updateRowUnit(key, parsed)
}

function isLevel(value: string): value is UnitResponsibleLevel {
  return value === 'View' || value === 'Edit' || value === 'Full'
}

function onLevelChange(key: string, event: Event): void {
  const target = event.target
  if (!(target instanceof HTMLSelectElement)) {
    return
  }

  if (!isLevel(target.value)) {
    return
  }

  updateRowLevel(key, target.value)
}
</script>

<template>
  <section class="user-unit-repeater">
    <div class="user-unit-repeater__head">
      <div>
        <h3 class="user-unit-repeater__title">{{ title }}</h3>
        <p class="user-unit-repeater__description">{{ description }}</p>
      </div>

      <UiButton
        type="button"
        size="sm"
        variant="ghost"
        tone="success"
        :disabled="disabled || loading || !canAddRow"
        @click="addRow"
      >
        <template #icon>
          <Plus :size="16" />
        </template>
        Add unit
      </UiButton>
    </div>

    <p v-if="errorMessage" class="user-unit-repeater__error">{{ errorMessage }}</p>
    <p v-else-if="loading" class="user-unit-repeater__state">Loading units...</p>

    <div v-if="modelValue.length === 0" class="user-unit-repeater__empty">
      No unit bindings yet.
    </div>

    <div v-else class="user-unit-repeater__table">
      <div class="user-unit-repeater__columns" aria-hidden="true">
        <span class="user-unit-repeater__column-title">Unit</span>
        <span class="user-unit-repeater__column-title">Level</span>
        <span class="user-unit-repeater__column-title user-unit-repeater__column-title--actions" />
      </div>

      <div class="user-unit-repeater__rows">
      <div
        v-for="row in modelValue"
        :key="row.key"
        class="user-unit-repeater__row"
      >
        <div class="user-unit-repeater__field">
          <select
            class="user-unit-repeater__select"
            aria-label="Unit"
            :disabled="disabled || loading"
            :value="row.unitId === null ? '' : String(row.unitId)"
            @change="onUnitChange(row.key, $event)"
          >
            <option value="">Select unit</option>
            <option
              v-for="unit in units"
              :key="unit.id"
              :value="unit.id"
              :disabled="row.unitId !== unit.id && isUnitSelectedInAnotherRow(row.key, unit.id)"
            >
              {{ unit.name }}
            </option>
          </select>
        </div>

        <div class="user-unit-repeater__field user-unit-repeater__field--level">
          <select
            class="user-unit-repeater__select"
            aria-label="Level"
            :disabled="disabled"
            :value="row.level"
            @change="onLevelChange(row.key, $event)"
          >
            <option v-for="level in levelOptions" :key="level" :value="level">
              {{ level }}
            </option>
          </select>
        </div>

        <UiButton
          type="button"
          size="md"
          variant="ghost"
          tone="danger"
          icon-only
          aria-label="Remove unit binding"
          :disabled="disabled"
          class="user-unit-repeater__remove"
          @click="removeRow(row.key)"
        >
          <template #icon>
            <Trash2 :size="16" />
          </template>
        </UiButton>
      </div>
      </div>
    </div>
  </section>
</template>

<style scoped lang="scss">
.user-unit-repeater {
  display: grid;
  gap: var(--space-3);

  &__head {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: var(--space-3);
  }

  &__title {
    margin: 0;
    font-size: 1rem;
  }

  &__description {
    margin: var(--space-1) 0 0;
    color: var(--color-text-muted);
    font-size: 0.875rem;
  }

  &__error {
    margin: 0;
    color: var(--color-danger);
    font-size: 0.875rem;
  }

  &__state,
  &__empty {
    margin: 0;
    color: var(--color-text-muted);
    font-size: 0.875rem;
  }

  &__rows {
    display: grid;
    gap: var(--space-2);
  }

  &__table {
    display: grid;
    gap: var(--space-2);
  }

  &__columns {
    display: grid;
    grid-template-columns: minmax(0, 1fr) 140px auto;
    gap: var(--space-2);
    align-items: center;
    padding: 0 var(--space-2);
  }

  &__column-title {
    color: var(--color-text-muted);
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    font-weight: 600;
  }

  &__column-title--actions {
    width: 36px;
  }

  &__row {
    display: grid;
    grid-template-columns: minmax(0, 1fr) 140px auto;
    gap: var(--space-2);
    align-items: end;
    padding: var(--space-2);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
  }

  &__field {
    display: grid;
    gap: 6px;
    min-width: 0;
  }

  &__field--level {
    min-width: 120px;
  }

  &__select {
    min-height: 36px;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    background: var(--color-surface);
    color: var(--color-text);
    padding: 0 var(--space-2);
  }

  &__remove {
    align-self: end;
  }
}

@media (max-width: 900px) {
  .user-unit-repeater {
    &__columns {
      display: none;
    }

    &__row {
      grid-template-columns: 1fr;
      align-items: stretch;
    }

    &__remove {
      justify-self: start;
    }
  }
}
</style>
