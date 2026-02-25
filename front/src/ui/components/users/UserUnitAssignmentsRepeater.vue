<script setup lang="ts">
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

let nextRowId = 1

function updateRows(nextRows: AssignmentRow[]): void {
  emit('update:modelValue', nextRows)
}

function addRow(): void {
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
        :disabled="disabled"
        @click="addRow"
      >
        Add unit
      </UiButton>
    </div>

    <p v-if="errorMessage" class="user-unit-repeater__error">{{ errorMessage }}</p>
    <p v-else-if="loading" class="user-unit-repeater__state">Loading units...</p>

    <div v-if="modelValue.length === 0" class="user-unit-repeater__empty">
      No unit bindings yet.
    </div>

    <div v-else class="user-unit-repeater__rows">
      <div
        v-for="row in modelValue"
        :key="row.key"
        class="user-unit-repeater__row"
      >
        <label class="user-unit-repeater__field">
          <span class="user-unit-repeater__label">Unit</span>
          <select
            class="user-unit-repeater__select"
            :disabled="disabled || loading"
            :value="row.unitId === null ? '' : String(row.unitId)"
            @change="onUnitChange(row.key, $event)"
          >
            <option value="">Select unit</option>
            <option v-for="unit in units" :key="unit.id" :value="unit.id">
              {{ unit.name }}
            </option>
          </select>
        </label>

        <label class="user-unit-repeater__field user-unit-repeater__field--level">
          <span class="user-unit-repeater__label">Level</span>
          <select
            class="user-unit-repeater__select"
            :disabled="disabled"
            :value="row.level"
            @change="onLevelChange(row.key, $event)"
          >
            <option v-for="level in levelOptions" :key="level" :value="level">
              {{ level }}
            </option>
          </select>
        </label>

        <UiButton
          type="button"
          size="sm"
          variant="ghost"
          :disabled="disabled"
          class="user-unit-repeater__remove"
          @click="removeRow(row.key)"
        >
          Remove
        </UiButton>
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

  &__row {
    display: grid;
    grid-template-columns: minmax(0, 1fr) 140px auto;
    gap: var(--space-2);
    align-items: end;
    padding: var(--space-2);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    background: var(--color-surface-soft);
  }

  &__field {
    display: grid;
    gap: 6px;
    min-width: 0;
  }

  &__field--level {
    min-width: 120px;
  }

  &__label {
    color: var(--color-text-muted);
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
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
