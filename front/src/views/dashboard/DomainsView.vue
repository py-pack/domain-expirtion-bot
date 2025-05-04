<script setup lang="ts">
import { ref, onMounted } from 'vue';

const isMounted = ref(false);

onMounted(() => {
  isMounted.value = true;
});
</script>

<template>
  <div v-if="isMounted" class="domains-page">
    <h1>Domains</h1>
    <p>This page is under construction.</p>
  </div>
</template>

<style lang="scss" scoped>
.domains-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 50vh;
  text-align: center;
  color: var(--color-text-secondary);
}
</style>