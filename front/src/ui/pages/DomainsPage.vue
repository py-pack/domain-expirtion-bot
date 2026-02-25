<script setup lang="ts">
import {computed, ref} from 'vue'
import {Search} from 'lucide-vue-next'
import {useDomainExpirationQuery} from '@/domain/domains/queries'
import {getApiErrorMessage} from '@/shared/http/errors'
import {formatIsoDate} from '@/shared/utils/time'
import UiButton from '@/ui/components/common/UiButton.vue'
import UiEntityPageLayout from '@/ui/layout/UiEntityPageLayout.vue'

const inputDomain = ref('')
const selectedDomain = ref('')
const submitted = ref(false)

const expirationQuery = useDomainExpirationQuery(selectedDomain)

const normalizedInput = computed(() => inputDomain.value.trim().toLowerCase())
const canSubmit = computed(() => normalizedInput.value.length > 0)

const errorMessage = computed(() => {
  if (!expirationQuery.error.value) {
    return null
  }

  return getApiErrorMessage(expirationQuery.error.value)
})

const formattedExpirationDate = computed(() => {
  if (!expirationQuery.data.value) {
    return ''
  }

  return formatIsoDate(expirationQuery.data.value.expirationDate)
})

function submitDomain(): void {
  if (!canSubmit.value) {
    return
  }

  submitted.value = true
  selectedDomain.value = normalizedInput.value
}
</script>

<template>
  <UiEntityPageLayout
    class="domains-page"
    title="Domain Expiration"
    description="Fetch expiration details from the backend /api/domain/expiration endpoint."
    :breadcrumbs="[{label: 'Domains'}]"
  >
    <form class="domains-page__form" @submit.prevent="submitDomain">
      <label class="domains-page__input-wrap">
        <Search :size="16" class="domains-page__search-icon" />
        <input
          v-model="inputDomain"
          class="ui-input domains-page__input"
          type="text"
          placeholder="example.com"
        />
      </label>

      <UiButton type="submit" :disabled="!canSubmit || expirationQuery.isFetching.value">
        {{ expirationQuery.isFetching.value ? 'Checking...' : 'Check domain' }}
      </UiButton>
    </form>

    <p v-if="errorMessage" class="domains-page__error">{{ errorMessage }}</p>

    <article v-if="expirationQuery.data.value" class="domains-page__result">
      <h3>{{ expirationQuery.data.value.domain }}</h3>
      <p>Expiration date: {{ formattedExpirationDate }}</p>
    </article>

    <p
      v-else-if="submitted && !expirationQuery.isFetching.value && !expirationQuery.error.value"
      class="domains-page__hint"
    >
      No data received for this domain.
    </p>
  </UiEntityPageLayout>
</template>

<style scoped lang="scss">
.domains-page {
  display: grid;
  gap: var(--space-4);

  &__form {
    display: grid;
    gap: var(--space-3);
    grid-template-columns: minmax(0, 1fr) auto;
  }

  &__input-wrap {
    position: relative;
  }

  &__search-icon {
    position: absolute;
    left: var(--space-3);
    top: 50%;
    transform: translateY(-50%);
    color: var(--color-text-muted);
  }

  &__input {
    padding-left: 34px;
  }

  &__error {
    color: var(--color-danger);
    font-size: 0.875rem;
  }

  &__hint {
    color: var(--color-text-muted);
    font-size: 0.875rem;
  }

  &__result {
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-4);
    background: var(--color-surface-soft);
    display: grid;
    gap: var(--space-1);
  }
}

@media (max-width: 720px) {
  .domains-page {
    &__form {
      grid-template-columns: 1fr;
    }
  }
}
</style>
