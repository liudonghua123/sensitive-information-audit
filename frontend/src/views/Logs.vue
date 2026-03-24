<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center bg-white p-6 rounded-xl shadow-sm border border-gray-100">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">{{ $t('logs.title') }}</h2>
        <p class="text-sm text-gray-500 mt-1">{{ $t('logs.subtitle') }}</p>
      </div>
      <button @click="fetchLogs" class="btn-secondary">
        <svg class="-ml-1 mr-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd" />
        </svg>
        {{ $t('common.refresh') }}
      </button>
    </div>

    <!-- Filters -->
    <div class="bg-white shadow-sm rounded-xl border border-gray-100 p-4">
      <div class="flex flex-wrap gap-4">
        <div>
          <label class="block text-xs font-medium text-gray-500 mb-1">{{ $t('logs.level') }}</label>
          <select v-model="filters.level" @change="fetchLogs" class="input-field text-sm">
            <option value="">All Levels</option>
            <option value="info">Info</option>
            <option value="warning">Warning</option>
            <option value="error">Error</option>
            <option value="debug">Debug</option>
          </select>
        </div>
        <div>
          <label class="block text-xs font-medium text-gray-500 mb-1">{{ $t('logs.action') }}</label>
          <select v-model="filters.action" @change="fetchLogs" class="input-field text-sm">
            <option value="">All Actions</option>
            <option v-for="action in availableActions" :key="action" :value="action">{{ action }}</option>
          </select>
        </div>
        <div>
          <label class="block text-xs font-medium text-gray-500 mb-1">{{ $t('logs.user') }}</label>
          <input
            type="text"
            v-model.number="filters.user_id"
            @change="fetchLogs"
            placeholder="User ID"
            class="input-field text-sm"
          />
        </div>
        <div class="flex items-end">
          <button @click="clearFilters" class="text-sm text-gray-500 hover:text-gray-700">
            Clear Filters
          </button>
        </div>
      </div>
    </div>

    <!-- Logs Table -->
    <div class="bg-white shadow-sm rounded-xl border border-gray-100 overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th scope="col" class="px-6 py-3 text-left text-xs font-semibold text-gray-700 uppercase">{{ $t('logs.time') }}</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-semibold text-gray-700 uppercase">{{ $t('logs.level') }}</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-semibold text-gray-700 uppercase">{{ $t('logs.action') }}</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-semibold text-gray-700 uppercase">{{ $t('logs.user') }}</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-semibold text-gray-700 uppercase">{{ $t('logs.message') }}</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-semibold text-gray-700 uppercase">{{ $t('logs.details') }}</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-100">
          <tr v-for="log in logs" :key="log.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ formatDate(log.created_at) }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span :class="getLevelClass(log.level)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                {{ log.level }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
              {{ log.action }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ log.username || log.user_id || '-' }}
            </td>
            <td class="px-6 py-4 text-sm text-gray-600 max-w-md truncate">
              {{ log.message }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <button
                v-if="log.details"
                @click="viewDetails(log)"
                class="text-primary-600 hover:text-primary-700 text-sm font-medium"
              >
                View
              </button>
              <span v-else class="text-gray-400 text-sm">-</span>
            </td>
          </tr>
          <tr v-if="logs.length === 0">
            <td colspan="6" class="px-6 py-12 text-center text-gray-500">
              No logs found
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
    <div class="flex justify-between items-center">
      <div class="text-sm text-gray-500">
        Showing {{ logs.length }} logs
      </div>
      <div class="flex space-x-2">
        <button
          @click="changePage(-1)"
          :disabled="skip === 0"
          class="px-3 py-1 border border-gray-300 rounded text-sm disabled:opacity-50"
        >
          Previous
        </button>
        <button
          @click="changePage(1)"
          :disabled="logs.length < limit"
          class="px-3 py-1 border border-gray-300 rounded text-sm disabled:opacity-50"
        >
          Next
        </button>
      </div>
    </div>

    <!-- Details Modal -->
    <div v-if="showDetailsModal" class="fixed z-20 inset-0 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-900 bg-opacity-50 transition-opacity backdrop-filter backdrop-blur-sm" aria-hidden="true" @click="showDetailsModal = false"></div>
        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
        <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full sm:p-6">
          <div>
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">Log Details</h3>
            <div class="bg-gray-50 p-4 rounded border border-gray-200 font-mono text-sm max-h-96 overflow-y-auto">
              <pre>{{ selectedLog.details }}</pre>
            </div>
          </div>
          <div class="mt-5 sm:mt-6">
            <button type="button" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-primary-600 text-base font-medium text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:text-sm" @click="showDetailsModal = false">
              {{ $t('common.close') }}
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

const logs = ref([]);
const availableActions = ref([]);
const filters = ref({
  level: '',
  action: '',
  user_id: null,
});
const skip = ref(0);
const limit = ref(50);
const showDetailsModal = ref(false);
const selectedLog = ref(null);

const fetchLogs = async () => {
  try {
    const params = {
      skip: skip.value,
      limit: limit.value,
    };
    if (filters.value.level) params.level = filters.value.level;
    if (filters.value.action) params.action = filters.value.action;
    if (filters.value.user_id) params.user_id = filters.value.user_id;

    const response = await api.get('/logs/', { params });
    logs.value = response.data;
  } catch (e) {
    console.error('Failed to fetch logs:', e);
  }
};

const fetchActions = async () => {
  try {
    const response = await api.get('/logs/actions');
    availableActions.value = response.data;
  } catch (e) {
    console.error('Failed to fetch actions:', e);
  }
};

const clearFilters = () => {
  filters.value = {
    level: '',
    action: '',
    user_id: null,
  };
  skip.value = 0;
  fetchLogs();
};

const changePage = (delta) => {
  skip.value = Math.max(0, skip.value + delta * limit.value);
  fetchLogs();
};

const viewDetails = (log) => {
  selectedLog.value = log;
  showDetailsModal.value = true;
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  return new Date(dateString).toLocaleString();
};

const getLevelClass = (level) => {
  switch (level) {
    case 'info': return 'bg-blue-100 text-blue-800';
    case 'warning': return 'bg-yellow-100 text-yellow-800';
    case 'error': return 'bg-red-100 text-red-800';
    case 'debug': return 'bg-gray-100 text-gray-800';
    default: return 'bg-gray-100 text-gray-800';
  }
};

onMounted(() => {
  fetchLogs();
  fetchActions();
});
</script>