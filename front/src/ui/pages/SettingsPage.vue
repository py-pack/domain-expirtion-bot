<script setup lang="ts">
import {computed, ref, watch} from 'vue'
import {getApiErrorMessage} from '@/shared/http/errors'
import {
  useCurrentUserQuery,
  useUpdateCurrentUserMutation,
} from '@/domain/users/queries'
import UiButton from '@/ui/components/common/UiButton.vue'
import UiFormField from '@/ui/components/common/UiFormField.vue'

const currentUserQuery = useCurrentUserQuery()
const updateCurrentUserMutation = useUpdateCurrentUserMutation()

const fullName = ref('')
const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')

const errorMessage = ref<string | null>(null)
const successMessage = ref<string | null>(null)

watch(
  () => currentUserQuery.data.value,
  (user) => {
    if (!user) {
      return
    }

    fullName.value = user.full_name
  },
  {immediate: true},
)

const email = computed(() => currentUserQuery.data.value?.email ?? '')
const isSubmitting = computed(() => updateCurrentUserMutation.isPending.value)

function resetPasswordFields(): void {
  currentPassword.value = ''
  newPassword.value = ''
  confirmPassword.value = ''
}

function validatePasswordChange(): string | null {
  const hasAnyPasswordField =
    currentPassword.value.length > 0 ||
    newPassword.value.length > 0 ||
    confirmPassword.value.length > 0

  if (!hasAnyPasswordField) {
    return null
  }

  if (!currentPassword.value || !newPassword.value || !confirmPassword.value) {
    return 'Fill current password, new password, and confirm password to change password.'
  }

  if (newPassword.value.length < 8) {
    return 'New password must be at least 8 characters.'
  }

  if (newPassword.value !== confirmPassword.value) {
    return 'New password and confirmation do not match.'
  }

  return null
}

async function submitSettings(): Promise<void> {
  errorMessage.value = null
  successMessage.value = null

  const normalizedName = fullName.value.trim()
  if (!normalizedName) {
    errorMessage.value = 'Name is required.'
    return
  }

  const passwordValidationError = validatePasswordChange()
  if (passwordValidationError) {
    errorMessage.value = passwordValidationError
    return
  }

  try {
    await updateCurrentUserMutation.mutateAsync({
      full_name: normalizedName,
      current_password: currentPassword.value || undefined,
      new_password: newPassword.value || undefined,
    })

    resetPasswordFields()
    successMessage.value = 'Settings updated successfully.'
  } catch (error: unknown) {
    errorMessage.value = getApiErrorMessage(error)
  }
}
</script>

<template>
  <section class="page-card settings-page">
    <h1 class="page-title">Account Settings</h1>
    <p class="page-subtitle">Update your display name and change password.</p>

    <p v-if="currentUserQuery.isLoading.value" class="settings-page__hint">
      Loading account...
    </p>
    <p v-else-if="currentUserQuery.error.value" class="settings-page__error">
      {{ getApiErrorMessage(currentUserQuery.error.value) }}
    </p>

    <form
      v-else
      class="settings-page__form"
      autocomplete="off"
      @submit.prevent="submitSettings"
    >
      <UiFormField
        id="settings-email"
        label="Email"
        :model-value="email"
        type="email"
        readonly
      />

      <UiFormField
        id="settings-full-name"
        label="Name"
        :model-value="fullName"
        autocomplete="name"
        required
        @update:model-value="fullName = $event"
      />

      <div class="settings-page__divider" />

      <UiFormField
        id="settings-current-password"
        label="Current password"
        type="password"
        autocomplete="current-password"
        :model-value="currentPassword"
        @update:model-value="currentPassword = $event"
      />

      <UiFormField
        id="settings-new-password"
        label="New password"
        type="password"
        autocomplete="new-password"
        :model-value="newPassword"
        @update:model-value="newPassword = $event"
      />

      <UiFormField
        id="settings-confirm-password"
        label="Confirm new password"
        type="password"
        autocomplete="new-password"
        :model-value="confirmPassword"
        @update:model-value="confirmPassword = $event"
      />

      <p v-if="errorMessage" class="settings-page__error">{{ errorMessage }}</p>
      <p v-if="successMessage" class="settings-page__success">{{ successMessage }}</p>

      <UiButton type="submit" :disabled="isSubmitting">
        {{ isSubmitting ? 'Saving...' : 'Save settings' }}
      </UiButton>
    </form>
  </section>
</template>

<style scoped lang="scss">
.settings-page {
  display: grid;
  gap: var(--space-4);
  max-width: 620px;

  &__form {
    display: grid;
    gap: var(--space-3);
  }

  &__divider {
    height: 1px;
    background: var(--color-border);
    margin: var(--space-1) 0;
  }

  &__hint {
    color: var(--color-text-muted);
    font-size: 0.875rem;
  }

  &__error {
    color: var(--color-danger);
    font-size: 0.875rem;
  }

  &__success {
    color: var(--color-success);
    font-size: 0.875rem;
  }
}
</style>
