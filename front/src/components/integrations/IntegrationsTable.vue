<script setup lang="ts">
import { ref, computed } from 'vue';
import type { Integration } from '@/types';
import StatusPill from '@/components/ui/StatusPill.vue';
import UnitTag from '@/components/ui/UnitTag.vue';
import IconSettings from '@/components/icons/IconSettings.vue';

const props = defineProps<{
  integrations: Integration[];
  searchQuery?: string;
  statusFilter?: string;
  typeFilter?: string;
}>();

// Computed filtered integrations
const filteredIntegrations = computed(() => {
  let filtered = [...props.integrations];
  
  // Apply search filter
  if (props.searchQuery && props.searchQuery.trim() !== '') {
    const query = props.searchQuery.toLowerCase();
    filtered = filtered.filter(integration => 
      integration.name.toLowerCase().includes(query) || 
      integration.login.toLowerCase().includes(query)
    );
  }
  
  // Apply status filter
  if (props.statusFilter && props.statusFilter !== 'all') {
    filtered = filtered.filter(integration => integration.status === props.statusFilter);
  }
  
  // Apply type filter
  if (props.typeFilter && props.typeFilter !== 'all') {
    filtered = filtered.filter(integration => integration.type === props.typeFilter);
  }
  
  return filtered;
});
</script>

<template>
  <div class="table-responsive">
    <table class="table integrations-table">
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
        <tr v-for="integration in filteredIntegrations" :key="integration.id">
          <td>
            <div class="type-cell">
              <div class="type-icon">
                <img :src="integration.icon" :alt="integration.type" class="integration-icon">
              </div>
            </div>
          </td>
          <td>{{ integration.name }}</td>
          <td>{{ integration.login }}</td>
          <td>
            <StatusPill :status="integration.status" />
          </td>
          <td>
            <div class="units-container">
              <UnitTag v-for="(unit, index) in integration.units" :key="index" :text="unit" />
            </div>
          </td>
          <td>{{ integration.lastSync }}</td>
          <td>
            <button class="btn-icon-only">
              <IconSettings />
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style lang="scss" scoped>
.integrations-table {
  width: 100%;
  
  .type-cell {
    display: flex;
    align-items: center;
  }
  
  .type-icon {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
  }
  
  .integration-icon {
    width: 100%;
    height: 100%;
    object-fit: contain;
  }
  
  .units-container {
    display: flex;
    flex-wrap: wrap;
    gap: var(--spacing-1);
  }
}
</style>