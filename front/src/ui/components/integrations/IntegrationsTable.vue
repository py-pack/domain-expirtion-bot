<script setup lang="ts">
import {Pencil} from 'lucide-vue-next'
import type {Integration} from '@/domain/integrations/model'
import UiButton from '@/ui/components/common/UiButton.vue'
import UiStatusPill from '@/ui/components/common/UiStatusPill.vue'
import UiTable from '@/ui/components/common/UiTable.vue'
import UiUnitTag from '@/ui/components/common/UiUnitTag.vue'

defineProps<{
  integrations: Integration[]
}>()
</script>

<template>
  <UiTable>
    <thead>
      <tr>
        <th>Type</th>
        <th>Name</th>
        <th>Login</th>
        <th>Status</th>
        <th>Units</th>
        <th>Last Sync</th>
        <th>Edit</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="integration in integrations" :key="integration.id">
        <td>
          <img class="integrations-table__icon" :src="integration.icon" :alt="integration.type" />
        </td>
        <td>{{ integration.name }}</td>
        <td>{{ integration.login }}</td>
        <td>
          <UiStatusPill :status="integration.status" />
        </td>
        <td>
          <div class="integrations-table__units">
            <UiUnitTag
              v-for="unit in integration.units"
              :key="`${integration.id}-${unit}`"
              :text="unit"
            />
          </div>
        </td>
        <td>{{ integration.lastSync }}</td>
        <td>
          <UiButton
            type="button"
            size="md"
            variant="ghost"
            tone="primary"
            icon-only
            aria-label="Edit integration"
          >
            <template #icon>
              <Pencil :size="16" />
            </template>
          </UiButton>
        </td>
      </tr>
    </tbody>
  </UiTable>
</template>

<style scoped lang="scss">
.integrations-table {
  &__icon {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    object-fit: contain;
    background: var(--color-surface-soft);
    padding: 3px;
  }

  &__units {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-1);
  }
}
</style>
