<script setup lang="ts">
import {Plus, Trash2} from 'lucide-vue-next'
import type {UnitResponsibleLevel} from '@/domain/units/model'
import UiButton from '@/ui/components/common/UiButton.vue'

type UserOption = {
  id: number
  full_name: string
  email: string
}

export type UnitResponsibleDraftRow = {
  key: string
  userId: number | null
  level: UnitResponsibleLevel
}

const props = withDefaults(
  defineProps<{
    modelValue: UnitResponsibleDraftRow[]
    users: UserOption[]
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
    title: 'Unit responsibles',
    description: 'Bind users to this unit and set access level.',
  },
)

const emit = defineEmits<{
  (event: 'update:modelValue', value: UnitResponsibleDraftRow[]): void
}>()

const levelOptions: readonly UnitResponsibleLevel[] = ['View', 'Edit', 'Full']
let nextRowId = 1

function updateRows(rows: UnitResponsibleDraftRow[]): void {
  emit('update:modelValue', rows)
}

function addRow(): void {
  updateRows([
    ...props.modelValue,
    {
      key: `unit-resp-${Date.now()}-${nextRowId++}`,
      userId: null,
      level: 'View',
    },
  ])
}

function removeRow(key: string): void {
  updateRows(props.modelValue.filter((row) => row.key !== key))
}

function updateRowUser(key: string, userId: number | null): void {
  updateRows(
    props.modelValue.map((row) => (row.key === key ? {...row, userId} : row)),
  )
}

function updateRowLevel(key: string, level: UnitResponsibleLevel): void {
  updateRows(
    props.modelValue.map((row) => (row.key === key ? {...row, level} : row)),
  )
}

function onUserChange(key: string, event: Event): void {
  const target = event.target
  if (!(target instanceof HTMLSelectElement)) {
    return
  }

  const value = target.value.trim()
  if (!value) {
    updateRowUser(key, null)
    return
  }

  const parsed = Number.parseInt(value, 10)
  if (!Number.isInteger(parsed) || parsed <= 0) {
    return
  }

  updateRowUser(key, parsed)
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
  <section class="unit-responsibles-repeater">
    <div class="unit-responsibles-repeater__head">
      <div>
        <h3 class="unit-responsibles-repeater__title">{{ title }}</h3>
        <p class="unit-responsibles-repeater__description">{{ description }}</p>
      </div>

      <UiButton
        type="button"
        size="sm"
        variant="ghost"
        tone="success"
        :disabled="disabled"
        @click="addRow"
      >
        <template #icon>
          <Plus :size="16" />
        </template>
        Add responsible
      </UiButton>
    </div>

    <p v-if="errorMessage" class="unit-responsibles-repeater__error">{{ errorMessage }}</p>
    <p v-else-if="loading" class="unit-responsibles-repeater__state">Loading users...</p>

    <div v-if="modelValue.length === 0" class="unit-responsibles-repeater__empty">
      No responsibles yet.
    </div>

    <div v-else class="unit-responsibles-repeater__rows">
      <div v-for="row in modelValue" :key="row.key" class="unit-responsibles-repeater__row">
        <label class="unit-responsibles-repeater__field">
          <span class="unit-responsibles-repeater__label">User</span>
          <select
            class="unit-responsibles-repeater__select"
            :disabled="disabled || loading"
            :value="row.userId === null ? '' : String(row.userId)"
            @change="onUserChange(row.key, $event)"
          >
            <option value="">Select user</option>
            <option v-for="user in users" :key="user.id" :value="user.id">
              {{ user.full_name }} ({{ user.email }})
            </option>
          </select>
        </label>

        <label class="unit-responsibles-repeater__field unit-responsibles-repeater__field--level">
          <span class="unit-responsibles-repeater__label">Level</span>
          <select
            class="unit-responsibles-repeater__select"
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
          tone="danger"
          :disabled="disabled"
          @click="removeRow(row.key)"
        >
          <template #icon>
            <Trash2 :size="16" />
          </template>
          Remove
        </UiButton>
      </div>
    </div>
  </section>
</template>

<style scoped lang="scss">
.unit-responsibles-repeater {
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
}

@media (max-width: 900px) {
  .unit-responsibles-repeater {
    &__row {
      grid-template-columns: 1fr;
      align-items: stretch;
    }
  }
}
</style>
