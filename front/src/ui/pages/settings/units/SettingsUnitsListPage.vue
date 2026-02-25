<script setup lang="ts">
import {computed, ref} from 'vue'
import {useRouter} from 'vue-router'
import {
  useDeleteUnitMutation,
  useUnitsQuery,
} from '@/domain/units/queries'
import {getApiErrorMessage} from '@/shared/http/errors'
import UiButton from '@/ui/components/common/UiButton.vue'
import UiTable from '@/ui/components/common/UiTable.vue'

const router = useRouter()

const unitsQuery = useUnitsQuery()
const deleteUnitMutation = useDeleteUnitMutation()

const actionError = ref<string | null>(null)
const actionSuccess = ref<string | null>(null)

const units = computed(() => unitsQuery.data.value ?? [])

function openEditPage(unitId: number): void {
  void router.push({name: 'settings-units-edit', params: {id: String(unitId)}})
}

async function removeUnit(unitId: number): Promise<void> {
  actionError.value = null
  actionSuccess.value = null

  if (!window.confirm(`Delete unit #${unitId}?`)) {
    return
  }

  try {
    await deleteUnitMutation.mutateAsync(unitId)
    actionSuccess.value = 'Unit deleted successfully.'
  } catch (error: unknown) {
    actionError.value = getApiErrorMessage(error)
  }
}
</script>

<template>
  <section class="settings-units-page">
    <p class="settings-units-page__text">
      Manage units and open a dedicated page to edit unit name and responsibles.
    </p>

    <p v-if="actionError" class="settings-units-page__error">{{ actionError }}</p>
    <p v-if="actionSuccess" class="settings-units-page__success">{{ actionSuccess }}</p>
    <p v-if="unitsQuery.error.value" class="settings-units-page__error">
      {{ getApiErrorMessage(unitsQuery.error.value) }}
    </p>

    <p v-if="unitsQuery.isLoading.value" class="settings-units-page__state">Loading units...</p>
    <p v-else-if="units.length === 0" class="settings-units-page__state">No units yet.</p>

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
          <td class="settings-units-page__actions">
            <UiButton size="sm" variant="ghost" @click="openEditPage(unit.id)">
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
  </section>
</template>

<style scoped lang="scss">
.settings-units-page {
  display: grid;
  gap: var(--space-4);

  &__text,
  &__state {
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

  &__actions {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
  }
}
</style>
