import {createRouter, createWebHistory} from 'vue-router'
import {checkIfUserIsAuthenticated} from '@/utils/auth'

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
        meta: { requiresAuth: true },  // Добавляем мета-данные
        children: [{path: '', component: DashboardView}],
    },
    {
        path: '/integrations',
        component: DashboardLayout,
        meta: { requiresAuth: true },
        children: [{path: '', component: IntegrationsView}]
    },
    {
        path: '/domains',
        component: DashboardLayout,
        meta: { requiresAuth: true },
        children: [{path: '', component: DomainsView}]
    },
    {
        path: '/logs',
        component: DashboardLayout,
        meta: { requiresAuth: true },
        children: [{path: '', component: LogsView}]
    }
]

export const router = createRouter({
    history: createWebHistory(),
    routes,
})


// Добавляем глобальный навигационный хук
router.beforeEach((to, from, next) => {
    // Проверяем, требует ли маршрут авторизации
    if (to.matched.some(record => record.meta.requiresAuth)) {
        // Проверяем, авторизован ли пользователь
        // Здесь должна быть ваша логика проверки авторизации
        const isAuthenticated = checkIfUserIsAuthenticated() // Ваша функция проверки

        if (!isAuthenticated) {
            // Если не авторизован, перенаправляем на страницу входа
            next({ path: '/login' })
        } else {
            // Если авторизован, разрешаем переход
            next()
        }
    } else {
        // Для маршрутов, не требующих авторизации, просто разрешаем переход
        next()
    }
})

router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requiresAuth)) {
        const isAuthenticated = checkIfUserIsAuthenticated()

        if (!isAuthenticated) {
            // Сохраняем изначально запрошенный URL
            next({
                path: '/login',
                query: { redirect: to.fullPath }
            })
        } else {
            next()
        }
    } else {
        next()
    }
})