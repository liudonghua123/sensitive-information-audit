import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import Login from '../views/Login.vue';
import Dashboard from '../views/Dashboard.vue';
import Connections from '../views/Connections.vue';
import Rules from '../views/Rules.vue';
import Tasks from '../views/Tasks.vue';
import Users from '../views/Users.vue';
import Roles from '../views/Roles.vue';
import Logs from '../views/Logs.vue';
import NotFound from '../views/NotFound.vue';
import Forbidden from '../views/Forbidden.vue';

const routes = [
    { path: '/login', component: Login },
    { path: '/403', component: Forbidden },
    {
        path: '/',
        component: Dashboard,
        meta: { requiresAuth: true },
        children: [
            { path: '', redirect: '/connections' },
            { path: 'connections', component: Connections },
            { path: 'rules', component: Rules },
            { path: 'tasks', component: Tasks },
            {
                path: 'users',
                component: Users,
                meta: { permission: 'user:read' }
            },
            {
                path: 'roles',
                component: Roles,
                meta: { permission: 'role:manage' }
            },
            {
                path: 'logs',
                component: Logs,
                meta: { requiresAuth: true }
            },
        ]
    },
    { path: '/:pathMatch(.*)*', component: NotFound },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach(async (to, from, next) => {
    const authStore = useAuthStore();

    // Check authentication
    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
        next('/login');
        return;
    }

    // Fetch user if authenticated but user data is missing (e.g. page refresh)
    if (authStore.isAuthenticated && !authStore.user) {
        try {
            await authStore.fetchUser();
        } catch (e) {
            next('/login');
            return;
        }
    }

    // Check permissions
    if (to.meta.permission) {
        if (!authStore.hasPermission(to.meta.permission)) {
            next('/403');
            return;
        }
    }

    next();
});

export default router;
