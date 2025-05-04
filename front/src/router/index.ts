import {createRouter, createWebHistory} from 'vue-router'

import AuthLayout from '@/layouts/AuthLayout.vue'
import DashboardLayout from '@/layouts/DashboardLayout.vue'

import LoginView from '@/views/auth/LoginView.vue'
import DashboardView from '@/views/dashboard/DashboardView.vue'
import IntegrationsView from '@/views/dashboard/IntegrationsView.vue'
import DomainsView from '@/views/dashboard/DomainsView.vue'
import LogsView from '@/views/dashboard/LogsView.vue'

const routes = [
    {
        path: '/login',
        component: AuthLayout,
        children: [{path: '', component: LoginView}],
    },
    {
        path: '/',
        component: DashboardLayout,
        children: [{path: '', component: DashboardView}],
    },
    {
        path: '/integrations',
        component: DashboardLayout,
        children: [{path: '', component: IntegrationsView}]
    },
    {
        path: '/domains',
        component: DashboardLayout,
        children: [{path: '', component: DomainsView}]
    },
    {
        path: '/logs',
        component: DashboardLayout,
        children: [{path: '', component: LogsView}]
    }
]

export const router = createRouter({
    history: createWebHistory(),
    routes,
})
