<script setup lang="ts">
import {ref} from 'vue'
import {useRouter} from 'vue-router'
import {useCreateUnitMutation} from '@/domain/units/queries'
import {getApiErrorMessage} from '@/shared/http/errors'
import UiButton from '@/ui/components/common/UiButton.vue'
import UiFormField from '@/ui/components/common/UiFormField.vue'

const router = useRouter()
const createUnitMutation = useCreateUnitMutation()

const name = ref('')
const errorMessage = ref<string | null>(null)

async function submitCreate(): Promise<void> {
  errorMessage.value = null

  try {
    const unit = await createUnitMutation.mutateAsync({
      name: name.value.trim(),
    })

    void router.push({name: 'settings-units-edit', params: {id: String(unit.id)}})
  } catch (error: unknown) {
    errorMessage.value = getApiErrorMessage(error)
  }
}
</script>

<template>
  <section class="settings-unit-form-page">
    <p class="settings-unit-form-page__text">
      Create a new unit, then continue to the edit page to assign responsibles.
    </p>

    <p v-if="errorMessage" class="settings-unit-form-page__error">{{ errorMessage }}</p>

    <form class="settings-unit-form-page__form" @submit.prevent="submitCreate">
      <UiFormField
        id="unit-create-name"
        label="Unit name"
        :model-value="name"
        required
        @update:model-value="name = $event"
      />

      <div class="settings-unit-form-page__actions">
        <UiButton type="button" variant="ghost" @click="router.push({name: 'settings-units'})">
          Cancel
        </UiButton>
        <UiButton type="submit" :disabled="createUnitMutation.isPending.value">
          {{ createUnitMutation.isPending.value ? 'Creating...' : 'Create unit' }}
        </UiButton>
      </div>
    </form>
  </section>
</template>

<style scoped lang="scss">
.settings-unit-form-page {
  display: grid;
  gap: var(--space-4);

  &__text {
    margin: 0;
    color: var(--color-text-muted);
  }

  &__form {
    display: grid;
    gap: var(--space-3);
    max-width: 520px;
  }

  &__actions {
    display: inline-flex;
    gap: var(--space-2);
    flex-wrap: wrap;
  }

  &__error {
    margin: 0;
    color: var(--color-danger);
    font-size: 0.875rem;
  }
}
</style>
