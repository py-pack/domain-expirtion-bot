<script setup lang="ts">
import {computed, nextTick, onBeforeUnmount, ref, watch} from 'vue'
import {createId} from '@/shared/utils/id'

const props = withDefaults(
  defineProps<{
    text: string
    maxWidth?: number
  }>(),
  {
    maxWidth: 320,
  },
)

const isOpen = ref(false)
const triggerRef = ref<HTMLElement | null>(null)
const tooltipRef = ref<HTMLElement | null>(null)
const tooltipId = computed(() => `ui-tooltip-${createId()}`)
const position = ref({top: 0, left: 0})

function updatePosition(): void {
  const trigger = triggerRef.value
  const tooltip = tooltipRef.value

  if (!trigger || !tooltip) {
    return
  }

  const triggerRect = trigger.getBoundingClientRect()
  const tooltipRect = tooltip.getBoundingClientRect()
  const viewportWidth = window.innerWidth
  const gap = 8

  let left = triggerRect.left + triggerRect.width / 2 - tooltipRect.width / 2
  left = Math.max(gap, Math.min(left, viewportWidth - tooltipRect.width - gap))

  let top = triggerRect.bottom + gap
  const canRenderBelow = top + tooltipRect.height <= window.innerHeight - gap

  if (!canRenderBelow) {
    top = Math.max(gap, triggerRect.top - tooltipRect.height - gap)
  }

  position.value = {top, left}
}

async function openTooltip(): Promise<void> {
  if (isOpen.value) {
    return
  }

  isOpen.value = true
  await nextTick()
  updatePosition()
}

function closeTooltip(): void {
  isOpen.value = false
}

function handleEscape(event: KeyboardEvent): void {
  if (event.key === 'Escape') {
    closeTooltip()
  }
}

function handleViewportChange(): void {
  if (!isOpen.value) {
    return
  }

  updatePosition()
}

watch(isOpen, (nextIsOpen) => {
  if (nextIsOpen) {
    window.addEventListener('resize', handleViewportChange)
    window.addEventListener('scroll', handleViewportChange, true)
    document.addEventListener('keydown', handleEscape)
    return
  }

  window.removeEventListener('resize', handleViewportChange)
  window.removeEventListener('scroll', handleViewportChange, true)
  document.removeEventListener('keydown', handleEscape)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleViewportChange)
  window.removeEventListener('scroll', handleViewportChange, true)
  document.removeEventListener('keydown', handleEscape)
})
</script>

<template>
  <span
    ref="triggerRef"
    class="ui-tooltip-trigger"
    :aria-describedby="isOpen ? tooltipId : undefined"
    @mouseenter="openTooltip"
    @mouseleave="closeTooltip"
    @focusin="openTooltip"
    @focusout="closeTooltip"
  >
    <slot />
  </span>

  <Teleport to="body">
    <div
      v-if="isOpen"
      :id="tooltipId"
      ref="tooltipRef"
      class="ui-tooltip"
      role="tooltip"
      :style="{
        top: `${position.top}px`,
        left: `${position.left}px`,
        maxWidth: `${props.maxWidth}px`,
      }"
    >
      {{ text }}
    </div>
  </Teleport>
</template>

<style scoped lang="scss">
.ui-tooltip-trigger {
  display: inline-flex;
}

.ui-tooltip {
  position: fixed;
  z-index: 2000;
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-sm);
  border: 1px solid var(--color-border);
  background: var(--color-surface);
  color: var(--color-text);
  box-shadow: var(--card-shadow);
  font-size: 0.875rem;
  line-height: 1.4;
  pointer-events: none;
}
</style>
