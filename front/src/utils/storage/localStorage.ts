type StorageReader = <T = unknown>(args: { key: string }) => T | null
type StorageWriter = <T = unknown>(args: { key: string; value: T }) => void
type StorageRemover = (args: { key: string }) => void

export function createStorage(namespace: string) {
  const prefix = `${namespace}:`

  const read: StorageReader = ({ key }) => {
    try {
      const item = localStorage.getItem(prefix + key)
      return item ? JSON.parse(item) : null
    } catch {
      return null
    }
  }

  const write: StorageWriter = ({ key, value }) => {
    localStorage.setItem(prefix + key, JSON.stringify(value))
  }

  const remove: StorageRemover = ({ key }) => {
    localStorage.removeItem(prefix + key)
  }

  return { read, write, remove }
}
