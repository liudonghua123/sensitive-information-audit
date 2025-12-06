<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center bg-white p-6 rounded-xl shadow-sm border border-gray-100">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">{{ t('connections.title') }}</h2>
        <p class="text-sm text-gray-500 mt-1">{{ t('connections.subtitle') }}</p>
      </div>
      <button @click="openAddModal" class="btn-primary whitespace-nowrap">
        <svg class="-ml-1 mr-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
        </svg>
        {{ t('connections.addConnection') }}
      </button>
    </div>

    <!-- Connection Grid -->
    <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <div v-for="conn in connections" :key="conn.id" class="bg-white overflow-hidden shadow-sm rounded-xl border border-gray-100 hover:shadow-md transition-shadow duration-200">
        <div class="px-6 py-5">
          <div class="flex items-center">
            <div class="flex-shrink-0 bg-gradient-to-br from-primary-100 to-secondary-100 rounded-lg p-3">
              <svg v-if="conn.db_type === 'sqlite'" class="h-8 w-8 text-primary-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" />
              </svg>
              <svg v-else class="h-8 w-8 text-secondary-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2m-2-4h.01M17 16h.01" />
              </svg>
            </div>
            <div class="ml-4 flex-1">
              <h3 class="text-lg font-medium text-gray-900 truncate">{{ conn.name }}</h3>
              <p class="text-sm text-gray-500 uppercase tracking-wider font-bold text-xs mt-1">{{ conn.db_type }}</p>
            </div>
            <div class="ml-2 flex space-x-1">
               <button @click="openEditModal(conn)" class="text-gray-400 hover:text-primary-500 transition-colors p-2" :title="t('common.edit')">
                 <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                   <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                 </svg>
               </button>
               <button @click="deleteConnection(conn.id)" class="text-gray-400 hover:text-red-500 transition-colors p-2" :title="t('common.delete')">
                 <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                   <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                 </svg>
               </button>
            </div>
          </div>
        </div>
        <div class="bg-gray-50 px-6 py-3 border-t border-gray-100">
          <div class="flex items-center justify-between">
            <div class="text-xs text-gray-500 flex items-center truncate flex-1">
              <span class="truncate">{{ conn.host }}:{{ conn.port }}</span>
              <span class="mx-2">•</span>
              <span class="truncate font-medium">{{ conn.db_name }}</span>
            </div>
            <button @click="viewMetadata(conn)" class="ml-2 text-xs text-primary-600 hover:text-primary-700 font-medium whitespace-nowrap">
              {{ t('connections.viewMetadata') }}
            </button>
          </div>
        </div>
      </div>
      
      <!-- Empty State -->
      <div v-if="connections.length === 0" class="col-span-full flex flex-col items-center justify-center p-12 bg-white rounded-xl border-2 border-dashed border-gray-300 text-gray-500">
        <svg class="h-12 w-12 text-gray-400 mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v3m0 0v3m0-3h3m-3 0H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <p class="text-lg font-medium">{{ t('connections.emptyState') }}</p>
        <p class="text-sm mt-1">{{ t('connections.emptyStateDesc') }}</p>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showModal" class="fixed z-20 inset-0 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-900 bg-opacity-50 transition-opacity backdrop-filter backdrop-blur-sm" aria-hidden="true" @click="closeModal"></div>
        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
        <div class="inline-block align-bottom bg-white rounded-2xl px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-8">
          <div>
            <h3 class="text-xl leading-6 font-bold text-gray-900" id="modal-title">
              {{ isEditMode ? t('connections.editTitle') : t('connections.addTitle') }}
            </h3>
            <div class="mt-6 space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('connections.name') }}</label>
                <input v-model="formData.name" type="text" class="input-field" :placeholder="t('connections.namePlaceholder')">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('connections.dbType') }}</label>
                <select v-model="formData.db_type" class="input-field">
                  <option value="sqlite">SQLite</option>
                  <option value="mysql">MySQL</option>
                  <option value="postgresql">PostgreSQL</option>
                  <option value="oracle">Oracle</option>
                </select>
              </div>
              <div class="grid grid-cols-2 gap-4">
                <div class="col-span-2">
                  <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('connections.host') }}</label>
                  <input v-model="formData.host" type="text" class="input-field" :placeholder="t('connections.hostPlaceholder')">
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('connections.port') }}</label>
                  <input v-model="formData.port" type="number" class="input-field" :placeholder="t('connections.portPlaceholder')">
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('connections.dbName') }}</label>
                  <input v-model="formData.db_name" type="text" class="input-field" :placeholder="t('connections.dbNamePlaceholder')">
                </div>
              </div>
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('connections.username') }}</label>
                  <input v-model="formData.username" type="text" class="input-field" :placeholder="t('connections.usernamePlaceholder')">
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('connections.password') }}</label>
                  <input v-model="formData.password" type="password" class="input-field" :placeholder="isEditMode ? '••••••' : t('connections.passwordPlaceholder')">
                </div>
              </div>
              
              <!-- Test Result -->
              <div v-if="testResult" :class="testResult.success ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'" class="rounded-md p-4 border">
                <div class="flex">
                  <div class="flex-shrink-0">
                    <svg v-if="testResult.success" class="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                    </svg>
                    <svg v-else class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                    </svg>
                  </div>
                  <div class="ml-3">
                    <h3 :class="testResult.success ? 'text-green-800' : 'text-red-800'" class="text-sm font-medium">{{ testResult.message }}</h3>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="mt-8 sm:flex sm:flex-row-reverse">
            <button 
              type="button" 
              :disabled="!canSaveConnection"
              :class="canSaveConnection ? 'bg-gradient-to-r from-primary-600 to-secondary-600 hover:from-primary-700 hover:to-secondary-700' : 'bg-gray-300 cursor-not-allowed'"
              class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 text-base font-medium text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:ml-3 sm:w-auto sm:text-sm" 
              @click="saveConnection"
            >
              {{ isEditMode ? t('common.save') : t('common.add') }}
            </button>
            <button 
              type="button" 
              :disabled="testing || !canSaveConnection"
              :class="(testing || !canSaveConnection) ? 'bg-gray-300 cursor-not-allowed' : 'bg-white text-primary-700 hover:bg-primary-50'"
              class="mt-3 w-full inline-flex justify-center rounded-md border border-primary-300 shadow-sm px-4 py-2 text-base font-medium focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm" 
              @click="testConnectionHandler"
            >
              {{ testing ? t('common.testing') : t('common.test') }}
            </button>
            <button type="button" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm" @click="closeModal">
              {{ t('common.cancel') }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Metadata Modal -->
    <div v-if="showMetadataModal" class="fixed z-20 inset-0 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-900 bg-opacity-50 transition-opacity backdrop-filter backdrop-blur-sm" aria-hidden="true" @click="showMetadataModal = false"></div>
        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
        <div class="inline-block align-bottom bg-white rounded-2xl px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-4xl sm:w-full sm:p-8">
          <div>
            <div class="flex justify-between items-center mb-6">
              <h3 class="text-xl leading-6 font-bold text-gray-900">{{ t('connections.metadataTitle') }}: {{ currentConnection?.name }}</h3>
              <div class="flex items-center space-x-2">
                <input 
                  type="text" 
                  v-model="metadataSearchQuery" 
                  placeholder="Search tables..." 
                  class="text-xs border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-1 focus:ring-primary-500"
                />
                <button @click="refreshMetadata" class="text-gray-400 hover:text-primary-600" :title="t('common.refresh')">
                  <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                </button>
                <button @click="showMetadataModal = false" class="text-gray-400 hover:text-gray-500">
                  <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
            
            <div v-if="loadingMetadata" class="text-center py-12">
              <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
              <p class="mt-2 text-sm text-gray-500">{{ t('connections.loadingMetadata') }}</p>
            </div>

            <div v-else-if="metadata && metadata.tables.length > 0" class="border border-gray-200 rounded-lg p-4 max-h-96 overflow-y-auto">
              <div class="space-y-2">
                <div v-for="table in filteredMetadataTables" :key="table.name" class="border border-gray-100 rounded-lg overflow-hidden">
                  <div class="flex items-center p-3 bg-gray-50 hover:bg-gray-100 transition-colors cursor-pointer" @click="toggleMetadataExpand(table.name)">
                    <div class="flex-1">
                      <div class="flex items-center justify-between">
                        <div class="flex items-center space-x-2">
                          <svg class="h-4 w-4 text-gray-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M5 4a3 3 0 00-3 3v6a3 3 0 003 3h10a3 3 0 003-3V7a3 3 0 00-3-3H5zm-1 9v-1h5v2H5a1 1 0 01-1-1zm7 1h4a1 1 0 001-1v-1h-5v2zm0-4h5V8h-5v2zM9 8H4v2h5V8z" clip-rule="evenodd" />
                          </svg>
                          <span class="text-sm font-medium text-gray-900">{{ table.name }}</span>
                          <span class="text-xs text-gray-500">({{ table.type }})</span>
                        </div>
                        <div class="flex items-center space-x-4 text-xs text-gray-500">
                          <span v-if="table.row_count !== null">{{ t('tasks.rows') }}: {{ formatNumber(table.row_count) }}</span>
                          <span v-if="table.size_bytes !== null">{{ t('tasks.size') }}: {{ formatBytes(table.size_bytes) }}</span>
                          <span class="text-primary-600">{{ expandedMetadataTables.includes(table.name) ? '▼' : '▶' }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  <!-- Columns -->
                  <div v-if="expandedMetadataTables.includes(table.name)" class="bg-white p-3 border-t border-gray-100">
                    <div class="text-xs font-semibold text-gray-600 mb-2">{{ t('tasks.columns') }}:</div>
                    <div class="grid grid-cols-2 gap-2">
                      <div v-for="col in table.columns" :key="col.name" class="flex items-center space-x-2 text-xs">
                        <span class="font-mono text-gray-700">{{ col.name }}</span>
                        <span class="text-gray-400">{{ col.type }}</span>
                        <span v-if="col.nullable" class="text-gray-400">(nullable)</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div v-else class="text-center py-12 text-gray-500">
              <p>{{ t('connections.noMetadata') }}</p>
            </div>
          </div>
          <div class="mt-8 sm:flex sm:flex-row-reverse">
            <button type="button" class="w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:w-auto sm:text-sm" @click="showMetadataModal = false">
              {{ t('common.close') }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { useToast, useConfirm } from '../composables/useToast';
import api from '../api';

const { t } = useI18n();
const toast = useToast();
const confirm = useConfirm();

const connections = ref([]);
const showModal = ref(false);
const showMetadataModal = ref(false);
const testing = ref(false);
const testResult = ref(null);
const isEditMode = ref(false);
const editingId = ref(null);
const metadata = ref(null);
const loadingMetadata = ref(false);
const currentConnection = ref(null);
const expandedMetadataTables = ref([]);
const metadataSearchQuery = ref('');
const metadataCache = ref({});

const canSaveConnection = computed(() => {
  if (!formData.value.name || !formData.value.db_type) return false;
  
  // For non-SQLite databases, require host and db_name
  if (formData.value.db_type !== 'sqlite') {
    if (!formData.value.host || !formData.value.db_name) return false;
  } else {
    // For SQLite, require host (file path)
    if (!formData.value.host) return false;
  }
  
  return true;
});

const formData = ref({
  name: '',
  db_type: 'sqlite',
  host: '',
  port: null,
  username: '',
  password: '',
  db_name: ''
});

// Default ports for each DB type
const defaultPorts = {
  mysql: 3306,
  postgresql: 5432,
  oracle: 1521,
  sqlite: null
};

// Watch for db_type changes to update port
watch(() => formData.value.db_type, (newType, oldType) => {
  // Only update if port is empty or matches the default of the previous type
  const oldDefault = defaultPorts[oldType];
  if (!formData.value.port || formData.value.port == oldDefault) {
    formData.value.port = defaultPorts[newType];
  }
});

const filteredMetadataTables = computed(() => {
  if (!metadata.value || !metadata.value.tables) return [];
  if (!metadataSearchQuery.value) return metadata.value.tables;
  const query = metadataSearchQuery.value.toLowerCase();
  return metadata.value.tables.filter(t => t.name.toLowerCase().includes(query));
});

const fetchConnections = async () => {
  try {
    const response = await api.get('/connections/');
    connections.value = response.data;
  } catch (e) {
    console.error(e);
  }
};

const openAddModal = () => {
  isEditMode.value = false;
  editingId.value = null;
  formData.value = { name: '', db_type: 'sqlite', host: '', port: null, username: '', password: '', db_name: '' };
  testResult.value = null;
  showModal.value = true;
};

const openEditModal = (conn) => {
  isEditMode.value = true;
  editingId.value = conn.id;
  formData.value = {
    name: conn.name,
    db_type: conn.db_type,
    host: conn.host || '',
    port: conn.port,
    username: conn.username || '',
    password: '', // Don't populate password
    db_name: conn.db_name || ''
  };
  testResult.value = null;
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  testResult.value = null;
};

const testConnectionHandler = async () => {
  testing.value = true;
  testResult.value = null;
  try {
    const payload = { ...formData.value };
    if (isEditMode.value && editingId.value) {
      payload.id = editingId.value;
    }
    const response = await api.post('/connections/test', payload);
    testResult.value = { success: true, message: t('connections.testSuccess') };
  } catch (e) {
    const errorMsg = e.response?.data?.detail || e.message;
    testResult.value = { success: false, message: t('connections.testFailed', { error: errorMsg }) };
  } finally {
    testing.value = false;
  }
};

const saveConnection = async () => {
  if (!canSaveConnection.value) {
    toast.error(t('connections.requiredFields'));
    return;
  }
  try {
    if (isEditMode.value) {
      await api.put(`/connections/${editingId.value}`, formData.value);
      toast.success(t('common.success'));
    } else {
      await api.post('/connections/', formData.value);
      toast.success(t('common.success'));
    }
    closeModal();
    fetchConnections();
  } catch (e) {
    console.error(e);
    const errorMsg = e.response?.data?.detail || e.message;
    toast.error(errorMsg);
  }
};

const deleteConnection = async (id) => {
  const confirmed = await confirm.show({
    title: t('common.confirm'),
    message: t('connections.deleteConfirm'),
    confirmText: t('common.delete'),
    cancelText: t('common.cancel')
  });
  if (!confirmed) return;
  try {
    await api.delete(`/connections/${id}`);
    fetchConnections();
    toast.success(t('common.success'));
    // Clear cache for this connection
    delete metadataCache.value[id];
  } catch (e) {
    console.error(e);
    toast.error(e.response?.data?.detail || e.message);
  }
};

const viewMetadata = async (conn, forceRefresh = false) => {
  currentConnection.value = conn;
  showMetadataModal.value = true;
  expandedMetadataTables.value = [];
  metadataSearchQuery.value = '';
  
  // Check cache first
  if (!forceRefresh && metadataCache.value[conn.id]) {
    metadata.value = metadataCache.value[conn.id];
    return;
  }

  loadingMetadata.value = true;
  metadata.value = null;
  
  try {
    const response = await api.get(`/tasks/metadata/${conn.id}`);
    metadata.value = response.data;
    // Update cache
    metadataCache.value[conn.id] = response.data;
  } catch (e) {
    console.error('Failed to load metadata:', e);
    toast.error(t('connections.metadataError'));
    metadata.value = null;
  } finally {
    loadingMetadata.value = false;
  }
};

const refreshMetadata = () => {
  if (currentConnection.value) {
    viewMetadata(currentConnection.value, true);
  }
};

const toggleMetadataExpand = (tableName) => {
  const index = expandedMetadataTables.value.indexOf(tableName);
  if (index > -1) {
    expandedMetadataTables.value.splice(index, 1);
  } else {
    expandedMetadataTables.value.push(tableName);
  }
};

const formatNumber = (num) => {
  if (num === null || num === undefined) return '-';
  return num.toLocaleString();
};

const formatBytes = (bytes) => {
  if (bytes === null || bytes === undefined) return '-';
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

onMounted(fetchConnections);
</script>
