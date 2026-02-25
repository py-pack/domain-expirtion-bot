import {createRouter, createWebHistory, type RouteRecordRaw} from 'vue-router'
import {authGuard} from '@/app/router/guards'
import AppShell from '@/ui/layout/AppShell.vue'
import LoginPage from '@/ui/pages/LoginPage.vue'
import DashboardPage from '@/ui/pages/DashboardPage.vue'
import IntegrationsPage from '@/ui/pages/IntegrationsPage.vue'
import DomainsPage from '@/ui/pages/DomainsPage.vue'
import LogsPage from '@/ui/pages/LogsPage.vue'
import ProfilePage from '@/ui/pages/ProfilePage.vue'
import SettingsPage from '@/ui/pages/SettingsPage.vue'
import SettingsGeneralPage from '@/ui/pages/settings/SettingsGeneralPage.vue'
import SettingsNotificationsPage from '@/ui/pages/settings/SettingsNotificationsPage.vue'
import SettingsUnitCreatePage from '@/ui/pages/settings/units/SettingsUnitCreatePage.vue'
import SettingsUnitEditPage from '@/ui/pages/settings/units/SettingsUnitEditPage.vue'
import SettingsUnitsListPage from '@/ui/pages/settings/units/SettingsUnitsListPage.vue'
import UserCreatePage from '@/ui/pages/users/UserCreatePage.vue'
import UserEditPage from '@/ui/pages/users/UserEditPage.vue'
import UsersListPage from '@/ui/pages/users/UsersListPage.vue'

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
        component: UsersListPage,
      },
      {
        path: 'users/create',
        name: 'users-create',
        component: UserCreatePage,
      },
      {
        path: 'users/:id/edit',
        name: 'users-edit',
        component: UserEditPage,
      },
      {
        path: 'profile',
        name: 'profile',
        component: ProfilePage,
      },
      {
        path: 'settings',
        name: 'settings',
        component: SettingsPage,
        children: [
          {
            path: '',
            redirect: {name: 'settings-general'},
          },
          {
            path: 'general',
            name: 'settings-general',
            component: SettingsGeneralPage,
          },
          {
            path: 'units',
            name: 'settings-units',
            component: SettingsUnitsListPage,
          },
          {
            path: 'units/create',
            name: 'settings-units-create',
            component: SettingsUnitCreatePage,
          },
          {
            path: 'units/:id/edit',
            name: 'settings-units-edit',
            component: SettingsUnitEditPage,
          },
          {
            path: 'notifications',
            name: 'settings-notifications',
            component: SettingsNotificationsPage,
          },
        ],
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
