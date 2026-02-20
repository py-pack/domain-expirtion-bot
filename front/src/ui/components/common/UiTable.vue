<template>
  <div class="ui-table-wrap">
    <table class="ui-table">
      <slot />
    </table>
  </div>
</template>

<style scoped lang="scss">
.ui-table-wrap {
  overflow-x: auto;
}

.ui-table {
  width: 100%;
  border-collapse: collapse;

  :deep(th),
  :deep(td) {
    text-align: left;
    padding: var(--space-3) var(--space-4);
    border-bottom: 1px solid var(--color-border);
    white-space: nowrap;
  }

  :deep(th) {
    color: var(--color-text-muted);
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }

  :deep(tbody tr:hover) {
    background: var(--color-surface-soft);
  }

  :deep(tbody tr:last-child td) {
    border-bottom: none;
  }
}
</style>
