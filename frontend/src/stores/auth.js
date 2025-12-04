import { defineStore } from 'pinia';
import api from '../api';
import { jwtDecode } from 'jwt-decode';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        token: localStorage.getItem('token') || null,
        user: null,
    }),
    getters: {
        isAuthenticated: (state) => !!state.token,
        isSuperuser: (state) => state.user?.is_superuser || false,
        hasPermission: (state) => (permissionCode) => {
            if (state.user?.is_superuser) return true;
            if (!state.user?.roles) return false;

            return state.user.roles.some(role =>
                role.permissions.some(p => p.code === permissionCode)
            );
        },
    },
    actions: {
        async login(username, password) {
            const formData = new FormData();
            formData.append('username', username);
            formData.append('password', password);

            const response = await api.post('/login/access-token', formData);
            this.token = response.data.access_token;
            localStorage.setItem('token', this.token);
            await this.fetchUser();
        },
        async fetchUser() {
            if (!this.token) return;
            try {
                const response = await api.get('/users/me');
                this.user = response.data;
            } catch (error) {
                this.logout();
            }
        },
        logout() {
            this.token = null;
            this.user = null;
            localStorage.removeItem('token');
        },
    },
});
