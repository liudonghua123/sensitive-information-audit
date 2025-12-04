<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center bg-white p-6 rounded-xl shadow-sm border border-gray-100">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">{{ $t('tasks.title') }}</h2>
        <p class="text-sm text-gray-500 mt-1">{{ $t('tasks.subtitle') }}</p>
      </div>
      <button @click="showCreateModal = true" class="btn-primary">
        <svg class="-ml-1 mr-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v2H7a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2V7z" clip-rule="evenodd" />
        </svg>
        {{ $t('tasks.newScan') }}
      </button>
    </div>

    <!-- Task List -->
    <div class="bg-white shadow-sm rounded-xl border border-gray-100 overflow-hidden">
      <ul role="list" class="divide-y divide-gray-100">
        <li v-for="task in tasks" :key="task.id" class="hover:bg-gray-50 transition-colors duration-150 cursor-pointer" @click="viewResults(task)">
          <div class="px-6 py-5">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-4">
                <div class="flex-shrink-0">
                  <span :class="getStatusClass(task.status)" class="inline-flex items-center justify-center h-10 w-10 rounded-full ring-2 ring-white shadow-sm">
                    <svg v-if="task.status === 'completed'" class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                    <svg v-else-if="task.status === 'running'" class="h-6 w-6 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                    <svg v-else-if="task.status === 'failed'" class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                    <svg v-else class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </span>
                </div>
                <div>
                  <div class="flex items-center">
                    <p class="text-sm font-bold text-gray-900">{{ $t('tasks.taskId') }} #{{ task.id }}</p>
                    <span class="mx-2 text-gray-300">|</span>
                    <p class="text-sm text-gray-600">{{ $t('tasks.connectionId') }}: {{ task.connection_id }}</p>
                  </div>
                  <div class="flex items-center mt-1 text-xs text-gray-500">
                    <svg class="flex-shrink-0 mr-1.5 h-4 w-4 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd" />
                    </svg>
                    {{ $t('tasks.started') }}: {{ formatDate(task.start_time) }}
                  </div>
                </div>
              </div>
              <div class="flex items-center">
                <div v-if="task.end_time" class="text-right mr-4">
                   <p class="text-xs text-gray-500">{{ $t('tasks.duration') }}</p>
                   <p class="text-sm font-medium text-gray-900">{{ calculateDuration(task.start_time, task.end_time) }}</p>
                </div>
                <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                </svg>
              </div>
            </div>
            
            <!-- Actions -->
            <div class="mt-4 flex justify-end space-x-3 border-t border-gray-100 pt-3" @click.stop>
              <button @click="exportTask(task, 'docx')" class="inline-flex items-center px-2.5 py-1.5 border border-gray-300 shadow-sm text-xs font-medium rounded text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
                <svg class="-ml-0.5 mr-2 h-4 w-4 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                DOCX
              </button>
              <button @click="exportTask(task, 'pdf')" class="inline-flex items-center px-2.5 py-1.5 border border-gray-300 shadow-sm text-xs font-medium rounded text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
                <svg class="-ml-0.5 mr-2 h-4 w-4 text-red-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                </svg>
                PDF
              </button>
              <button @click="deleteTask(task)" class="inline-flex items-center px-2.5 py-1.5 border border-transparent shadow-sm text-xs font-medium rounded text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500">
                <svg class="-ml-0.5 mr-2 h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
                Delete
              </button>
            </div>

            <div v-if="task.summary" class="mt-3 text-sm text-red-600 bg-red-50 p-2 rounded border border-red-100">
              {{ $t('common.error') }}: {{ task.summary }}
            </div>
            <div v-if="task.selected_rules && parseRulesUsed(task.selected_rules).length > 0" class="mt-3">
              <div class="text-xs font-semibold text-gray-600 mb-1">{{ $t('tasks.summary.rulesUsed') }}:</div>
              <div class="flex flex-wrap gap-1">
                <span v-for="ruleId in parseRulesUsed(task.selected_rules)" :key="ruleId" class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800">
                  {{ getRuleName(ruleId) }}
                </span>
              </div>
            </div>
          </div>
        </li>
        <li v-if="tasks.length === 0" class="px-6 py-12 text-center text-gray-500">
          <p>{{ $t('tasks.emptyState') }}</p>
        </li>
      </ul>
    </div>

    <!-- Create Task Modal -->
    <div v-if="showCreateModal" class="fixed z-20 inset-0 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-900 bg-opacity-50 transition-opacity backdrop-filter backdrop-blur-sm" aria-hidden="true" @click="closeCreateModal"></div>
        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
        <div class="inline-block align-bottom bg-white rounded-2xl px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-4xl sm:w-full sm:p-8">
          <div>
            <h3 class="text-xl leading-6 font-bold text-gray-900" id="modal-title">{{ $t('tasks.startScan') }}</h3>
            <div class="mt-6 space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('tasks.selectDatabase') }}</label>
                <select v-model="selectedConnectionId" @change="loadMetadata" class="input-field">
                  <option :value="null">------</option>
                  <option v-for="conn in connections" :key="conn.id" :value="conn.id">
                    {{ conn.name }} ({{ conn.db_type }})
                  </option>
                </select>
              </div>

              <!-- Loading State -->
              <div v-if="loadingMetadata" class="text-center py-8">
                <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
                <p class="mt-2 text-sm text-gray-500">{{ $t('connections.loadingMetadata') }}</p>
              </div>

              <!-- Database Metadata Tree -->
              <div v-else-if="metadata && metadata.tables.length > 0" class="border border-gray-200 rounded-lg p-4 max-h-96 overflow-y-auto">
                <div class="flex items-center justify-between mb-3">
                  <h4 class="text-sm font-semibold text-gray-700">{{ $t('tasks.selectTables') }}</h4>
                  <div class="flex items-center space-x-2">
                    <input 
                      type="text" 
                      v-model="tableSearchQuery" 
                      placeholder="Search tables..." 
                      class="text-xs border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-1 focus:ring-primary-500"
                    />
                    <button @click="toggleSelectAll" class="text-xs text-primary-600 hover:text-primary-700">
                      {{ allTablesSelected ? $t('tasks.deselectAll') : $t('tasks.selectAll') }}
                    </button>
                  </div>
                </div>
                <div class="space-y-2">
                  <div v-for="table in filteredTables" :key="table.name" class="border border-gray-100 rounded-lg overflow-hidden">
                    <div class="flex items-center p-3 bg-gray-50 hover:bg-gray-100 transition-colors">
                      <input 
                        type="checkbox" 
                        :id="'table-' + table.name" 
                        v-model="selectedTables"
                        :value="table.name"
                        class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                      />
                      <label :for="'table-' + table.name" class="ml-3 flex-1 cursor-pointer">
                        <div class="flex items-center justify-between">
                          <div class="flex items-center space-x-2">
                            <svg class="h-4 w-4 text-gray-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                              <path fill-rule="evenodd" d="M5 4a3 3 0 00-3 3v6a3 3 0 003 3h10a3 3 0 003-3V7a3 3 0 00-3-3H5zm-1 9v-1h5v2H5a1 1 0 01-1-1zm7 1h4a1 1 0 001-1v-1h-5v2zm0-4h5V8h-5v2zM9 8H4v2h5V8z" clip-rule="evenodd" />
                            </svg>
                            <span class="text-sm font-medium text-gray-900">{{ table.name }}</span>
                            <span class="text-xs text-gray-500">({{ table.type }})</span>
                          </div>
                          <div class="flex items-center space-x-4 text-xs text-gray-500">
                            <span v-if="table.row_count !== null">{{ $t('tasks.rows') }}: {{ formatNumber(table.row_count) }}</span>
                            <span v-if="table.size_bytes !== null">{{ $t('tasks.size') }}: {{ formatBytes(table.size_bytes) }}</span>
                            <button @click.prevent="toggleTableExpand(table.name)" class="text-primary-600 hover:text-primary-700">
                              {{ expandedTables.includes(table.name) ? '▼' : '▶' }}
                            </button>
                          </div>
                        </div>
                      </label>
                    </div>
                    <!-- Columns -->
                    <div v-if="expandedTables.includes(table.name)" class="bg-white p-3 border-t border-gray-100">
                      <div class="text-xs font-semibold text-gray-600 mb-2">{{ $t('tasks.columns') }}:</div>
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

              <!-- Rule Selection -->
              <div v-if="rules.length > 0" class="border border-gray-200 rounded-lg p-4">
                <div class="flex items-center justify-between mb-3">
                  <h4 class="text-sm font-semibold text-gray-700">{{ $t('tasks.selectRules') }}</h4>
                  <button @click="toggleSelectAllRules" class="text-xs text-primary-600 hover:text-primary-700">
                    {{ allRulesSelected ? $t('tasks.deselectAll') : $t('tasks.selectAll') }}
                  </button>
                </div>
                <div class="space-y-2 max-h-48 overflow-y-auto">
                  <div v-for="rule in rules" :key="rule.id" class="flex items-center">
                    <input 
                      type="checkbox" 
                      :id="'rule-' + rule.id" 
                      v-model="selectedRules"
                      :value="rule.id"
                      class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                    />
                    <label :for="'rule-' + rule.id" class="ml-3 flex-1 cursor-pointer">
                      <div class="flex items-center justify-between">
                        <div class="flex items-center space-x-2">
                          <span class="text-sm font-medium text-gray-900">{{ rule.name }}</span>
                          <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium" :class="rule.rule_type === 'regex' ? 'bg-purple-100 text-purple-800' : 'bg-green-100 text-green-800'">
                            {{ rule.rule_type }}
                          </span>
                        </div>
                      </div>
                    </label>
                  </div>
                </div>
                <p class="text-xs text-gray-500 mt-2">{{ $t('tasks.rulesHint') }}</p>
              </div>

              <p class="text-xs text-gray-500">{{ $t('tasks.scanHint') }}</p>
            </div>
          </div>
          <div class="mt-8 sm:flex sm:flex-row-reverse">
            <button 
              type="button" 
              :disabled="!canCreateScan"
              :class="canCreateScan ? 'bg-gradient-to-r from-primary-600 to-secondary-600 hover:from-primary-700 hover:to-secondary-700' : 'bg-gray-300 cursor-not-allowed'"
              class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 text-base font-medium text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:ml-3 sm:w-auto sm:text-sm" 
              @click="createTask"
            >
              {{ $t('common.confirm') }}
            </button>
            <button type="button" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm" @click="closeCreateModal">
              {{ $t('common.cancel') }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Results Modal -->
    <div v-if="showResultsModal" class="fixed z-20 inset-0 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-900 bg-opacity-50 transition-opacity backdrop-filter backdrop-blur-sm" aria-hidden="true" @click="showResultsModal = false"></div>
        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
        <div class="inline-block align-bottom bg-white rounded-2xl px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-6xl sm:w-full sm:p-8">
          <div>
            <div class="flex justify-between items-center mb-6">
              <h3 class="text-xl leading-6 font-bold text-gray-900" id="modal-title">{{ $t('tasks.resultsTitle') }}</h3>
              <button @click="showResultsModal = false" class="text-gray-400 hover:text-gray-500">
                <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <!-- Summary Section -->
            <div v-if="currentTaskSummary" class="mb-6 grid grid-cols-1 md:grid-cols-4 gap-4">
              <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <div class="text-xs font-semibold text-blue-600 uppercase">{{ $t('tasks.summary.tablesScanned') }}</div>
                <div class="text-2xl font-bold text-blue-900 mt-1">{{ currentTaskSummary.total_tables_scanned }}</div>
              </div>
              <div class="bg-purple-50 border border-purple-200 rounded-lg p-4">
                <div class="text-xs font-semibold text-purple-600 uppercase">{{ $t('tasks.summary.rowsScanned') }}</div>
                <div class="text-2xl font-bold text-purple-900 mt-1">{{ formatNumber(currentTaskSummary.total_rows_scanned) }}</div>
              </div>
              <div class="bg-red-50 border border-red-200 rounded-lg p-4">
                <div class="text-xs font-semibold text-red-600 uppercase">{{ $t('tasks.summary.issuesFound') }}</div>
                <div class="text-2xl font-bold text-red-900 mt-1">{{ currentTaskSummary.total_issues_found }}</div>
              </div>
              <div class="bg-amber-50 border border-amber-200 rounded-lg p-4">
                <div class="text-xs font-semibold text-amber-600 uppercase">{{ $t('tasks.summary.tablesAffected') }}</div>
                <div class="text-2xl font-bold text-amber-900 mt-1">{{ currentTaskSummary.tables_with_issues.length }}</div>
              </div>
            </div>

            <!-- Rules Used -->
            <div v-if="currentTaskRulesUsed && currentTaskRulesUsed.length > 0" class="mb-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h4 class="text-sm font-semibold text-blue-700 mb-3">{{ $t('tasks.summary.rulesUsed') }}</h4>
              <div class="flex flex-wrap gap-2">
                <span v-for="ruleId in currentTaskRulesUsed" :key="ruleId" class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                  {{ getRuleName(ruleId) }}
                </span>
              </div>
            </div>

            <!-- Rules Triggered -->
            <div v-if="currentTaskSummary && Object.keys(currentTaskSummary.rules_triggered).length > 0" class="mb-6 bg-gray-50 border border-gray-200 rounded-lg p-4">
              <h4 class="text-sm font-semibold text-gray-700 mb-3">{{ $t('tasks.summary.rulesTriggered') }}</h4>
              <div class="flex flex-wrap gap-2">
                <span v-for="(count, ruleName) in currentTaskSummary.rules_triggered" :key="ruleName" class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">
                  {{ ruleName }}: {{ count }}
                </span>
              </div>
            </div>

            <!-- Detailed Results by Table -->
            <div class="mt-6">
              <div class="flex justify-between items-center mb-3">
                <h4 class="text-sm font-semibold text-gray-700">{{ $t('tasks.detailedResults') }}</h4>
                <!-- Rule Filter -->
                <div v-if="availableResultRules.length > 0" class="flex items-center space-x-2">
                  <label class="text-xs text-gray-500">Filter by Rule:</label>
                  <select v-model="selectedResultRule" class="text-xs border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-1 focus:ring-primary-500">
                    <option value="">All Rules</option>
                    <option v-for="rule in availableResultRules" :key="rule" :value="rule">{{ rule }}</option>
                  </select>
                </div>
              </div>
              
              <div v-if="groupedResults && Object.keys(groupedResults).length > 0" class="space-y-4">
                <div v-for="(tableResults, tableName) in groupedResults" :key="tableName" class="border border-gray-200 rounded-lg overflow-hidden">
                  <div class="bg-gray-100 px-4 py-3 flex items-center justify-between cursor-pointer" @click="toggleResultTable(tableName)">
                    <div class="flex items-center space-x-3">
                      <svg class="h-5 w-5 text-gray-600" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M5 4a3 3 0 00-3 3v6a3 3 0 003 3h10a3 3 0 003-3V7a3 3 0 00-3-3H5zm-1 9v-1h5v2H5a1 1 0 01-1-1zm7 1h4a1 1 0 001-1v-1h-5v2zm0-4h5V8h-5v2zM9 8H4v2h5V8z" clip-rule="evenodd" />
                      </svg>
                      <span class="font-semibold text-gray-900">{{ tableName }}</span>
                      <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                        {{ tableResults.length }} {{ $t('tasks.issues') }}
                      </span>
                    </div>
                    <span class="text-gray-500">{{ expandedResultTables.includes(tableName) ? '▼' : '▶' }}</span>
                  </div>
                  <div v-if="expandedResultTables.includes(tableName)" class="bg-white">
                    <table class="min-w-full divide-y divide-gray-200">
                      <thead class="bg-gray-50">
                        <tr>
                          <th scope="col" class="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase">{{ $t('tasks.column') }}</th>
                          <th scope="col" class="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase">{{ $t('tasks.rule') }}</th>
                          <th scope="col" class="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase">{{ $t('tasks.content') }}</th>
                        </tr>
                      </thead>
                      <tbody class="divide-y divide-gray-100">
                        <tr v-for="result in tableResults" :key="result.id" class="hover:bg-gray-50">
                          <td class="px-4 py-3 text-sm font-medium text-gray-900">{{ result.column_name }}</td>
                          <td class="px-4 py-3 text-sm">
                            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                              {{ result.rule_name }}
                            </span>
                          </td>
                          <td class="px-4 py-3 text-sm font-mono text-gray-500 cursor-pointer" @click="openDetailModal(result)" title="Click to view details">
                            <div class="truncate max-w-md" v-html="highlightContent(result.sensitive_content_masked, result.rule_name)"></div>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
              <div v-else class="text-center py-12">
                <svg class="mx-auto h-12 w-12 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p class="mt-2 text-sm text-gray-500">{{ $t('tasks.noResults') }}</p>
              </div>
            </div>
          </div>
          <div class="mt-8 sm:flex sm:flex-row-reverse">
            <button type="button" class="w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:w-auto sm:text-sm" @click="showResultsModal = false">
              {{ $t('common.close') }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Detail Modal -->
    <div v-if="showDetailModal" class="fixed z-30 inset-0 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-900 bg-opacity-50 transition-opacity backdrop-filter backdrop-blur-sm" aria-hidden="true" @click="showDetailModal = false"></div>
        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
        <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6">
          <div>
            <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">Result Detail</h3>
            <div class="mt-2">
              <p class="text-sm text-gray-500 mb-2">
                <span class="font-semibold">Table:</span> {{ selectedDetail?.table_name }}<br>
                <span class="font-semibold">Column:</span> {{ selectedDetail?.column_name }}<br>
                <span class="font-semibold">Rule:</span> {{ selectedDetail?.rule_name }}
              </p>
              <div class="bg-gray-50 p-3 rounded border border-gray-200 font-mono text-sm break-all max-h-60 overflow-y-auto" v-html="highlightContent(selectedDetail?.sensitive_content_masked, selectedDetail?.rule_name)"></div>
            </div>
          </div>
          <div class="mt-5 sm:mt-6">
            <button type="button" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-primary-600 text-base font-medium text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:text-sm" @click="showDetailModal = false">
              {{ $t('common.close') }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted, computed } from 'vue';
import api from '../api';

const tasks = ref([]);
const connections = ref([]);
const results = ref([]);
const metadata = ref(null);
const showCreateModal = ref(false);
const showResultsModal = ref(false);
const selectedConnectionId = ref(null);
const selectedTables = ref([]);
const selectedRules = ref([]);
const expandedTables = ref([]);
const expandedResultTables = ref([]);
const currentTaskSummary = ref(null);
const currentTaskRulesUsed = ref([]);
const rules = ref([]);
const loadingMetadata = ref(false);
const tableSearchQuery = ref('');
const selectedResultRule = ref('');
const showDetailModal = ref(false);
const selectedDetail = ref(null);

const fetchTasks = async () => {
  try {
    const response = await api.get('/tasks/');
    tasks.value = response.data.sort((a, b) => new Date(b.start_time) - new Date(a.start_time));
  } catch (e) {
    console.error(e);
  }
};

const fetchConnections = async () => {
  try {
    const response = await api.get('/connections/');
    connections.value = response.data;
  } catch (e) {
    console.error(e);
  }
};

const fetchRules = async () => {
  try {
    const response = await api.get('/rules/');
    rules.value = response.data;
    selectedRules.value = rules.value.map(r => r.id);
  } catch (e) {
    console.error(e);
  }
};

const loadMetadata = async () => {
  if (!selectedConnectionId.value) {
    metadata.value = null;
    selectedTables.value = [];
    expandedTables.value = [];
    loadingMetadata.value = false;
    return;
  }
  loadingMetadata.value = true;
  try {
    const response = await api.get(`/tasks/metadata/${selectedConnectionId.value}`);
    metadata.value = response.data;
    selectedTables.value = [];
    expandedTables.value = [];
    tableSearchQuery.value = '';
  } catch (e) {
    console.error('Failed to load metadata:', e);
    metadata.value = null;
  } finally {
    loadingMetadata.value = false;
  }
};

const filteredTables = computed(() => {
  if (!metadata.value || !metadata.value.tables) return [];
  if (!tableSearchQuery.value) return metadata.value.tables;
  const query = tableSearchQuery.value.toLowerCase();
  return metadata.value.tables.filter(t => t.name.toLowerCase().includes(query));
});

const createTask = async () => {
  if (!selectedConnectionId.value) return;
  try {
    const payload = {
      connection_id: selectedConnectionId.value
    };
    if (selectedTables.value.length > 0) {
      payload.table_names = selectedTables.value;
    }
    if (selectedRules.value.length > 0) {
      payload.rule_ids = selectedRules.value;
    }
    await api.post('/tasks/', payload);
    closeCreateModal();
    fetchTasks();
  } catch (e) {
    console.error(e);
    alert('Failed to start scan');
  }
};

const deleteTask = async (task) => {
  if (!confirm('Are you sure you want to delete this scan task?')) return;
  try {
    await api.delete(`/tasks/${task.id}`);
    fetchTasks();
  } catch (e) {
    console.error(e);
    alert('Failed to delete task');
  }
};

const exportTask = async (task, format = 'docx') => {
  try {
    const response = await api.get(`/tasks/${task.id}/export`, { 
      params: { format },
      responseType: 'blob' 
    });
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `scan_report_${task.id}.${format}`);
    document.body.appendChild(link);
    link.click();
    link.remove();
  } catch (e) {
    console.error(e);
    alert('Failed to export report');
  }
};

const viewResults = async (task) => {
  if (task.status !== 'completed') return;
  try {
    const response = await api.get(`/tasks/${task.id}/results`);
    results.value = response.data;
    
    if (task.scan_summary) {
      try {
        currentTaskSummary.value = JSON.parse(task.scan_summary);
      } catch (e) {
        currentTaskSummary.value = null;
      }
    } else {
      currentTaskSummary.value = null;
    }
    
    if (task.selected_rules) {
      try {
        currentTaskRulesUsed.value = JSON.parse(task.selected_rules);
      } catch (e) {
        currentTaskRulesUsed.value = [];
      }
    } else {
      currentTaskRulesUsed.value = [];
    }
    
    expandedResultTables.value = [];
    selectedResultRule.value = '';
    showResultsModal.value = true;
  } catch (e) {
    console.error(e);
  }
};

const openCreateModal = async () => {
  showCreateModal.value = true;
  if (selectedConnectionId.value && !metadata.value) {
    await loadMetadata();
  }
};

const closeCreateModal = () => {
  showCreateModal.value = false;
  selectedTables.value = [];
  selectedRules.value = rules.value.map(r => r.id);
  expandedTables.value = [];
  metadata.value = null;
  tableSearchQuery.value = '';
};

const toggleTableExpand = (tableName) => {
  const index = expandedTables.value.indexOf(tableName);
  if (index > -1) {
    expandedTables.value.splice(index, 1);
  } else {
    expandedTables.value.push(tableName);
  }
};

const toggleResultTable = (tableName) => {
  const index = expandedResultTables.value.indexOf(tableName);
  if (index > -1) {
    expandedResultTables.value.splice(index, 1);
  } else {
    expandedResultTables.value.push(tableName);
  }
};

const toggleSelectAll = () => {
  if (allTablesSelected.value) {
    selectedTables.value = [];
  } else {
    selectedTables.value = filteredTables.value.map(t => t.name);
  }
};

const allTablesSelected = computed(() => {
  return filteredTables.value.length > 0 && selectedTables.value.length === filteredTables.value.length;
});

const allRulesSelected = computed(() => {
  return selectedRules.value.length === rules.value.length;
});

const canCreateScan = computed(() => {
  return selectedConnectionId.value !== null && selectedRules.value.length > 0;
});

const toggleSelectAllRules = () => {
  if (allRulesSelected.value) {
    selectedRules.value = [];
  } else {
    selectedRules.value = rules.value.map(r => r.id);
  }
};

const groupedResults = computed(() => {
  const grouped = {};
  results.value.forEach(result => {
    if (selectedResultRule.value && result.rule_name !== selectedResultRule.value) {
      return;
    }
    if (!grouped[result.table_name]) {
      grouped[result.table_name] = [];
    }
    grouped[result.table_name].push(result);
  });
  return grouped;
});

const availableResultRules = computed(() => {
  const ruleNames = new Set(results.value.map(r => r.rule_name));
  return Array.from(ruleNames);
});

const highlightContent = (content, ruleName) => {
  if (!content) return '';
  const rule = rules.value.find(r => r.name === ruleName);
  if (!rule) return content;

  let highlighted = content;
  try {
    if (rule.rule_type === 'regex') {
      const regex = new RegExp(rule.content, 'gi');
      highlighted = content.replace(regex, match => `<mark class="bg-yellow-200 text-yellow-900 rounded px-0.5">${match}</mark>`);
    } else {
      const regex = new RegExp(rule.content.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
      highlighted = content.replace(regex, match => `<mark class="bg-yellow-200 text-yellow-900 rounded px-0.5">${match}</mark>`);
    }
  } catch (e) {
    console.error('Highlight error:', e);
  }
  return highlighted;
};

const openDetailModal = (result) => {
  selectedDetail.value = result;
  showDetailModal.value = true;
};

const getStatusClass = (status) => {
  switch (status) {
    case 'completed': return 'bg-green-100 text-green-600';
    case 'running': return 'bg-blue-100 text-blue-600';
    case 'failed': return 'bg-red-100 text-red-600';
    default: return 'bg-gray-100 text-gray-600';
  }
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  return new Date(dateString).toLocaleString();
};

const calculateDuration = (start, end) => {
  if (!start || !end) return '-';
  const diff = new Date(end) - new Date(start);
  return (diff / 1000).toFixed(2) + 's';
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

const parseRulesUsed = (rulesJson) => {
  try {
    return JSON.parse(rulesJson);
  } catch (e) {
    return [];
  }
};

const getRuleName = (ruleId) => {
  const rule = rules.value.find(r => r.id === ruleId);
  return rule ? rule.name : `Rule #${ruleId}`;
};

onMounted(() => {
  fetchTasks();
  fetchConnections();
  fetchRules();
  setInterval(fetchTasks, 5000);
});
</script>
