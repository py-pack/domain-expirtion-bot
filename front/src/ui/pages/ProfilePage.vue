<script setup lang="ts">
import {computed, ref, watch} from 'vue'
import {Save} from 'lucide-vue-next'
import {getApiErrorMessage} from '@/shared/http/errors'
import {showErrorToast, showSuccessToast} from '@/shared/ui/toast'
import {
  useCurrentUserQuery,
  useUpdateCurrentUserMutation,
} from '@/domain/users/queries'
import UiButton from '@/ui/components/common/UiButton.vue'
import UiEntityPageLayout from '@/ui/layout/UiEntityPageLayout.vue'
import UiFormField from '@/ui/components/common/UiFormField.vue'

const currentUserQuery = useCurrentUserQuery()
const updateCurrentUserMutation = useUpdateCurrentUserMutation()

const fullName = ref('')
const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')

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

async function submitProfile(): Promise<void> {
  const normalizedName = fullName.value.trim()
  if (!normalizedName) {
    showErrorToast('Name is required.')
    return
  }

  const passwordValidationError = validatePasswordChange()
  if (passwordValidationError) {
    showErrorToast(passwordValidationError)
    return
  }

  try {
    await updateCurrentUserMutation.mutateAsync({
      full_name: normalizedName,
      current_password: currentPassword.value || undefined,
      new_password: newPassword.value || undefined,
    })

    resetPasswordFields()
    showSuccessToast('Profile updated successfully.')
  } catch (error: unknown) {
    showErrorToast(getApiErrorMessage(error))
  }
}
</script>

<template>
  <UiEntityPageLayout
    class="profile-page"
    title="Profile"
    description="Update your display name and change the account password."
    :breadcrumbs="[{label: 'Profile'}]"
  >
    <template #meta>
      <p v-if="email" class="profile-page__meta">Email: {{ email }}</p>
    </template>

    <p v-if="currentUserQuery.isLoading.value" class="profile-page__hint">
      Loading account...
    </p>
    <p v-else-if="currentUserQuery.error.value" class="profile-page__error">
      {{ getApiErrorMessage(currentUserQuery.error.value) }}
    </p>

    <form
      v-else
      class="profile-page__form"
      autocomplete="off"
      @submit.prevent="submitProfile"
    >
      <UiFormField
        id="settings-full-name"
        label="Name"
        :model-value="fullName"
        autocomplete="name"
        required
        @update:model-value="fullName = $event"
      />

      <div class="profile-page__divider" />

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

      <UiButton type="submit" tone="primary" :disabled="isSubmitting">
        <template #icon>
          <Save :size="16" />
        </template>
        {{ isSubmitting ? 'Saving...' : 'Save profile' }}
      </UiButton>
    </form>
  </UiEntityPageLayout>
</template>

<style scoped lang="scss">
.profile-page {
  display: grid;
  gap: var(--space-4);

  &__form {
    display: grid;
    gap: var(--space-3);
    max-width: 620px;
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

  &__meta {
    margin: 0;
  }
}
</style>
