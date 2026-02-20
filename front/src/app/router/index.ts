import {createRouter, createWebHistory, type RouteRecordRaw} from 'vue-router'
import {authGuard} from '@/app/router/guards'
import AppShell from '@/ui/layout/AppShell.vue'
import LoginPage from '@/ui/pages/LoginPage.vue'
import DashboardPage from '@/ui/pages/DashboardPage.vue'
import IntegrationsPage from '@/ui/pages/IntegrationsPage.vue'
import DomainsPage from '@/ui/pages/DomainsPage.vue'
import LogsPage from '@/ui/pages/LogsPage.vue'
import SettingsPage from '@/ui/pages/SettingsPage.vue'
import UsersPage from '@/ui/pages/UsersPage.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'login',
    component: LoginPage,
  },
  {
    path: '/',
    component: AppShell,
    meta: {
      requiresAuth: true,
    },
    children: [
      {
        path: '',
        name: 'dashboard',
        component: DashboardPage,
      },
      {
        path: 'domains',
        name: 'domains',
        component: DomainsPage,
      },
      {
        path: 'integrations',
        name: 'integrations',
        component: IntegrationsPage,
      },
      {
        path: 'logs',
        name: 'logs',
        component: LogsPage,
      },
      {
        path: 'users',
        name: 'users',
        component: UsersPage,
      },
      {
        path: 'settings',
        name: 'settings',
        component: SettingsPage,
      },
    ],
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/',
  },
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(authGuard)
