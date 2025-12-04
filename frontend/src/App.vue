<template>
  <Toast ref="toast" />
  <ConfirmDialog ref="confirm" />
  <router-view />
</template>

<script setup>
import { ref, provide } from 'vue';
import Toast from './components/Toast.vue';
import ConfirmDialog from './components/ConfirmDialog.vue';

const toast = ref(null);
const confirm = ref(null);

// Provide toast and confirm globally
provide('toast', toast);
provide('confirm', confirm);
</script>
