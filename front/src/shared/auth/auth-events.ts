type AuthEvent = 'session-expired' | 'signed-out'
type Listener = () => void

const listeners: Record<AuthEvent, Set<Listener>> = {
  'session-expired': new Set<Listener>(),
  'signed-out': new Set<Listener>(),
}

export const authEvents = {
  on(event: AuthEvent, listener: Listener): () => void {
    listeners[event].add(listener)

    return () => {
      listeners[event].delete(listener)
    }
  },

  emit(event: AuthEvent): void {
    listeners[event].forEach((listener) => listener())
  },
}
