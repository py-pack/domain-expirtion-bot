<script setup lang="ts">
import {onBeforeUnmount, onMounted} from 'vue'
import {useRouter} from 'vue-router'
import {useLogoutMutation} from '@/domain/auth/queries'
import {authEvents} from '@/shared/auth/auth-events'
import Topbar from '@/ui/layout/Topbar.vue'

const router = useRouter()
const logoutMutation = useLogoutMutation()

let stopSessionExpiredListener: (() => void) | null = null
let stopSignedOutListener: (() => void) | null = null

onMounted(() => {
  stopSessionExpiredListener = authEvents.on('session-expired', async () => {
    await router.push('/login')
  })

  stopSignedOutListener = authEvents.on('signed-out', async () => {
    await router.push('/login')
  })
})

onBeforeUnmount(() => {
  stopSessionExpiredListener?.()
  stopSignedOutListener?.()
})

async function handleLogout(): Promise<void> {
  await logoutMutation.mutateAsync()
}
</script>

<template>
  <div class="app-shell">
    <Topbar @logout="handleLogout" />

    <main class="page-content">
      <RouterView />
    </main>
  </div>
</template>
