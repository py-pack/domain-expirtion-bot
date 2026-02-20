<script setup lang="ts">
import {computed, ref} from 'vue'
import {useMutation, useQuery, useQueryClient} from '@tanstack/vue-query'
import {usersService} from '@/domain/users/service'
import {getApiErrorMessage} from '@/shared/http/errors'
import UiButton from '@/ui/components/common/UiButton.vue'
import UiFormField from '@/ui/components/common/UiFormField.vue'
import UiTable from '@/ui/components/common/UiTable.vue'

const queryClient = useQueryClient()

const usersQuery = useQuery({
  queryKey: ['users', 'list'],
  queryFn: async () => usersService.getSystemUsers(),
  staleTime: 30_000,
})

const createUserMutation = useMutation({
  mutationFn: async (payload: {
    email: string
    full_name: string
    password: string
    is_active: boolean
    settings: Record<string, unknown>
  }) => usersService.createSystemUser(payload),
  onSuccess: async () => {
    await queryClient.invalidateQueries({queryKey: ['users', 'list']})
  },
})

const updateUserMutation = useMutation({
  mutationFn: async (params: {
    id: number
    payload: {full_name: string; is_active: boolean; password?: string}
  }) => usersService.updateSystemUser(params.id, params.payload),
  onSuccess: async () => {
    await queryClient.invalidateQueries({queryKey: ['users', 'list']})
  },
})

const deleteUserMutation = useMutation({
  mutationFn: async (id: number) => usersService.deleteSystemUser(id),
  onSuccess: async () => {
    await queryClient.invalidateQueries({queryKey: ['users', 'list']})
  },
})

const createEmail = ref('')
const createName = ref('')
const createPassword = ref('')

const editingUserId = ref<number | null>(null)
const editName = ref('')
const editPassword = ref('')
const editIsActive = ref(true)

const errorMessage = ref<string | null>(null)

const users = computed(() => usersQuery.data.value ?? [])

function startEdit(userId: number): void {
  const user = users.value.find((item) => item.id === userId)
  if (!user) {
    return
  }

  editingUserId.value = user.id
  editName.value = user.full_name
  editPassword.value = ''
  editIsActive.value = user.is_active
}

function cancelEdit(): void {
  editingUserId.value = null
  editName.value = ''
  editPassword.value = ''
  editIsActive.value = true
}

async function submitCreate(): Promise<void> {
  errorMessage.value = null

  try {
    await createUserMutation.mutateAsync({
      email: createEmail.value.trim(),
      full_name: createName.value.trim(),
      password: createPassword.value,
      is_active: true,
      settings: {},
    })

    createEmail.value = ''
    createName.value = ''
    createPassword.value = ''
  } catch (error: unknown) {
    errorMessage.value = getApiErrorMessage(error)
  }
}

async function submitEdit(userId: number): Promise<void> {
  errorMessage.value = null

  const payload: {full_name: string; is_active: boolean; password?: string} = {
    full_name: editName.value.trim(),
    is_active: editIsActive.value,
  }

  if (editPassword.value.length > 0) {
    payload.password = editPassword.value
  }

  try {
    await updateUserMutation.mutateAsync({
      id: userId,
      payload,
    })
    cancelEdit()
  } catch (error: unknown) {
    errorMessage.value = getApiErrorMessage(error)
  }
}

async function removeUser(userId: number): Promise<void> {
  errorMessage.value = null

  try {
    await deleteUserMutation.mutateAsync(userId)
  } catch (error: unknown) {
    errorMessage.value = getApiErrorMessage(error)
  }
}
</script>

<template>
  <section class="page-card users-page">
    <h1 class="page-title">Users</h1>
    <p class="page-subtitle">Manage system users.</p>

    <form class="users-page__create" @submit.prevent="submitCreate">
      <UiFormField
        id="user-create-email"
        label="Email"
        type="email"
        autocomplete="email"
        required
        :model-value="createEmail"
        @update:model-value="createEmail = $event"
      />
      <UiFormField
        id="user-create-name"
        label="Name"
        autocomplete="name"
        required
        :model-value="createName"
        @update:model-value="createName = $event"
      />
      <UiFormField
        id="user-create-password"
        label="Password"
        type="password"
        autocomplete="new-password"
        required
        :model-value="createPassword"
        @update:model-value="createPassword = $event"
      />
      <UiButton type="submit" :disabled="createUserMutation.isPending.value">
        {{ createUserMutation.isPending.value ? 'Creating...' : 'Create user' }}
      </UiButton>
    </form>

    <p v-if="errorMessage" class="users-page__error">{{ errorMessage }}</p>
    <p v-else-if="usersQuery.error.value" class="users-page__error">
      {{ getApiErrorMessage(usersQuery.error.value) }}
    </p>

    <UiTable v-if="users.length > 0">
      <thead>
        <tr>
          <th>ID</th>
          <th>Email</th>
          <th>Name</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.email }}</td>
          <td v-if="editingUserId !== user.id">{{ user.full_name }}</td>
          <td v-else>
            <input
              v-model="editName"
              class="ui-input users-page__inline-input"
              type="text"
              autocomplete="name"
            />
          </td>
          <td v-if="editingUserId !== user.id">{{ user.is_active ? 'Active' : 'Inactive' }}</td>
          <td v-else>
            <label class="users-page__checkbox">
              <input v-model="editIsActive" type="checkbox" />
              Active
            </label>
          </td>
          <td class="users-page__actions">
            <template v-if="editingUserId !== user.id">
              <UiButton size="sm" variant="ghost" @click="startEdit(user.id)">Edit</UiButton>
              <UiButton
                size="sm"
                variant="ghost"
                :disabled="deleteUserMutation.isPending.value"
                @click="removeUser(user.id)"
              >
                Delete
              </UiButton>
            </template>
            <template v-else>
              <input
                v-model="editPassword"
                class="ui-input users-page__inline-input"
                type="password"
                placeholder="New password (optional)"
                autocomplete="new-password"
              />
              <UiButton
                size="sm"
                :disabled="updateUserMutation.isPending.value"
                @click="submitEdit(user.id)"
              >
                Save
              </UiButton>
              <UiButton size="sm" variant="ghost" @click="cancelEdit">Cancel</UiButton>
            </template>
          </td>
        </tr>
      </tbody>
    </UiTable>
  </section>
</template>

<style scoped lang="scss">
.users-page {
  display: grid;
  gap: var(--space-4);

  &__create {
    display: grid;
    gap: var(--space-3);
    grid-template-columns: repeat(3, minmax(180px, 1fr)) auto;
    align-items: end;
  }

  &__error {
    color: var(--color-danger);
    font-size: 0.875rem;
  }

  &__actions {
    display: inline-flex;
    gap: var(--space-2);
    align-items: center;
  }

  &__inline-input {
    min-width: 170px;
    height: 34px;
  }

  &__checkbox {
    display: inline-flex;
    gap: var(--space-2);
    align-items: center;
  }
}

@media (max-width: 1000px) {
  .users-page {
    &__create {
      grid-template-columns: 1fr;
    }
  }
}
</style>
