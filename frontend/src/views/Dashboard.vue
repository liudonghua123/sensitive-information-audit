<template>
  <div class="min-h-screen bg-gray-50 flex">
    <!-- Sidebar -->
    <div class="hidden md:flex md:w-64 md:flex-col fixed inset-y-0 z-10 bg-gradient-to-b from-primary-900 to-secondary-900 text-white shadow-xl">
      <div class="flex items-center justify-center h-16 px-4 bg-black bg-opacity-20">
        <div class="h-8 w-8 bg-gradient-to-br from-primary-400 to-secondary-400 rounded-lg flex items-center justify-center mr-3 font-bold text-white shadow-lg">A</div>
        <span class="text-xl font-bold tracking-wider">AuditSys</span>
      </div>
      <div class="flex-1 flex flex-col overflow-y-auto pt-5 pb-4">
        <nav class="mt-5 flex-1 px-2 space-y-1">
          <router-link to="/connections" class="group flex items-center px-2 py-2 text-sm font-medium rounded-md transition-all duration-200" active-class="bg-white bg-opacity-10 text-white shadow-inner" :class="[$route.path.includes('connections') ? '' : 'text-primary-100 hover:bg-white hover:bg-opacity-5 hover:text-white']">
            <svg class="mr-3 flex-shrink-0 h-6 w-6 text-primary-300" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
            {{ t('nav.connections') }}
          </router-link>
          <router-link to="/rules" class="group flex items-center px-2 py-2 text-sm font-medium rounded-md transition-all duration-200" active-class="bg-white bg-opacity-10 text-white shadow-inner" :class="[$route.path.includes('rules') ? '' : 'text-primary-100 hover:bg-white hover:bg-opacity-5 hover:text-white']">
            <svg class="mr-3 flex-shrink-0 h-6 w-6 text-primary-300" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
            </svg>
            {{ t('nav.rules') }}
          </router-link>
          <router-link to="/tasks" class="group flex items-center px-2 py-2 text-sm font-medium rounded-md transition-all duration-200" active-class="bg-white bg-opacity-10 text-white shadow-inner" :class="[$route.path.includes('tasks') ? '' : 'text-primary-100 hover:bg-white hover:bg-opacity-5 hover:text-white']">
            <svg class="mr-3 flex-shrink-0 h-6 w-6 text-primary-300" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {{ t('nav.tasks') }}
          </router-link>
          <router-link 
            v-if="authStore.isSuperuser || authStore.hasPermission('user:read')"
            to="/users" 
            class="group flex items-center px-2 py-2 text-sm font-medium rounded-md transition-all duration-200" 
            active-class="bg-white bg-opacity-10 text-white shadow-inner" 
            :class="[$route.path.includes('users') ? '' : 'text-primary-100 hover:bg-white hover:bg-opacity-5 hover:text-white']"
          >
            <svg class="mr-3 flex-shrink-0 h-6 w-6 text-primary-300" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            {{ t('nav.users') }}
          </router-link>
          <router-link 
            v-if="authStore.isSuperuser || authStore.hasPermission('role:manage')"
            to="/roles" 
            class="group flex items-center px-2 py-2 text-sm font-medium rounded-md transition-all duration-200" 
            active-class="bg-white bg-opacity-10 text-white shadow-inner" 
            :class="[$route.path.includes('roles') ? '' : 'text-primary-100 hover:bg-white hover:bg-opacity-5 hover:text-white']"
          >
            <svg class="mr-3 flex-shrink-0 h-6 w-6 text-primary-300" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
            {{ t('nav.roles') }}
          </router-link>
        </nav>
      </div>
      <div class="flex-shrink-0 flex border-t border-white border-opacity-10 p-4 bg-black bg-opacity-20">
        <div class="flex items-center w-full">
          <div class="flex-shrink-0">
            <span class="inline-flex items-center justify-center h-9 w-9 rounded-full bg-gradient-to-br from-primary-400 to-secondary-400 shadow-sm">
              <span class="text-sm font-medium leading-none text-white">{{ authStore.user?.username?.charAt(0).toUpperCase() || 'U' }}</span>
            </span>
          </div>
          <div class="ml-3 w-full flex justify-between items-center">
            <div class="flex flex-col">
              <p class="text-sm font-medium text-white truncate max-w-[100px]" :title="authStore.user?.username">{{ authStore.user?.username || 'User' }}</p>
              <select v-model="currentLocale" @change="changeLocale" class="mt-1 text-xs bg-white bg-opacity-10 border border-white border-opacity-20 rounded px-1 py-0.5 text-white focus:outline-none focus:ring-1 focus:ring-primary-400 w-20">
                <option value="zh-CN" class="text-gray-900">中文</option>
                <option value="en-US" class="text-gray-900">English</option>
              </select>
            </div>
            <button @click="logout" class="text-primary-200 hover:text-white transition-colors p-1 rounded-full hover:bg-white hover:bg-opacity-10" :title="t('nav.logout')">
              <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Main content -->
    <div class="flex-1 flex flex-col md:pl-64 transition-all duration-300">
      <main class="flex-1">
        <div class="py-6">
          <div class="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
            <router-view v-slot="{ Component }">
              <transition name="fade" mode="out-in">
                <component :is="Component" />
              </transition>
            </router-view>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const authStore = useAuthStore();
const { t, locale } = useI18n();
const currentLocale = ref(locale.value);

const changeLocale = () => {
  locale.value = currentLocale.value;
  localStorage.setItem('locale', currentLocale.value);
};

const logout = () => {
  authStore.logout();
  router.push('/login');
};
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
