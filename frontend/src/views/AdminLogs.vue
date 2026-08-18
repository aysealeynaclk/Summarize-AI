<script setup>
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import apiClient from '../api/client'

const { t } = useI18n()

const logs = ref([])
const error = ref('')
const loading = ref(true)

async function loadLogs() {
  loading.value = true
  error.value = ''
  try {
    const { data } = await apiClient.get('/admin/logs')
    logs.value = data
  } catch (err) {
    error.value = err.response?.data?.detail || t('adminLogs.genericError')
  } finally {
    loading.value = false
  }
}

function truncate(str, len = 60) {
  if (!str) return '-'
  return str.length > len ? str.slice(0, len) + '...' : str
}

onMounted(loadLogs)
</script>

<template>
  <div class="max-w-5xl mx-auto px-4 py-10">
    <h1 class="text-2xl font-bold text-slate-800 mb-1">{{ t('adminLogs.title') }}</h1>
    <p class="text-slate-500 mb-6">{{ t('adminLogs.subtitle') }}</p>

    <p v-if="error" class="text-sm text-red-600 bg-red-50 border border-red-100 rounded-lg px-3 py-2 mb-4">
      {{ error }}
    </p>

    <div class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-x-auto">
      <table class="w-full text-sm">
        <thead>
          <tr class="text-left text-slate-500 border-b border-slate-100">
            <th class="px-4 py-3 font-medium">{{ t('adminLogs.date') }}</th>
            <th class="px-4 py-3 font-medium">{{ t('adminLogs.user') }}</th>
            <th class="px-4 py-3 font-medium">{{ t('adminLogs.input') }}</th>
            <th class="px-4 py-3 font-medium">{{ t('adminLogs.summary') }}</th>
            <th class="px-4 py-3 font-medium">{{ t('adminLogs.provider') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading">
            <td colspan="5" class="px-4 py-6 text-center text-slate-400">{{ t('adminLogs.loading') }}</td>
          </tr>
          <tr v-else-if="!logs.length">
            <td colspan="5" class="px-4 py-6 text-center text-slate-400">{{ t('adminLogs.empty') }}</td>
          </tr>
          <tr v-for="log in logs" :key="log.id" class="border-b border-slate-50 last:border-0">
            <td class="px-4 py-3 text-slate-500 whitespace-nowrap">
              {{ new Date(log.created_at).toLocaleString('tr-TR') }}
            </td>
            <td class="px-4 py-3 text-slate-700">{{ log.username_or_email }}</td>
            <td class="px-4 py-3 text-slate-600">{{ truncate(log.input_text) }}</td>
            <td class="px-4 py-3 text-slate-600">{{ truncate(log.output_summary) }}</td>
            <td class="px-4 py-3 text-slate-500">{{ log.provider }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
