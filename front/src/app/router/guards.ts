import type {NavigationGuardWithThis} from 'vue-router'
import {authService} from '@/domain/auth/service'

export const authGuard: NavigationGuardWithThis<undefined> = async (to) => {
  if (to.path === '/login' && authService.isAuthenticated()) {
    return {name: 'dashboard'}
  }

  if (!to.meta.requiresAuth) {
    return true
  }

  if (authService.isAuthenticated()) {
    return true
  }

  try {
    await authService.refreshSession()
    return true
  } catch {
    return {
      path: '/login',
      query: {
        redirect: to.fullPath,
      },
    }
  }
}
