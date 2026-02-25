<script setup lang="ts">
import {computed, ref} from 'vue'
import {CornerUpLeft, Plus} from 'lucide-vue-next'
import type {UnitResponsibleLevel} from '@/domain/units/model'
import {useUnitsQuery} from '@/domain/units/queries'
import {
  useCreateSystemUserMutation,
  useReplaceUserUnitAssignmentsMutation,
} from '@/domain/users/queries'
import {getApiErrorMessage} from '@/shared/http/errors'
import {showErrorToast, showSuccessToast} from '@/shared/ui/toast'
import UiButton from '@/ui/components/common/UiButton.vue'
import UiFormField from '@/ui/components/common/UiFormField.vue'
import UserUnitAssignmentsRepeater from '@/ui/components/users/UserUnitAssignmentsRepeater.vue'
import UiEntityPageLayout from '@/ui/layout/UiEntityPageLayout.vue'
import {useRouter} from 'vue-router'

type UserUnitAssignmentDraftRow = {
  key: string
  unitId: number | null
  level: UnitResponsibleLevel
}

const router = useRouter()
const createUserMutation = useCreateSystemUserMutation()
const replaceUserUnitAssignmentsMutation = useReplaceUserUnitAssignmentsMutation()
const unitsQuery = useUnitsQuery()

const email = ref('')
const fullName = ref('')
const password = ref('')
const isActive = ref(true)
const unitAssignmentsError = ref<string | null>(null)
const unitAssignmentRows = ref<UserUnitAssignmentDraftRow[]>([])

let nextAssignmentRowId = 1

const availableUnits = computed(() => unitsQuery.data.value ?? [])
const unitAssignmentsRepeaterError = computed(
  () =>
    unitAssignmentsError.value ??
    (unitsQuery.error.value ? getApiErrorMessage(unitsQuery.error.value) : null),
)

function createDraftRow(): UserUnitAssignmentDraftRow {
  return {
    key: `user-unit-${Date.now()}-${nextAssignmentRowId++}`,
    unitId: null,
    level: 'View',
  }
}

function normalizeUnitAssignments(): Array<{unit_id: number; level: UnitResponsibleLevel}> | null {
  const result: Array<{unit_id: number; level: UnitResponsibleLevel}> = []
  const seenUnitIds = new Set<number>()

  for (const row of unitAssignmentRows.value) {
    if (row.unitId === null) {
      unitAssignmentsError.value = 'Select a unit in each assignment row or remove the empty row.'
      return null
    }

    if (seenUnitIds.has(row.unitId)) {
      unitAssignmentsError.value = 'Each unit can be assigned only once.'
      return null
    }

    seenUnitIds.add(row.unitId)
    result.push({
      unit_id: row.unitId,
      level: row.level,
    })
  }

  return result
}

async function submitCreate(): Promise<void> {
  unitAssignmentsError.value = null

  const normalizedAssignments = normalizeUnitAssignments()
  if (normalizedAssignments === null) {
    return
  }

  try {
    const createdUser = await createUserMutation.mutateAsync({
      email: email.value.trim(),
      full_name: fullName.value.trim(),
      password: password.value,
      is_active: isActive.value,
      settings: {},
    })

    if (normalizedAssignments.length > 0) {
      await replaceUserUnitAssignmentsMutation.mutateAsync({
        userId: createdUser.id,
        payload: {
          assignments: normalizedAssignments,
        },
      })
    }

    showSuccessToast('User created successfully.')
    void router.push({name: 'users'})
  } catch (error: unknown) {
    showErrorToast(getApiErrorMessage(error))
  }
}

function goBack(): void {
  void router.push({name: 'users'})
}
</script>

<template>
  <UiEntityPageLayout
    class="user-form-page"
    title="Create user"
    description="Create a new system user account and set initial access parameters."
    :breadcrumbs="[
      {label: 'Users', to: {name: 'users'}},
      {label: 'Create'},
    ]"
  >
    <template #actions>
      <UiButton variant="ghost" @click="goBack">
        <template #icon>
          <CornerUpLeft :size="16" />
        </template>
        Back to list
      </UiButton>
    </template>

    <div class="user-form-page__grid">
      <form class="user-form-page__form-card" @submit.prevent="submitCreate">
        <div class="user-form-page__form">
          <UiFormField
            id="user-create-email"
            label="Email"
            type="email"
            autocomplete="email"
            required
            :model-value="email"
            @update:model-value="email = $event"
          />
          <UiFormField
            id="user-create-name"
            label="Name"
            autocomplete="name"
            required
            :model-value="fullName"
            @update:model-value="fullName = $event"
          />
          <UiFormField
            id="user-create-password"
            label="Password"
            type="password"
            autocomplete="new-password"
            required
            :model-value="password"
            @update:model-value="password = $event"
          />

          <label class="user-form-page__checkbox">
            <input v-model="isActive" type="checkbox" />
            Active user
          </label>
        </div>

        <div class="user-form-page__actions">
          <UiButton type="button" variant="ghost" @click="goBack">Cancel</UiButton>
          <UiButton
            type="submit"
            tone="success"
            :disabled="
              createUserMutation.isPending.value ||
              replaceUserUnitAssignmentsMutation.isPending.value
            "
          >
            <template #icon>
              <Plus :size="16" />
            </template>
            {{
              createUserMutation.isPending.value ||
              replaceUserUnitAssignmentsMutation.isPending.value
                ? 'Creating...'
                : 'Create user'
            }}
          </UiButton>
        </div>
      </form>

      <aside class="user-form-page__side-card">
        <UserUnitAssignmentsRepeater
          v-model="unitAssignmentRows"
          :units="availableUnits"
          :loading="unitsQuery.isLoading.value"
          :disabled="
            createUserMutation.isPending.value ||
            replaceUserUnitAssignmentsMutation.isPending.value
          "
          :error-message="unitAssignmentsRepeaterError"
          title="Unit bindings"
          description="Optional. Add unit access bindings for the new user."
        />

        <UiButton
          v-if="unitAssignmentRows.length === 0"
          type="button"
          size="sm"
          variant="ghost"
          tone="success"
          @click="unitAssignmentRows = [createDraftRow()]"
        >
          <template #icon>
            <Plus :size="16" />
          </template>
          Add first binding
        </UiButton>
      </aside>
    </div>
  </UiEntityPageLayout>
</template>

<style scoped lang="scss">
.user-form-page {
  display: grid;
  gap: var(--space-4);

  &__grid {
    display: grid;
    grid-template-columns: minmax(0, 1.2fr) minmax(0, 1fr);
    gap: var(--space-4);
    align-items: start;
  }

  &__form-card,
  &__side-card {
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    background: var(--color-surface);
    box-shadow: var(--card-shadow);
    padding: var(--space-4);
  }

  &__form-card {
    display: grid;
    gap: var(--space-4);
  }

  &__side-card {
    display: grid;
    gap: var(--space-3);
  }

  &__form {
    display: grid;
    gap: var(--space-3);
  }

  &__checkbox {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
  }

  &__actions {
    display: inline-flex;
    gap: var(--space-2);
    align-items: center;
    flex-wrap: wrap;
  }

  &__error {
    color: var(--color-danger);
    font-size: 0.875rem;
    margin: 0;
  }
}

@media (max-width: 980px) {
  .user-form-page {
    &__grid {
      grid-template-columns: 1fr;
    }
  }
}
</style>
