import {defineStore} from 'pinia'

export type Theme = 'light' | 'dark'

const STORAGE_KEY = 'ui:theme'

function isTheme(value: unknown): value is Theme {
  return value === 'light' || value === 'dark'
}

function readStoredTheme(): Theme {
  if (typeof window === 'undefined') {
    return 'light'
  }

  const stored = window.localStorage.getItem(STORAGE_KEY)

  return isTheme(stored) ? stored : 'light'
}

function applyTheme(theme: Theme): void {
  document.body.dataset.theme = theme
}

function persistTheme(theme: Theme): void {
  window.localStorage.setItem(STORAGE_KEY, theme)
}

export const useThemeStore = defineStore('theme', {
  state: () => ({
    theme: 'light' as Theme,
  }),
  actions: {
    init(): void {
      this.theme = readStoredTheme()
      applyTheme(this.theme)
    },

    setTheme(theme: Theme): void {
      this.theme = theme
      applyTheme(theme)
      persistTheme(theme)
    },

    toggleTheme(): void {
      this.setTheme(this.theme === 'light' ? 'dark' : 'light')
    },
  },
})
