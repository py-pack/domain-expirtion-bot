import {createApp} from 'vue'
import {VueQueryPlugin, QueryClient} from '@tanstack/vue-query'
import {createPinia} from 'pinia'
import App from '@/app/app.vue'
import {router} from '@/app/router'
import {useThemeStore} from '@/shared/ui/theme.store'
import '@/app/styles/main.scss'

export function bootstrapApp(): void {
  const app = createApp(App)
  const pinia = createPinia()

  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: 1,
        refetchOnWindowFocus: false,
      },
    },
  })

  app.use(pinia)
  app.use(VueQueryPlugin, {queryClient})
  app.use(router)

  const themeStore = useThemeStore(pinia)
  themeStore.init()

  app.mount('#app')
}
