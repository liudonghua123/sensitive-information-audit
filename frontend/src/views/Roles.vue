<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-900">{{ t('roles.title') }}</h1>
      <button @click="openCreateModal" class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
        <svg class="-ml-1 mr-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
        </svg>
        {{ t('roles.add') }}
      </button>
    </div>

    <!-- Roles List -->
    <div class="bg-white shadow overflow-hidden sm:rounded-md">
      <ul role="list" class="divide-y divide-gray-200">
        <li v-for="role in roles" :key="role.id">
          <div class="px-4 py-4 sm:px-6">
            <div class="flex items-center justify-between">
              <div class="flex-1">
                <div class="flex items-center justify-between">
                  <div class="text-sm font-medium text-primary-600 truncate">{{ role.name }}</div>
                  <div class="ml-2 flex-shrink-0 flex">
                    <button @click="openEditModal(role)" class="mr-2 text-gray-400 hover:text-gray-500">
                      <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                      </svg>
                    </button>
                    <!-- Disable deleting Admin and User roles for safety -->
                    <button v-if="!['Admin', 'User'].includes(role.name)" @click="confirmDelete(role)" class="text-red-400 hover:text-red-500">
                      <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                      </svg>
                    </button>
                  </div>
                </div>
                <div class="mt-2 text-sm text-gray-500">
                  {{ role.description }}
                </div>
                <div class="mt-2">
                  <span v-for="permission in role.permissions" :key="permission.id" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800 mr-1 mb-1">
                    {{ permission.name }}
                  </span>
                </div>
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
              {{ isEditMode ? t('roles.edit') : t('roles.add') }}
            </h3>
            <div class="mt-4 space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700">{{ t('roles.name') }}</label>
                <input type="text" v-model="formData.name" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">{{ t('roles.description') }}</label>
                <input type="text" v-model="formData.description" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">{{ t('roles.permissions') }}</label>
                <div class="mt-2 h-60 overflow-y-auto border border-gray-200 rounded-md p-2">
                  <div v-for="permission in permissions" :key="permission.id" class="flex items-start mb-2">
                    <div class="flex items-center h-5">
                      <input :id="'perm-' + permission.id" type="checkbox" :value="permission.id" v-model="formData.permission_ids" class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded">
                    </div>
                    <div class="ml-3 text-sm">
                      <label :for="'perm-' + permission.id" class="font-medium text-gray-700">{{ permission.name }}</label>
                      <p class="text-gray-500">{{ permission.description }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
            <button type="button" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-primary-600 text-base font-medium text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:col-start-2 sm:text-sm" @click="saveRole">
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
const roles = ref([]);
const permissions = ref([]);
const showModal = ref(false);
const isEditMode = ref(false);
const formData = ref({
  id: null,
  name: '',
  description: '',
  permission_ids: []
});

const fetchRoles = async () => {
  try {
    const response = await api.get('/roles/');
    roles.value = response.data;
  } catch (e) {
    console.error(e);
  }
};

const fetchPermissions = async () => {
  try {
    const response = await api.get('/roles/permissions');
    permissions.value = response.data;
  } catch (e) {
    console.error(e);
  }
};

const openCreateModal = () => {
  isEditMode.value = false;
  formData.value = {
    id: null,
    name: '',
    description: '',
    permission_ids: []
  };
  showModal.value = true;
};

const openEditModal = (role) => {
  isEditMode.value = true;
  formData.value = {
    id: role.id,
    name: role.name,
    description: role.description,
    permission_ids: role.permissions.map(p => p.id)
  };
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

const saveRole = async () => {
  try {
    // Note: Backend endpoint for creating/updating roles needs to be implemented or verified
    // Currently only GET /roles/ is implemented in roles.py
    // We need to add POST /roles/ and PUT /roles/{id}
    
    if (isEditMode.value) {
      await api.put(`/roles/${formData.value.id}`, formData.value);
    } else {
      await api.post('/roles/', formData.value);
    }
    closeModal();
    fetchRoles();
  } catch (e) {
    console.error(e);
    alert(t('common.error'));
  }
};

const confirmDelete = async (role) => {
  if (confirm(t('common.confirmDelete'))) {
    try {
      await api.delete(`/roles/${role.id}`);
      fetchRoles();
    } catch (e) {
      console.error(e);
      alert(t('common.error'));
    }
  }
};

onMounted(() => {
  fetchRoles();
  fetchPermissions();
});
</script>
