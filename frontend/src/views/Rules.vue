<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center bg-white p-6 rounded-xl shadow-sm border border-gray-100">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">{{ t('rules.title') }}</h2>
        <p class="text-sm text-gray-500 mt-1">{{ t('rules.subtitle') }}</p>
      </div>
      <div class="flex space-x-3">
        <button @click="resetBuiltinRules" class="btn-secondary whitespace-nowrap">
          <svg class="-ml-1 mr-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd" />
          </svg>
          {{ t('common.reset') }}
        </button>
        <button @click="showAddModal = true" class="btn-primary whitespace-nowrap">
          <svg class="-ml-1 mr-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
          </svg>
          {{ t('rules.addRule') }}
        </button>
      </div>
    </div>

    <!-- Rule List -->
    <div class="bg-white shadow-sm rounded-xl border border-gray-100 overflow-hidden">
      <ul role="list" class="divide-y divide-gray-100">
        <li v-for="rule in rules" :key="rule.id" class="hover:bg-gray-50 transition-colors duration-150">
          <div class="px-6 py-5">
            <div class="flex items-center justify-between">
              <div class="flex items-start space-x-4">
                <div class="flex-shrink-0 mt-1">
                  <span :class="rule.rule_type === 'regex' ? 'bg-purple-100 text-purple-700 ring-purple-500/10' : 'bg-teal-100 text-teal-700 ring-teal-500/10'" class="inline-flex items-center justify-center px-2.5 py-0.5 rounded-md text-xs font-bold uppercase ring-1 ring-inset">
                    {{ rule.rule_type }}
                  </span>
                </div>
                <div>
                  <div class="flex items-center">
                    <p class="text-base font-semibold text-gray-900">{{ rule.name }}</p>
                    <span v-if="rule.is_system" class="ml-2 inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800">
                      {{ t('rules.system') }}
                    </span>
                  </div>
                  <div class="mt-1 font-mono text-sm text-gray-600 bg-gray-50 px-2 py-1 rounded border border-gray-200 inline-block">
                    {{ rule.content }}
                  </div>
                  <p v-if="rule.description" class="mt-1 text-sm text-gray-500">{{ rule.description }}</p>
                </div>
              </div>
              <div class="ml-4 flex-shrink-0 flex space-x-2">
                <button @click="editRule(rule)" class="text-gray-400 hover:text-blue-600 transition-colors p-2 rounded-full hover:bg-blue-50">
                  <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </button>
                <button @click="deleteRule(rule.id)" class="text-gray-400 hover:text-red-600 transition-colors p-2 rounded-full hover:bg-red-50">
                  <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </li>
        <li v-if="rules.length === 0" class="px-6 py-12 text-center text-gray-500">
          <p>{{ t('rules.emptyState') }}</p>
        </li>
      </ul>
    </div>

    <!-- Add Modal -->
    <div v-if="showAddModal" class="fixed z-20 inset-0 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-900 bg-opacity-50 transition-opacity backdrop-filter backdrop-blur-sm" aria-hidden="true" @click="showAddModal = false"></div>
        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
        <div class="inline-block align-bottom bg-white rounded-2xl px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-8">
          <div>
            <h3 class="text-xl leading-6 font-bold text-gray-900" id="modal-title">{{ editingRule ? t('common.edit') + ' ' + t('rules.name') : t('rules.addTitle') }}</h3>
            <div class="mt-6 space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('rules.name') }}</label>
                <input v-model="newRule.name" type="text" class="input-field" :placeholder="t('rules.namePlaceholder')">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('rules.ruleType') }}</label>
                <select v-model="newRule.rule_type" class="input-field">
                  <option value="regex">Regex Pattern</option>
                  <option value="keyword">Exact Keyword</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('rules.content') }}</label>
                <input v-model="newRule.content" type="text" class="input-field" :placeholder="t('rules.contentPlaceholder')">
                <p class="mt-1 text-xs text-gray-500">{{ t('rules.contentHint') }}</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('rules.description') }}</label>
                <input v-model="newRule.description" type="text" class="input-field" :placeholder="t('rules.descriptionPlaceholder')">
              </div>
            </div>
          </div>
          <div class="mt-8 sm:flex sm:flex-row-reverse">
            <button type="button" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-gradient-to-r from-primary-600 to-secondary-600 text-base font-medium text-white hover:from-primary-700 hover:to-secondary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:ml-3 sm:w-auto sm:text-sm" @click="addRule">
              {{ editingRule ? t('common.save') : t('common.add') }}
            </button>
            <button type="button" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm" @click="showAddModal = false">
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
import { useToast, useConfirm } from '../composables/useToast';
import api from '../api';

const { t } = useI18n();
const toast = useToast();
const confirm = useConfirm();

const rules = ref([]);
const showAddModal = ref(false);
const editingRule = ref(null);
const newRule = ref({
  name: '',
  rule_type: 'regex',
  content: '',
  description: ''
});

const fetchRules = async () => {
  try {
    const response = await api.get('/rules/');
    rules.value = response.data;
  } catch (e) {
    console.error(e);
  }
};

const addRule = async () => {
  try {
    if (editingRule.value) {
      // Update existing rule
      await api.put(`/rules/${editingRule.value.id}`, newRule.value);
      toast.success(t('common.success'));
    } else {
      // Create new rule
      await api.post('/rules/', newRule.value);
      toast.success(t('common.success'));
    }
    showAddModal.value = false;
    editingRule.value = null;
    newRule.value = { name: '', rule_type: 'regex', content: '', description: '' };
    fetchRules();
  } catch (e) {
    console.error(e);
    toast.error('Failed to save rule');
  }
};

const editRule = (rule) => {
  editingRule.value = rule;
  newRule.value = {
    name: rule.name,
    rule_type: rule.rule_type,
    content: rule.content,
    description: rule.description || ''
  };
  showAddModal.value = true;
};

const deleteRule = async (id) => {
  const confirmed = await confirm.show({
    title: t('common.confirm'),
    message: t('rules.deleteConfirm'),
    confirmText: t('common.delete'),
    cancelText: t('common.cancel')
  });
  if (!confirmed) return;
  try {
    await api.delete(`/rules/${id}`);
    fetchRules();
  } catch (e) {
    console.error(e);
  }
};

const resetBuiltinRules = async () => {
  const confirmed = await confirm.show({
    title: t('common.reset'),
    message: t('common.reset') + '?',
    confirmText: t('common.confirm'),
    cancelText: t('common.cancel')
  });
  if (!confirmed) return;
  try {
    await api.post('/rules/reset-builtin');
    fetchRules();
    toast.success(t('common.success'));
  } catch (e) {
    console.error(e);
    toast.error(t('common.error'));
  }
};

onMounted(fetchRules);
</script>
