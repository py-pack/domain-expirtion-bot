import {readonly, ref} from 'vue'

export type UiToastVariant = 'success' | 'error'

export type UiToast = {
  id: number
  message: string
  variant: UiToastVariant
}

const TOAST_TIMEOUT_MS = 4000
const MAX_TOASTS = 5

const toasts = ref<UiToast[]>([])
const toastTimers = new Map<number, ReturnType<typeof setTimeout>>()

let nextToastId = 1

function removeToast(id: number): void {
  const timer = toastTimers.get(id)
  if (timer) {
    clearTimeout(timer)
    toastTimers.delete(id)
  }

  toasts.value = toasts.value.filter((toast) => toast.id !== id)
}

function showToast(message: string, variant: UiToastVariant): void {
  const normalizedMessage = message.trim()

  if (!normalizedMessage) {
    return
  }

  const id = nextToastId++
  const nextToast: UiToast = {
    id,
    message: normalizedMessage,
    variant,
  }

  toasts.value = [...toasts.value, nextToast].slice(-MAX_TOASTS)

  const timer = setTimeout(() => {
    removeToast(id)
  }, TOAST_TIMEOUT_MS)

  toastTimers.set(id, timer)
}

export function showSuccessToast(message: string): void {
  showToast(message, 'success')
}

export function showErrorToast(message: string): void {
  showToast(message, 'error')
}

export function useToastState() {
  return {
    toasts: readonly(toasts),
    removeToast,
  }
}
