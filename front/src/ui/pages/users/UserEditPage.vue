<script setup lang="ts">
import {computed, ref, watch} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import type {UnitResponsibleLevel} from '@/domain/units/model'
import {useUnitsQuery} from '@/domain/units/queries'
import {
  useReplaceUserUnitAssignmentsMutation,
  useSystemUsersQuery,
  useUpdateSystemUserMutation,
  useUserUnitAssignmentsQuery,
} from '@/domain/users/queries'
import {getApiErrorMessage} from '@/shared/http/errors'
import UiButton from '@/ui/components/common/UiButton.vue'
import UiEntityPageLayout from '@/ui/layout/UiEntityPageLayout.vue'
import UiFormField from '@/ui/components/common/UiFormField.vue'
import UserUnitAssignmentsRepeater from '@/ui/components/users/UserUnitAssignmentsRepeater.vue'

type UserUnitAssignmentDraftRow = {
  key: string
  unitId: number | null
  level: UnitResponsibleLevel
}

const route = useRoute()
const router = useRouter()

const usersQuery = useSystemUsersQuery()
const unitsQuery = useUnitsQuery()
const updateUserMutation = useUpdateSystemUserMutation()
const replaceUserUnitAssignmentsMutation = useReplaceUserUnitAssignmentsMutation()

const fullName = ref('')
const password = ref('')
const isActive = ref(true)
const errorMessage = ref<string | null>(null)
const unitAssignmentsError = ref<string | null>(null)
const successMessage = ref<string | null>(null)
const initializedUserId = ref<number | null>(null)
const initializedAssignmentsUserId = ref<number | null>(null)
const unitAssignmentRows = ref<UserUnitAssignmentDraftRow[]>([])

let nextAssignmentRowId = 1

const userId = computed<number | null>(() => {
  const rawId = route.params.id
  const value = Array.isArray(rawId) ? rawId[0] : rawId

  if (!value) {
    return null
  }

  const parsed = Number.parseInt(value, 10)
  return Number.isInteger(parsed) && parsed > 0 ? parsed : null
})

const users = computed(() => usersQuery.data.value ?? [])
const availableUnits = computed(() => unitsQuery.data.value ?? [])
const userUnitAssignmentsQuery = useUserUnitAssignmentsQuery(userId)
const unitAssignmentsRepeaterError = computed(
  () =>
    unitAssignmentsError.value ??
    (unitsQuery.error.value
      ? getApiErrorMessage(unitsQuery.error.value)
      : userUnitAssignmentsQuery.error.value
        ? getApiErrorMessage(userUnitAssignmentsQuery.error.value)
        : null),
)

const selectedUser = computed(() =>
  userId.value === null
    ? null
    : users.value.find((user) => user.id === userId.value) ?? null,
)

const breadcrumbs = computed(() => {
  const currentLabel = selectedUser.value
    ? `Edit: ${selectedUser.value.email} (ID: ${selectedUser.value.id})`
    : 'Edit'

  return [
    {label: 'Users', to: {name: 'users'}},
    {label: currentLabel},
  ]
})

function createDraftRow(params?: {
  unitId?: number | null
  level?: UnitResponsibleLevel
}): UserUnitAssignmentDraftRow {
  return {
    key: `user-unit-${Date.now()}-${nextAssignmentRowId++}`,
    unitId: params?.unitId ?? null,
    level: params?.level ?? 'View',
  }
}

watch(
  () => selectedUser.value?.id ?? null,
  (nextId) => {
    if (nextId === null || selectedUser.value === null) {
      return
    }

    if (initializedUserId.value === nextId) {
      return
    }

    fullName.value = selectedUser.value.full_name
    isActive.value = selectedUser.value.is_active
    password.value = ''
    errorMessage.value = null
    successMessage.value = null
    initializedUserId.value = nextId
  },
  {immediate: true},
)

watch(
  [() => userId.value, () => userUnitAssignmentsQuery.data.value],
  ([nextUserId, assignments]) => {
    if (nextUserId === null || !assignments) {
      return
    }

    if (initializedAssignmentsUserId.value === nextUserId) {
      return
    }

    unitAssignmentRows.value = assignments.map((assignment) =>
      createDraftRow({
        unitId: assignment.unit_id,
        level: assignment.level,
      }),
    )
    initializedAssignmentsUserId.value = nextUserId
  },
  {immediate: true},
)

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

async function submitEdit(): Promise<void> {
  errorMessage.value = null
  unitAssignmentsError.value = null
  successMessage.value = null

  if (userId.value === null || selectedUser.value === null) {
    errorMessage.value = 'User not found.'
    return
  }

  const normalizedAssignments = normalizeUnitAssignments()
  if (normalizedAssignments === null) {
    return
  }

  const payload: {full_name: string; is_active: boolean; password?: string} = {
    full_name: fullName.value.trim(),
    is_active: isActive.value,
  }

  if (password.value.length > 0) {
    payload.password = password.value
  }

  try {
    await updateUserMutation.mutateAsync({
      id: userId.value,
      payload,
    })

    await replaceUserUnitAssignmentsMutation.mutateAsync({
      userId: userId.value,
      payload: {
        assignments: normalizedAssignments,
      },
    })

    successMessage.value = 'User updated successfully.'
  } catch (error: unknown) {
    errorMessage.value = getApiErrorMessage(error)
  }
}

function goBack(): void {
  void router.push({name: 'users'})
}
</script>

<template>
  <UiEntityPageLayout
    class="user-form-page"
    title="Edit user"
    description="Update profile data, status, password, and unit bindings for a system user."
    :breadcrumbs="breadcrumbs"
  >
    <template #meta>
      <p v-if="selectedUser" class="user-form-page__meta">
        {{ selectedUser.email }} (ID: {{ selectedUser.id }})
      </p>
      <p v-else class="user-form-page__meta">Update system user details.</p>
    </template>

    <template #actions>
      <UiButton variant="ghost" @click="goBack">Back to list</UiButton>
    </template>

    <p v-if="successMessage" class="user-form-page__success">{{ successMessage }}</p>
    <p v-if="errorMessage" class="user-form-page__error">{{ errorMessage }}</p>
    <p v-else-if="usersQuery.error.value" class="user-form-page__error">
      {{ getApiErrorMessage(usersQuery.error.value) }}
    </p>

    <p v-if="userId === null" class="user-form-page__state">Invalid user ID.</p>
    <p v-else-if="usersQuery.isLoading.value" class="user-form-page__state">
      Loading user...
    </p>
    <p v-else-if="!selectedUser" class="user-form-page__state">
      User not found.
    </p>

    <div v-else class="user-form-page__grid">
      <form class="user-form-page__form-card" @submit.prevent="submitEdit">
        <div class="user-form-page__form">
          <UiFormField
            id="user-edit-email"
            label="Email"
            :model-value="selectedUser.email"
            readonly
          />
          <UiFormField
            id="user-edit-name"
            label="Name"
            autocomplete="name"
            required
            :model-value="fullName"
            @update:model-value="fullName = $event"
          />
          <UiFormField
            id="user-edit-password"
            label="New password (optional)"
            type="password"
            autocomplete="new-password"
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
            :disabled="
              updateUserMutation.isPending.value ||
              replaceUserUnitAssignmentsMutation.isPending.value
            "
          >
            {{
              updateUserMutation.isPending.value ||
              replaceUserUnitAssignmentsMutation.isPending.value
                ? 'Saving...'
                : 'Save changes'
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
            updateUserMutation.isPending.value ||
            replaceUserUnitAssignmentsMutation.isPending.value ||
            userUnitAssignmentsQuery.isLoading.value
          "
          :error-message="unitAssignmentsRepeaterError"
          title="Unit bindings"
          description="Manage user access to units using the repeater."
        />

        <UiButton
          v-if="unitAssignmentRows.length === 0"
          type="button"
          size="sm"
          variant="ghost"
          :disabled="userUnitAssignmentsQuery.isLoading.value"
          @click="unitAssignmentRows = [createDraftRow()]"
        >
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

  &__success {
    color: var(--color-success);
    font-size: 0.875rem;
    margin: 0;
  }

  &__state {
    color: var(--color-text-muted);
    margin: 0;
  }

  &__meta {
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
