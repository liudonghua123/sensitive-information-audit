<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-900">{{ t('users.title') }}</h1>
      <button @click="openCreateModal" class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
        <svg class="-ml-1 mr-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
        </svg>
        {{ t('users.add') }}
      </button>
    </div>

    <!-- Users List -->
    <div class="bg-white shadow overflow-hidden sm:rounded-md">
      <ul role="list" class="divide-y divide-gray-200">
        <li v-for="user in users" :key="user.id">
          <div class="px-4 py-4 sm:px-6">
            <div class="flex items-center justify-between">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <span class="inline-flex items-center justify-center h-10 w-10 rounded-full bg-gray-500">
                    <span class="text-sm font-medium leading-none text-white">{{ user.username.charAt(0).toUpperCase() }}</span>
                  </span>
                </div>
                <div class="ml-4">
                  <div class="text-sm font-medium text-primary-600 truncate">{{ user.username }}</div>
                  <div class="flex items-center mt-1">
                    <span v-if="user.is_superuser" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800 mr-2">
                      Superuser
                    </span>
                    <span v-for="role in user.roles" :key="role.id" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800 mr-1">
                      {{ role.name }}
                    </span>
                  </div>
                </div>
              </div>
              <div class="flex space-x-2">
                <button @click="openEditModal(user)" class="text-gray-400 hover:text-gray-500">
                  <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                  </svg>
                </button>
                <button @click="confirmDelete(user)" class="text-red-400 hover:text-red-500">
                  <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </li>
      </ul>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showModal" class="fixed z-10 inset-0 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true" @click="closeModal"></div>
        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
        <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6">
          <div>
            <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
              {{ isEditMode ? t('users.edit') : t('users.add') }}
            </h3>
            <div class="mt-4 space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700">{{ t('users.username') }}</label>
                <input type="text" v-model="formData.username" :disabled="isEditMode" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">{{ t('users.password') }}</label>
                <input type="password" v-model="formData.password" :placeholder="isEditMode ? t('users.passwordHint') : ''" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">{{ t('users.roles') }}</label>
                <div class="mt-2 space-y-2">
                  <div v-for="role in roles" :key="role.id" class="flex items-center">
                    <input :id="'role-' + role.id" type="checkbox" :value="role.id" v-model="formData.role_ids" class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded">
                    <label :for="'role-' + role.id" class="ml-2 block text-sm text-gray-900">
                      {{ role.name }}
                    </label>
                  </div>
                </div>
              </div>
              <div class="flex items-center">
                <input id="is_superuser" type="checkbox" v-model="formData.is_superuser" class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded">
                <label for="is_superuser" class="ml-2 block text-sm text-gray-900">
                  {{ t('users.isSuperuser') }}
                </label>
              </div>
            </div>
          </div>
          <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
            <button type="button" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-primary-600 text-base font-medium text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:col-start-2 sm:text-sm" @click="saveUser">
              {{ t('common.save') }}
            </button>
            <button type="button" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:mt-0 sm:col-start-1 sm:text-sm" @click="closeModal">
              {{ t('common.cancel') }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useI18n } from 'vue-i18n';
import api from '../api';

const { t } = useI18n();
const users = ref([]);
const roles = ref([]);
const showModal = ref(false);
const isEditMode = ref(false);
const formData = ref({
  id: null,
  username: '',
  password: '',
  role_ids: [],
  is_superuser: false
});

const fetchUsers = async () => {
  try {
    const response = await api.get('/users/');
    users.value = response.data;
  } catch (e) {
    console.error(e);
  }
};

const fetchRoles = async () => {
  try {
    const response = await api.get('/roles/');
    roles.value = response.data;
  } catch (e) {
    console.error(e);
  }
};

const openCreateModal = () => {
  isEditMode.value = false;
  formData.value = {
    id: null,
    username: '',
    password: '',
    role_ids: [],
    is_superuser: false
  };
  showModal.value = true;
};

const openEditModal = (user) => {
  isEditMode.value = true;
  formData.value = {
    id: user.id,
    username: user.username,
    password: '', // Don't show password
    role_ids: user.roles.map(r => r.id),
    is_superuser: user.is_superuser
  };
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

const saveUser = async () => {
  try {
    if (isEditMode.value) {
      await api.put(`/users/${formData.value.id}`, formData.value);
    } else {
      await api.post('/users/', formData.value);
    }
    closeModal();
    fetchUsers();
  } catch (e) {
    console.error(e);
    alert(t('common.error'));
  }
};

const confirmDelete = async (user) => {
  if (confirm(t('common.confirmDelete'))) {
    try {
      await api.delete(`/users/${user.id}`);
      fetchUsers();
    } catch (e) {
      console.error(e);
      alert(t('common.error'));
    }
  }
};

onMounted(() => {
  fetchUsers();
  fetchRoles();
});
</script>
