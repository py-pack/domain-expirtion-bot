<script setup lang="ts">
import {computed, ref, watch} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import {
    useSystemUsersQuery,
    useUpdateSystemUserMutation,
} from '@/domain/users/queries'
import {getApiErrorMessage} from '@/shared/http/errors'
import UiButton from '@/ui/components/common/UiButton.vue'
import UiEntityPageLayout from '@/ui/layout/UiEntityPageLayout.vue'
import UiFormField from '@/ui/components/common/UiFormField.vue'

const route = useRoute()
const router = useRouter()

const usersQuery = useSystemUsersQuery()
const updateUserMutation = useUpdateSystemUserMutation()

const fullName = ref('')
const password = ref('')
const isActive = ref(true)
const errorMessage = ref<string | null>(null)
const initializedUserId = ref<number | null>(null)

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
        initializedUserId.value = nextId
    },
    {immediate: true},
)

async function submitEdit(): Promise<void> {
    errorMessage.value = null

    if (userId.value === null || selectedUser.value === null) {
        errorMessage.value = 'User not found.'
        return
    }

    const payload: { full_name: string; is_active: boolean; password?: string } = {
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
        title="Edit user"
        description="Update profile data, status, and optionally set a new password for a system user."
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

        <p v-if="errorMessage" class="user-form-page__error">{{ errorMessage }}</p>
        <p v-else-if="usersQuery.error.value" class="user-form-page__error">
            {{ getApiErrorMessage(usersQuery.error.value) }}
        </p>

        <p v-if="userId === null" class="user-form-page__state">Invalid user ID.</p>
        <p v-else-if="usersQuery.isLoading.value" class="user-form-page__state">
            Loading user...
        </p>
        <p
            v-else-if="!selectedUser"
            class="user-form-page__state"
        >
            User not found.
        </p>

        <form
            v-else
            class="user-form-page__form"
            @submit.prevent="submitEdit"
        >
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
                <input v-model="isActive" type="checkbox"/>
                Active user
            </label>

            <div class="user-form-page__actions">
                <UiButton type="button" variant="ghost" @click="goBack">Cancel</UiButton>
                <UiButton type="submit" :disabled="updateUserMutation.isPending.value">
                    {{ updateUserMutation.isPending.value ? 'Saving...' : 'Save changes' }}
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

    &__state {
        color: var(--color-text-muted);
    }

    &__meta {
        margin: 0;
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
