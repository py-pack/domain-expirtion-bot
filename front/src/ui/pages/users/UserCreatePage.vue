<script setup lang="ts">
import {ref} from 'vue'
import {useRouter} from 'vue-router'
import {useCreateSystemUserMutation} from '@/domain/users/queries'
import {getApiErrorMessage} from '@/shared/http/errors'
import UiButton from '@/ui/components/common/UiButton.vue'
import UiEntityPageLayout from '@/ui/layout/UiEntityPageLayout.vue'
import UiFormField from '@/ui/components/common/UiFormField.vue'

const router = useRouter()
const createUserMutation = useCreateSystemUserMutation()

const email = ref('')
const fullName = ref('')
const password = ref('')
const isActive = ref(true)
const errorMessage = ref<string | null>(null)

async function submitCreate(): Promise<void> {
  errorMessage.value = null

  try {
    await createUserMutation.mutateAsync({
      email: email.value.trim(),
      full_name: fullName.value.trim(),
      password: password.value,
      is_active: isActive.value,
      settings: {},
    })

    void router.push({name: 'users'})
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
    title="Create user"
    description="Create a new system user account and set initial access parameters."
    :breadcrumbs="[
      {label: 'Users', to: {name: 'users'}},
      {label: 'Create'},
    ]"
  >
    <template #actions>
      <UiButton variant="ghost" @click="goBack">Back to list</UiButton>
    </template>

    <p v-if="errorMessage" class="user-form-page__error">{{ errorMessage }}</p>

    <form class="user-form-page__form" @submit.prevent="submitCreate">
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

      <div class="user-form-page__actions">
        <UiButton type="button" variant="ghost" @click="goBack">Cancel</UiButton>
        <UiButton type="submit" :disabled="createUserMutation.isPending.value">
          {{ createUserMutation.isPending.value ? 'Creating...' : 'Create user' }}
        </UiButton>
      </div>
    </form>
  </UiEntityPageLayout>
</template>

<style scoped lang="scss">
.user-form-page {
  display: grid;
  gap: var(--space-4);

  &__form {
    display: grid;
    gap: var(--space-3);
    max-width: 720px;
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
  }

  &__error {
    color: var(--color-danger);
    font-size: 0.875rem;
  }
}

@media (max-width: 768px) {
  .user-form-page {
    &__actions {
      flex-wrap: wrap;
    }
  }
}
</style>
