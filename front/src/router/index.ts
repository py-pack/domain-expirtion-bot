import { createRouter, createWebHistory } from 'vue-router'

import LoginView from '@/views/auth/LoginView.vue'
import DashboardView from '@/views/dashboard/DashboardView.vue'
import AuthLayout from '@/layouts/AuthLayout.vue'
import DashboardLayout from '@/layouts/DashboardLayout.vue'

const routes = [
  {
    path: '/login',
    component: AuthLayout,
    children: [{ path: '', component: LoginView }],
  },
  {
    path: '/dashboard',
    component: DashboardLayout,
    children: [{ path: '', component: DashboardView }],
  },
  {
    path: '/',
    redirect: '/login',
  },
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
})
