<script setup lang="ts">
import {computed} from 'vue'
import {Pencil, Plus, Trash2} from 'lucide-vue-next'
import {useRouter} from 'vue-router'
import {
  useDeleteSystemUserMutation,
  useSystemUsersQuery,
} from '@/domain/users/queries'
import {getApiErrorMessage} from '@/shared/http/errors'
import {showErrorToast, showSuccessToast} from '@/shared/ui/toast'
import UiButton from '@/ui/components/common/UiButton.vue'
import UiEntityPageLayout from '@/ui/layout/UiEntityPageLayout.vue'
import UiTable from '@/ui/components/common/UiTable.vue'

const router = useRouter()

const usersQuery = useSystemUsersQuery()
const deleteUserMutation = useDeleteSystemUserMutation()

const users = computed(() => usersQuery.data.value ?? [])

function openCreatePage(): void {
  void router.push({name: 'users-create'})
}

function openEditPage(userId: number): void {
  void router.push({name: 'users-edit', params: {id: String(userId)}})
}

async function removeUser(userId: number): Promise<void> {
  try {
    await deleteUserMutation.mutateAsync(userId)
    showSuccessToast('User deleted successfully.')
  } catch (error: unknown) {
    showErrorToast(getApiErrorMessage(error))
  }
}
</script>

<template>
  <UiEntityPageLayout
    class="users-page"
    title="Users"
    description="System users management: view the list, open editing, create new users, and remove users."
    :breadcrumbs="[{label: 'Users'}]"
  >
    <template #actions>
      <UiButton tone="success" @click="openCreatePage">
        <template #icon>
          <Plus :size="16" />
        </template>
        Create user
      </UiButton>
    </template>

    <p v-if="usersQuery.error.value" class="users-page__error">
      {{ getApiErrorMessage(usersQuery.error.value) }}
    </p>

    <p v-if="usersQuery.isLoading.value" class="users-page__state">Loading users...</p>

    <p v-else-if="users.length === 0" class="users-page__state">No users yet.</p>

    <UiTable v-else>
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
          <td>{{ user.full_name }}</td>
          <td>{{ user.is_active ? 'Active' : 'Inactive' }}</td>
          <td class="users-page__actions">
            <UiButton size="sm" variant="ghost" @click="openEditPage(user.id)">
              <template #icon>
                <Pencil :size="16" />
              </template>
              Edit
            </UiButton>
            <UiButton
              size="sm"
              variant="ghost"
              tone="danger"
              :disabled="deleteUserMutation.isPending.value"
              @click="removeUser(user.id)"
            >
              <template #icon>
                <Trash2 :size="16" />
              </template>
              Delete
            </UiButton>
          </td>
        </tr>
      </tbody>
    </UiTable>
  </UiEntityPageLayout>
</template>

<style scoped lang="scss">
.users-page {
  display: grid;
  gap: var(--space-4);

  &__error {
    color: var(--color-danger);
    font-size: 0.875rem;
  }

  &__state {
    color: var(--color-text-muted);
  }

  &__actions {
    display: inline-flex;
    gap: var(--space-2);
    align-items: center;
  }
}
</style>
